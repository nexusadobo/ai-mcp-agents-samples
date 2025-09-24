"""
Test específico para análisis de código con GitHub MCP Server.
Demuestra diferentes tipos de análisis que se pueden hacer.
"""

import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Agregar el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent))

from servers.server_manager import ServerManager
from ai_agents.agent_factory import AgentFactory
from agents import Runner


async def test_code_analysis():
    """
    Test específico para análisis de código.
    """
    print("🔍 Test de análisis de código GitHub MCP")
    print("=" * 50)
    
    try:
        async with ServerManager.create_github_server() as server:
            agent = AgentFactory.create_github_agent([server])
            
            # 1. Listar repositorios del usuario
            print("\n📂 Listando repositorios...")
            result = await Runner.run(
                starting_agent=agent,
                input="Lista mis repositorios de GitHub. Muestra los 5 más recientes con sus lenguajes principales."
            )
            print("Respuesta:", result.final_output[:500] + "..." if len(result.final_output) > 500 else result.final_output)
            
            # 2. Análisis de un repositorio específico
            print("\n🔬 Analizando estructura de repositorio...")
            result = await Runner.run(
                starting_agent=agent,
                input="Analiza la estructura de archivos de uno de mis repositorios. Muestra los tipos de archivos, directorios principales y arquitectura del código."
            )
            print("Respuesta:", result.final_output[:500] + "..." if len(result.final_output) > 500 else result.final_output)
            
            # 3. Búsqueda de código
            print("\n🔎 Búsqueda de código...")
            result = await Runner.run(
                starting_agent=agent,
                input="Busca ejemplos de funciones o clases en mis repositorios. Muestra algunos patrones de código interesantes que encuentres."
            )
            print("Respuesta:", result.final_output[:500] + "..." if len(result.final_output) > 500 else result.final_output)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n✅ Test de análisis de código completado!")
    return True


async def main():
    """Función principal."""
    success = await test_code_analysis()
    
    if success:
        print("\n🎉 Las capacidades de análisis de código están funcionando!")
    else:
        print("\n⚠️  Hubo problemas con el análisis de código")


if __name__ == "__main__":
    asyncio.run(main())