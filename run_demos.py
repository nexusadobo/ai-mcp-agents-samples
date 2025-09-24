"""
Script principal unificado para ejecutar diferentes demos y pruebas.
Punto de entrada central para todas las funcionalidades del proyecto.
"""

import asyncio
import argparse
import sys
from typing import Optional

from agents import Runner
from ai_agents.agent_factory import AgentFactory
from servers.server_manager import ServerManager


async def run_filesystem_demo():
    """Ejecuta el demo del sistema de archivos."""
    print("🔧 Iniciando demo del sistema de archivos...")
    
    async with ServerManager.create_filesystem_server() as server:
        agent = AgentFactory.create_filesystem_agent([server])
        
        # Listar archivos
        print("\n📋 Listando archivos en sample_files...")
        result = await Runner.run(
            starting_agent=agent, 
            input="Read the files in `sample_files` folder, and list them."
        )
        print(result.final_output)
        
        # Crear un programa simple
        print("\n🔨 Creando un programa simple...")
        result = await Runner.run(
            starting_agent=agent,
            input="Create a simple Python program called 'demo_hello.py' in the sample_files folder. The program should greet the user and ask for their name."
        )
        print(result.final_output)
        
        # Preguntar sobre libros favoritos
        print("\n📚 Preguntando sobre libros favoritos...")
        result = await Runner.run(
            starting_agent=agent,
            input="What is my #1 favorite book?"
        )
        print(result.final_output)


async def run_github_demo():
    """
    Demo del agente GitHub con operaciones de repositorio.
    Muestra gestión de repositorios, issues, PRs y análisis de código.
    """
    print("🔧 Iniciando demo de GitHub...")
    
    try:
        async with ServerManager.create_github_server() as server:
            agent = AgentFactory.create_github_agent([server])
            
            # Analizar perfil y repositorios
            print("\n👤 Analizando perfil de GitHub...")
            result = await Runner.run(
                starting_agent=agent,
                input="Analiza mi perfil de GitHub. Muestra mis repositorios más recientes (últimos 5) y estadísticas generales de actividad."
            )
            print(result.final_output)
            
            # Consultar issues abiertas
            print("\n🐛 Consultando issues abiertas...")
            result = await Runner.run(
                starting_agent=agent,
                input="Revisa las issues abiertas en mis repositorios principales y proporciona un resumen del estado actual."
            )
            print(result.final_output)
            
    except Exception as e:
        print(f"❌ Error en demo GitHub: {e}")
        print("💡 Asegúrate de tener configurado GITHUB_TOKEN en tu archivo .env")


async def run_sequential_thinking_demo():
    """
    Demo del agente Sequential Thinking para análisis estructurado.
    Muestra pensamiento paso a paso para resolución de problemas complejos.
    """
    print("🔧 Iniciando demo de Sequential Thinking...")
    
    async with ServerManager.create_sequential_thinking_server() as server:
        agent = AgentFactory.create_sequential_thinking_agent([server])
        
        # Problema complejo de análisis
        print("\n🧠 Analizando problema complejo paso a paso...")
        result = await Runner.run(
            starting_agent=agent,
            input="Necesito diseñar una arquitectura de software para un sistema de e-commerce que maneje alta concurrencia, tenga múltiples métodos de pago, y soporte internacionalización. Analiza esto paso a paso considerando todos los aspectos técnicos y de negocio."
        )
        print(result.final_output)
        
        # Análisis de código estructurado
        print("\n🔍 Análisis estructurado de mejoras de código...")
        result = await Runner.run(
            starting_agent=agent,
            input="Tengo un sistema Python con problemas de rendimiento. Los usuarios se quejan de lentitud en las consultas de base de datos y la interfaz web. Analiza sistemáticamente las posibles causas y soluciones, considerando tanto el backend como el frontend."
        )
        print(result.final_output)


async def run_fetch_demo():
    """
    Demo del agente Fetch para operaciones HTTP/REST API.
    Muestra capacidades de realizar llamadas HTTP y procesar respuestas.
    """
    print("🔧 Iniciando demo de Fetch...")
    
    async with ServerManager.create_fetch_server() as server:
        agent = AgentFactory.create_fetch_agent([server])
        
        # Test básico de herramientas
        print("\n🛠️ Verificando herramientas HTTP disponibles...")
        result = await Runner.run(
            starting_agent=agent,
            input="List your HTTP/API tools and capabilities briefly."
        )
        print(result.final_output)
        
        # Test de llamada HTTP simple
        print("\n🌐 Realizando llamada HTTP de prueba...")
        result = await Runner.run(
            starting_agent=agent,
            input="Use your fetch tool to get data from https://httpbin.org/json and show me the response structure."
        )
        print(result.final_output)


async def run_playwright_demo():
    """Ejecuta el demo de Playwright."""
    print("🔧 Iniciando demo de Playwright...")
    
    async with ServerManager.create_playwright_server() as server:
        agent = AgentFactory.create_web_automation_agent([server])
        
        print("\n🤖 Preguntando al agente sobre sus herramientas web...")
        result = await Runner.run(
            starting_agent=agent,
            input="What web automation tools do you have? List them briefly with examples of what each can do."
        )
        print(result.final_output)


async def run_combined_demo():
    """Ejecuta el demo combinado (filesystem + Playwright)."""
    print("🔧 Iniciando demo combinado...")
    
    async with ServerManager.create_combined_servers() as (fs_server, pw_server):
        agent = AgentFactory.create_combined_agent([fs_server, pw_server])
        
        print("\n🤖 Preguntando sobre capacidades combinadas...")
        result = await Runner.run(
            starting_agent=agent,
            input="What are all your capabilities? List both file system and web automation tools you have available."
        )
        print(result.final_output)


async def run_tool_inspection():
    """Ejecuta la inspección de herramientas."""
    print("🔧 Iniciando inspección de herramientas...")
    
    async with ServerManager.create_filesystem_server() as server:
        agent = AgentFactory.create_tool_inspector_agent([server])
        
        print("\n🔍 Inspeccionando herramientas disponibles...")
        result = await Runner.run(
            starting_agent=agent,
            input="What tools do you have available? Please list all your capabilities and what each tool can do."
        )
        print(result.final_output)


async def run_interactive_mode():
    """Modo interactivo para preguntas personalizadas."""
    print("🔧 Iniciando modo interactivo...")
    print("Selecciona el tipo de servidor:")
    print("1. Solo filesystem")
    print("2. Solo Playwright")
    print("3. Solo GitHub")
    print("4. Solo Sequential Thinking")
    print("5. Solo Fetch (HTTP/API)")
    print("6. Combinado (filesystem + Playwright)")
    
    choice = input("Selección (1-6): ").strip()
    
    if choice == "1":
        async with ServerManager.create_filesystem_server() as server:
            agent = AgentFactory.create_filesystem_agent([server])
            await interactive_chat(agent)
    elif choice == "2":
        async with ServerManager.create_playwright_server() as server:
            agent = AgentFactory.create_web_automation_agent([server])
            await interactive_chat(agent)
    elif choice == "3":
        try:
            async with ServerManager.create_github_server() as server:
                agent = AgentFactory.create_github_agent([server])
                await interactive_chat(agent)
        except Exception as e:
            print(f"❌ Error configurando GitHub: {e}")
            print("💡 Asegúrate de tener configurado GITHUB_TOKEN en tu .env")
    elif choice == "4":
        async with ServerManager.create_sequential_thinking_server() as server:
            agent = AgentFactory.create_sequential_thinking_agent([server])
            await interactive_chat(agent)
    elif choice == "5":
        async with ServerManager.create_fetch_server() as server:
            agent = AgentFactory.create_fetch_agent([server])
            await interactive_chat(agent)
    elif choice == "6":
        async with ServerManager.create_combined_servers() as (fs_server, pw_server):
            agent = AgentFactory.create_combined_agent([fs_server, pw_server])
            await interactive_chat(agent)
    else:
        print("❌ Selección inválida")


async def interactive_chat(agent):
    """Chat interactivo con el agente."""
    print("\n💬 Modo interactivo iniciado. Escribe 'quit' para salir.")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\n👤 Tu pregunta: ").strip()
            if user_input.lower() in ['quit', 'exit', 'salir']:
                break
            
            if not user_input:
                continue
                
            print("\n🤖 Respuesta:")
            print("-" * 40)
            result = await Runner.run(starting_agent=agent, input=user_input)
            print(result.final_output)
            print("-" * 40)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 ¡Hasta luego!")


def print_help():
    """Imprime ayuda sobre los comandos disponibles."""
    print("""
🚀 AI Foundry Agents Samples - Demos disponibles:

COMANDOS:
  filesystem    - Demo del sistema de archivos (leer/crear archivos)
                  • Leer archivos en sample_files/
                  • Crear nuevos archivos con código
                  • Analizar y sugerir mejoras
                  
  playwright    - Demo de automatización web con Playwright  
                  • Navegar páginas web
                  • Interactuar con elementos
                  • Tomar capturas de pantalla
                  
  github        - Demo de operaciones GitHub
                  • Gestión de repositorios
                  • Issues y Pull Requests
                  • Análisis de código y estadísticas
                  
  thinking      - Demo de pensamiento secuencial estructurado
                  • Análisis paso a paso de problemas complejos
                  • Razonamiento estructurado y revisable
                  • Planificación sistemática de soluciones
                  
  fetch         - Demo de operaciones HTTP/REST API
                  • Realizar llamadas HTTP GET
                  • Procesar respuestas JSON, HTML, XML
                  • Extraer información de páginas web
                  • Trabajar con APIs REST
                  
  combined      - Demo combinado (filesystem + web)
                  • Combina capacidades de archivos y web
                  • Flujos de trabajo más complejos
                  
  tools         - Inspección de herramientas disponibles
                  • Lista todas las herramientas disponibles
                  • Describe capacidades de cada una
                  
  interactive   - Modo interactivo para preguntas personalizadas
                  • Chat directo con el agente
                  • Selección de tipo de servidor
                  • Modo conversacional
                  
  help          - Muestra esta ayuda

EJEMPLOS:
  uv run python run_demos.py filesystem     # Demo seguro de archivos
  uv run python run_demos.py playwright     # Demo de automatización web
  uv run python run_demos.py github         # Demo de operaciones GitHub
  uv run python run_demos.py thinking       # Demo de pensamiento estructurado
  uv run python run_demos.py fetch          # Demo de operaciones HTTP/API
  uv run python run_demos.py combined       # Demo combinado
  uv run python run_demos.py interactive    # Modo conversacional

REQUISITOS:
  - Node.js y npm instalados (para npx)
  - Variables de entorno de Azure OpenAI configuradas
  - Archivo .env con las credenciales necesarias
  - GITHUB_TOKEN configurado para operaciones GitHub
    """)


async def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="AI Foundry Agents Samples - Demo Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "demo",
        nargs="?",
        choices=["filesystem", "playwright", "github", "thinking", "fetch", "combined", "tools", "interactive", "help"],
        help="Demo a ejecutar"
    )
    
    args = parser.parse_args()
    
    if args.demo is None or args.demo == "help":
        print_help()
        return
    
    try:
        print("🚀 AI Foundry Agents Samples")
        print("=" * 50)
        
        if args.demo == "filesystem":
            await run_filesystem_demo()
        elif args.demo == "playwright":
            await run_playwright_demo()
        elif args.demo == "github":
            await run_github_demo()
        elif args.demo == "thinking":
            await run_sequential_thinking_demo()
        elif args.demo == "fetch":
            await run_fetch_demo()
        elif args.demo == "combined":
            await run_combined_demo()
        elif args.demo == "tools":
            await run_tool_inspection()
        elif args.demo == "interactive":
            await run_interactive_mode()
            
        print("\n✅ Demo completado exitosamente")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())