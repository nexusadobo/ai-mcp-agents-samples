import asyncio
import os
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.mcp import MCPServer, MCPServerStdio
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

def get_azure_open_ai_client():
    load_dotenv()
    return AsyncAzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

async def test_playwright_mcp():
    azure_open_ai_client = get_azure_open_ai_client()
    set_tracing_disabled(disabled=True)

    async with MCPServerStdio(
        name="Playwright Server",
        params={
            "command": "npx",
            "args": ["-y", "@playwright/mcp@latest", "--headless", "--browser", "chromium"],
        },
    ) as playwright_server:
        
        agent = Agent(
            name="Web Automation Assistant",
            instructions="""You are a web automation assistant with Playwright capabilities. You can:
            1. Navigate to websites
            2. Take screenshots
            3. Interact with web elements (click, type, etc.)
            4. Extract information from web pages
            5. Automate web workflows
            
            When listing your tools, be specific about what web automation actions you can perform.""",
            model=OpenAIChatCompletionsModel(
                model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"), 
                openai_client=azure_open_ai_client
            ),
            mcp_servers=[playwright_server],
        )

        # Ask the agent to list its Playwright tools
        message = "What web automation tools do you have available? Please list all your Playwright capabilities and what each tool can do."
        print(f"Asking agent: {message}")
        print("=" * 80)
        
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)
        
        print("\n" + "=" * 80)
        print("Testing basic web navigation:")
        
        # Test basic navigation
        message2 = "Navigate to https://www.ferrovial.com/es-es/ and take a screenshot. Then tell me what you see on the page."
        print(f"\nTesting: {message2}")
        result2 = await Runner.run(starting_agent=agent, input=message2)
        print(result2.final_output)

if __name__ == "__main__":
    asyncio.run(test_playwright_mcp())