"""
Test básico para el servidor GitHub MCP.
Solo se conecta y muestra las herramientas disponibles.
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


async def test_github_connection():
    """
    Test básico de conexión con GitHub MCP Server.
    Muestra las herramientas disponibles sin realizar operaciones.
    """
    print("🔧 Test de conexión GitHub MCP Server")
    print("=" * 50)
    
    try:
        print("🔗 Conectando con GitHub MCP Server...")
        print("⏳ Esto puede tomar unos momentos...")
        
        async with ServerManager.create_github_server() as server:
            print("✅ Conexión exitosa!")
            
            # Crear agente GitHub
            agent = AgentFactory.create_github_agent([server])
            
            # Preguntar sobre capacidades (consulta más simple)
            print("\n🛠️  Consultando herramientas disponibles...")
            result = await Runner.run(
                starting_agent=agent,
                input="List your available tools briefly."
            )
            
            print("\n🤖 Respuesta del agente:")
            print("-" * 40)
            print(result.final_output)
            print("-" * 40)
            
            # Test de análisis de código
            print("\n🔍 Probando análisis de código...")
            result = await Runner.run(
                starting_agent=agent,
                input="Analiza mi repositorio más reciente. Muéstrame información sobre los archivos de código, lenguajes usados, y estructura del proyecto."
            )
            
            print("\n🤖 Análisis de código:")
            print("-" * 40)
            print(result.final_output)
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        print("\n💡 Consejos para solucionar:")
        print("   • Verifica que GITHUB_TOKEN esté configurado en tu .env")
        print("   • Asegúrate de que Node.js y npm estén instalados")
        print("   • Verifica tu conexión a internet")
        return False
    
    print("\n✅ Test completado exitosamente!")
    return True


async def main():
    """Función principal del test."""
    success = await test_github_connection()
    
    if success:
        print("\n🎉 GitHub MCP Server está funcionando correctamente!")
    else:
        print("\n⚠️  Revisa la configuración antes de usar GitHub MCP Server")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())