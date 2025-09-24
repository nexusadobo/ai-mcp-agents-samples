import asyncio
import os
import sys
from pathlib import Path

# Añadir el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent.parent))

from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.mcp import MCPServer, MCPServerStdio
from utils.azure_client import get_azure_openai_client, get_chat_deployment_name

async def list_mcp_tools():
    # Usar el directorio padre (raíz del proyecto) para encontrar sample_files
    current_dir = Path(__file__).parent.parent
    samples_dir = current_dir / "sample_files"
    
    azure_open_ai_client = get_azure_openai_client()
    set_tracing_disabled(disabled=True)

    async with MCPServerStdio(
        name="Filesystem Server",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", str(samples_dir)],
        },
    ) as server:
        
        agent = Agent(
            name="Tool Inspector",
            instructions="You are a helpful assistant that can inspect and list available tools. When asked about your capabilities, list all the tools you have access to with a brief description of what each one does.",
            model=OpenAIChatCompletionsModel(
                model=get_chat_deployment_name(), 
                openai_client=azure_open_ai_client
            ),
            mcp_servers=[server],
        )

        # Ask the agent to list its tools
        message = "What tools do you have available? Please list all your capabilities and what each tool can do."
        print(f"Asking agent: {message}")
        print("=" * 60)
        
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)
        
        print("\n" + "=" * 60)
        print("Additional test - asking for specific tool details:")
        
        # Ask for more specific details
        message2 = "Can you show me specifically what filesystem operations you can perform? What are the exact tool names and parameters?"
        result2 = await Runner.run(starting_agent=agent, input=message2)
        print(result2.final_output)

if __name__ == "__main__":
    asyncio.run(list_mcp_tools())