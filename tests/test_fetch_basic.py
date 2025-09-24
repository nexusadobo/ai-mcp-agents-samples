"""
Test básico y rápido para el servidor Fetch MCP.
Solo verifica conectividad y herramientas disponibles.
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


async def test_fetch_basic():
    """
    Test básico del servidor Fetch MCP.
    Solo verifica conectividad sin hacer llamadas HTTP complejas.
    """
    print("🌐 Test básico de Fetch MCP Server")
    print("=" * 50)
    
    try:
        print("🔗 Conectando con Fetch MCP Server...")
        
        async with MCPServerStdio(
            name="Fetch Server",
            params={
                "command": "uvx",
                "args": ["mcp-server-fetch"],
            },
        ) as server:
            print("✅ Fetch Server conectado exitosamente!")
            
            # Crear agente básico
            agent = AgentFactory.create_base_agent(
                name="HTTP Test Agent",
                instructions="You are a simple HTTP testing agent. List your available tools briefly.",
                mcp_servers=[server]
            )
            
            # Solo verificar herramientas disponibles
            print("\n🛠️ Verificando herramientas disponibles...")
            result = await Runner.run(
                starting_agent=agent,
                input="List your available tools, focusing on HTTP/fetch capabilities. Be brief."
            )
            
            print("\n🤖 Herramientas disponibles:")
            print("-" * 40)
            # Mostrar solo las primeras 500 caracteres para mantenerlo conciso
            output = result.final_output
            if len(output) > 500:
                print(output[:500] + "...")
            else:
                print(output)
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        return False
    
    print("\n✅ Test básico completado exitosamente!")
    return True


async def main():
    """Función principal del test."""
    success = await test_fetch_basic()
    
    if success:
        print("\n🎉 Fetch MCP Server está funcionando correctamente!")
        print("💡 Puedes usar este servidor para hacer llamadas HTTP/fetch")
    else:
        print("\n⚠️  Revisa la configuración antes de usar Fetch MCP Server")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())