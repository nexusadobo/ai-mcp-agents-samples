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

async def simple_playwright_test():
    print("🔧 Verificando si npx está disponible...")
    if not shutil.which("npx"):
        print("❌ ERROR: npx no está instalado. Se necesita Node.js y npm.")
        return
    print("✅ npx encontrado")

    print("\n📦 Intentando conectar con Playwright MCP...")
    
    try:
        azure_open_ai_client = get_azure_openai_client()
        set_tracing_disabled(disabled=True)

        async with MCPServerStdio(
            name="Playwright Server",
            params={
                "command": "npx",
                "args": ["-y", "@playwright/mcp@latest", "--headless", "--browser", "chromium"],
            },
        ) as playwright_server:
            
            print("✅ Servidor MCP de Playwright conectado exitosamente")
            
            agent = Agent(
                name="Simple Web Agent",
                instructions="You are a simple web automation agent. Just tell me what tools you have available.",
                model=OpenAIChatCompletionsModel(
                    model=get_chat_deployment_name(), 
                    openai_client=azure_open_ai_client
                ),
                mcp_servers=[playwright_server],
            )

            print("\n🤖 Preguntando al agente sobre sus herramientas...")
            message = "What tools do you have? List them briefly."
            
            result = await Runner.run(starting_agent=agent, input=message)
            print(f"\n📋 Respuesta del agente:\n{result.final_output}")
            
    except Exception as e:
        print(f"❌ ERROR al conectar con Playwright MCP: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        
        # Intentar con versión alternativa
        print("\n🔄 Intentando con versión alternativa...")
        try:
            async with MCPServerStdio(
                
                name="Playwright Server Alt",
                params={
                    "command": "npx",
                    "args": ["-y", "@microsoft/playwright-mcp"],
                },
            ) as playwright_server_alt:
                print("✅ Versión alternativa conectada")
        except Exception as e2:
            print(f"❌ ERROR también con versión alternativa: {e2}")

if __name__ == "__main__":
    asyncio.run(simple_playwright_test())