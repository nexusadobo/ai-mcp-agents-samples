import asyncio
import os
import sys
from pathlib import Path

# Añadir el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent.parent))

from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.mcp import MCPServer, MCPServerStdio
from utils.azure_client import get_azure_openai_client, get_chat_deployment_name

async def test_combined_mcp_servers():
    # Usar el directorio padre (raíz del proyecto) para encontrar sample_files
    current_dir = Path(__file__).parent.parent
    samples_dir = current_dir / "sample_files"
    
    azure_open_ai_client = get_azure_openai_client()
    set_tracing_disabled(disabled=True)

    # Create both filesystem and playwright servers
    async with MCPServerStdio(
        name="Filesystem Server",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", str(samples_dir)],
        },
    ) as filesystem_server, MCPServerStdio(
        name="Playwright Server", 
        params={
            "command": "npx",
            "args": ["-y", "@microsoft/playwright-mcp"],
        },
    ) as playwright_server:
        
        agent = Agent(
            name="Full-Stack Assistant",
            instructions="""You are a powerful assistant with both file system and web automation capabilities. You can:
            
            FILESYSTEM OPERATIONS:
            - Read, write, and manage files
            - Create directories and organize files
            - Search through file contents
            
            WEB AUTOMATION:
            - Navigate to websites
            - Take screenshots
            - Interact with web elements
            - Extract data from web pages
            - Automate web workflows
            
            COMBINED WORKFLOWS:
            - Scrape web data and save to files
            - Read local files and use data for web automation
            - Create reports combining web data and local files
            
            Be helpful and demonstrate your full capabilities.""",
            model=OpenAIChatCompletionsModel(
                model=get_chat_deployment_name(), 
                openai_client=azure_open_ai_client
            ),
            mcp_servers=[filesystem_server, playwright_server],
        )

        print("🚀 TESTING COMBINED MCP CAPABILITIES")
        print("=" * 80)

        # Test 1: List all available tools
        message1 = "What tools do you have available? List both your filesystem and web automation capabilities."
        print(f"\n📋 Test 1: {message1}")
        result1 = await Runner.run(starting_agent=agent, input=message1)
        print(result1.final_output)

        # Test 2: Web scraping + file saving
        message2 = "Navigate to https://httpbin.org/json, extract the data you find, and save it to a file called 'web_data.json' in the sample_files folder."
        print(f"\n🌐 Test 2: {message2}")
        result2 = await Runner.run(starting_agent=agent, input=message2)
        print(result2.final_output)

        # Test 3: Read file and create web report
        message3 = "Read the favorite_books.txt file and create an HTML report about the books. Save it as 'books_report.html'."
        print(f"\n📚 Test 3: {message3}")
        result3 = await Runner.run(starting_agent=agent, input=message3)
        print(result3.final_output)

        # Test 4: Web automation with form filling
        message4 = "Navigate to https://httpbin.org/forms/post and take a screenshot of the form. Then describe what form fields are available."
        print(f"\n📝 Test 4: {message4}")
        result4 = await Runner.run(starting_agent=agent, input=message4)
        print(result4.final_output)

if __name__ == "__main__":
    asyncio.run(test_combined_mcp_servers())