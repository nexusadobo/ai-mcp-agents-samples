"""
Ejemplo de cómo usar el módulo utils.azure_client en otros scripts.
"""

import asyncio
import sys
from pathlib import Path

# Añadir el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.azure_client import get_azure_openai_client, get_chat_deployment_name, AzureOpenAIConfig
from agents import Agent, OpenAIChatCompletionsModel


# Ejemplo 1: Usando las funciones simples
async def example_with_functions():
    """Ejemplo usando las funciones get_azure_openai_client y get_chat_deployment_name."""
    print("🔧 Ejemplo 1: Usando funciones simples")
    
    try:
        # Obtener el cliente configurado
        client = get_azure_openai_client()
        deployment_name = get_chat_deployment_name()
        
        print(f"✅ Cliente creado exitosamente")
        print(f"✅ Deployment: {deployment_name}")
        
        # Crear un modelo para usar con agents
        model = OpenAIChatCompletionsModel(
            model=deployment_name,
            openai_client=client
        )
        print("✅ Modelo creado exitosamente")
        
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


# Ejemplo 2: Usando la clase AzureOpenAIConfig
async def example_with_class():
    """Ejemplo usando la clase AzureOpenAIConfig para más control."""
    print("\n🔧 Ejemplo 2: Usando la clase AzureOpenAIConfig")
    
    try:
        # Crear instancia de configuración
        config = AzureOpenAIConfig()
        
        print(f"✅ Configuración cargada:")
        print(f"   - Endpoint: {config.azure_endpoint}")
        print(f"   - API Version: {config.api_version}")
        print(f"   - Deployment: {config.chat_deployment_name}")
        
        # Obtener el cliente
        client = config.get_client()
        print("✅ Cliente creado exitosamente")
        
        # Crear un agente simple
        agent = Agent(
            name="Example Agent",
            instructions="You are a helpful assistant.",
            model=OpenAIChatCompletionsModel(
                model=config.chat_deployment_name,
                openai_client=client
            )
        )
        print("✅ Agente creado exitosamente")
        
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


# Ejemplo 3: Función reutilizable para crear agentes
def create_standard_agent(name: str, instructions: str) -> Agent:
    """
    Función helper para crear agentes con configuración estándar.
    
    Args:
        name: Nombre del agente
        instructions: Instrucciones para el agente
        
    Returns:
        Agent: Agente configurado y listo para usar
    """
    client = get_azure_openai_client()
    deployment_name = get_chat_deployment_name()
    
    return Agent(
        name=name,
        instructions=instructions,
        model=OpenAIChatCompletionsModel(
            model=deployment_name,
            openai_client=client
        )
    )


async def example_with_helper():
    """Ejemplo usando la función helper create_standard_agent."""
    print("\n🔧 Ejemplo 3: Usando función helper")
    
    try:
        # Crear diferentes agentes fácilmente
        web_agent = create_standard_agent(
            name="Web Agent",
            instructions="You are a web automation specialist."
        )
        
        data_agent = create_standard_agent(
            name="Data Agent", 
            instructions="You are a data analysis expert."
        )
        
        print("✅ Agentes creados exitosamente:")
        print(f"   - {web_agent.name}")
        print(f"   - {data_agent.name}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    """Ejecuta todos los ejemplos."""
    print("🚀 Ejemplos de uso del módulo azure_client\n")
    
    await example_with_functions()
    await example_with_class()
    await example_with_helper()
    
    print("\n✅ Todos los ejemplos completados")


if __name__ == "__main__":
    asyncio.run(main())