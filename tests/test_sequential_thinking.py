"""
Test para el servidor Sequential Thinking MCP.
Demuestra pensamiento estructurado paso a paso.
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent))

from servers.server_manager import ServerManager
from ai_agents.agent_factory import AgentFactory
from agents import Runner


async def test_sequential_thinking():
    """
    Test del servidor Sequential Thinking MCP.
    """
    print("🧠 Test de Sequential Thinking MCP Server")
    print("=" * 50)
    
    try:
        async with ServerManager.create_sequential_thinking_server() as server:
            agent = AgentFactory.create_sequential_thinking_agent([server])
            
            # Test 1: Análisis de problema técnico
            print("\n🔧 Analizando problema técnico paso a paso...")
            result = await Runner.run(
                starting_agent=agent,
                input="Tengo una aplicación web que se vuelve lenta cuando hay muchos usuarios. Necesito identificar las causas y proponer soluciones. Analiza esto sistemáticamente."
            )
            
            print("\n🤖 Análisis estructurado:")
            print("-" * 50)
            print(result.final_output)
            print("-" * 50)
            
            # Test 2: Planificación de proyecto
            print("\n📋 Planificando proyecto de software...")
            result = await Runner.run(
                starting_agent=agent,
                input="Quiero crear una API REST para un sistema de gestión de inventarios. Necesito planificar la arquitectura, endpoints, base de datos y seguridad. Hazlo paso a paso."
            )
            
            print("\n🤖 Planificación estructurada:")
            print("-" * 50)
            print(result.final_output)
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n✅ Test de Sequential Thinking completado!")
    return True


async def main():
    """Función principal."""
    success = await test_sequential_thinking()
    
    if success:
        print("\n🎉 Sequential Thinking MCP Server funcionando correctamente!")
        print("💡 Puedes usar pensamiento estructurado para problemas complejos")
    else:
        print("\n⚠️  Hubo problemas con Sequential Thinking")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())