"""
Test para el servidor Fetch MCP.
Demuestra capacidades de hacer llamadas HTTP/REST API.
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent))

from servers.server_manager import ServerManager
from ai_agents.agent_factory import AgentFactory
from agents import Runner
from agents.mcp import MCPServerStdio


async def test_fetch_server():
    """
    Test del servidor Fetch MCP.
    """
    print("🌐 Test de Fetch MCP Server")
    print("=" * 50)
    
    try:
        # Crear servidor Fetch siguiendo el patrón del proyecto
        print("🔗 Conectando con Fetch MCP Server...")
        print("⏳ Esto puede tomar unos momentos...")
        
        async with MCPServerStdio(
            name="Fetch Server",
            params={
                "command": "uvx",
                "args": ["mcp-server-fetch"],
            },
        ) as server:
            print("✅ Fetch Server conectado exitosamente!")
            
            # Crear agente con capacidades HTTP
            agent = AgentFactory.create_base_agent(
                name="HTTP API Assistant",
                instructions="""You are an HTTP API specialist. You can:
                1. Make GET requests to fetch data from APIs
                2. Make POST requests to send data
                3. Handle different content types (JSON, XML, HTML)
                4. Process and analyze API responses
                5. Work with REST APIs and web services
                
                Always explain what API calls you're making and why.
                Be careful with external API calls and respect rate limits.""",
                mcp_servers=[server]
            )
            
            # Test 1: Verificar herramientas disponibles
            print("\n🛠️ Consultando herramientas HTTP disponibles...")
            result = await Runner.run(
                starting_agent=agent,
                input="What HTTP tools do you have available? List them briefly with their capabilities."
            )
            
            print("\n🤖 Herramientas disponibles:")
            print("-" * 50)
            print(result.final_output)
            print("-" * 50)
            
            # Test 2: Hacer una llamada HTTP simple y segura
            print("\n🔍 Probando llamada HTTP básica...")
            result = await Runner.run(
                starting_agent=agent,
                input="Use your fetch tool to make a simple GET request to https://httpbin.org/json. Show me what you get back."
            )
            
            print("\n🤖 Resultado de la llamada HTTP:")
            print("-" * 50)
            print(result.final_output)
            print("-" * 50)
            
            # Test 3: Información de IP (otro endpoint seguro)
            print("\n📍 Obteniendo información de IP...")
            result = await Runner.run(
                starting_agent=agent,
                input="Use your fetch tool to get my public IP from https://httpbin.org/ip"
            )
            
            print("\n🤖 Información de IP:")
            print("-" * 50)
            print(result.final_output)
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        print("\n💡 Consejos para solucionar:")
        print("   • Verifica que Node.js y npm estén instalados")
        print("   • Asegúrate de tener conexión a internet")
        print("   • Verifica que npx funcione correctamente")
        return False
    
    print("\n✅ Test de Fetch Server completado exitosamente!")
    return True


async def main():
    """Función principal del test."""
    success = await test_fetch_server()
    
    if success:
        print("\n🎉 Fetch MCP Server está funcionando correctamente!")
        print("💡 Puedes usar este servidor para hacer llamadas HTTP/API REST")
    else:
        print("\n⚠️  Revisa la configuración antes de usar Fetch MCP Server")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())