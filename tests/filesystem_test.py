import asyncio
import os
import sys
import shutil
from pathlib import Path

# Añadir el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent.parent))

from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.mcp import MCPServer, MCPServerStdio
from utils.azure_client import get_azure_openai_client, get_chat_deployment_name


async def run(mcp_server: MCPServer):

    azure_open_ai_client = get_azure_openai_client()
    set_tracing_disabled(disabled=True)

    agent = Agent(
        name="Assistant",
        instructions="""You are a helpful coding assistant. You can:
        1. Read files in the sample_files directory
        2. Create new files in the sample_files directory
        3. Analyze code and provide suggestions
        4. Write code examples and programs
        
        When creating files, make sure to write clean, well-commented code.""",
        model=OpenAIChatCompletionsModel(model=get_chat_deployment_name(), 
                                         openai_client=azure_open_ai_client),
        mcp_servers=[mcp_server],
    )

    # List the files it can read
    message = "Read the files in `sample_files` folder, and list them."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Ask the agent to create a simple Python program
    message = "Create a simple Python program called 'hello_world.py' in the sample_files folder. The program should greet the user and ask for their name, then say hello to them personally."
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Ask the agent to create a more complex program
    message = "Create a Python program called 'number_game.py' that implements a simple number guessing game where the computer picks a random number between 1 and 10, and the user has to guess it."
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Ask the agent to create a data structure example
    message = "Create a Python file called 'student_manager.py' with a simple class to manage student information (name, age, grades). Include methods to add grades and calculate average."
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Ask about books (original example)
    message = "What is my #1 favorite book?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():
    # Usar el directorio padre (raíz del proyecto) para encontrar sample_files
    current_dir = Path(__file__).parent.parent
    samples_dir = current_dir / "sample_files"

    async with MCPServerStdio(
        name="Filesystem Server, via npx",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", str(samples_dir)],
        },
    ) as server:
        await run(server)


if __name__ == "__main__":
    # Let's make sure the user has npx installed
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")

    asyncio.run(main())
