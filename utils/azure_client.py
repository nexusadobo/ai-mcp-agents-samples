"""
Módulo para inicializar y gestionar el cliente de Azure OpenAI.
Centraliza la configuración para poder reutilizar en todos los scripts.
"""

import os
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI


def get_azure_openai_client():
    """
    Inicializa y retorna un cliente de Azure OpenAI configurado.
    
    Carga las variables de entorno necesarias desde un archivo .env
    y crea una instancia de AsyncAzureOpenAI configurada.
    
    Returns:
        AsyncAzureOpenAI: Cliente configurado de Azure OpenAI
        
    Raises:
        ValueError: Si falta alguna variable de entorno requerida
    """
    load_dotenv()
    
    # Verificar que las variables de entorno estén presentes
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    if not api_key:
        raise ValueError("AZURE_OPENAI_API_KEY no está definida en las variables de entorno")
    if not api_version:
        raise ValueError("AZURE_OPENAI_API_VERSION no está definida en las variables de entorno")
    if not azure_endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT no está definida en las variables de entorno")
    
    return AsyncAzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint,
    )


def get_chat_deployment_name():
    """
    Obtiene el nombre del deployment del modelo de chat desde variables de entorno.
    
    Returns:
        str: Nombre del deployment del modelo de chat
        
    Raises:
        ValueError: Si la variable de entorno no está definida
    """
    load_dotenv()
    
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    if not deployment_name:
        raise ValueError("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME no está definida en las variables de entorno")
    
    return deployment_name


class AzureOpenAIConfig:
    """
    Clase para gestionar la configuración de Azure OpenAI de forma más estructurada.
    Útil para casos donde necesites más control sobre la configuración.
    """
    
    def __init__(self):
        """Inicializa la configuración cargando las variables de entorno."""
        load_dotenv()
        self._validate_environment()
    
    def _validate_environment(self):
        """Valida que todas las variables de entorno necesarias estén presentes."""
        required_vars = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_API_VERSION", 
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Variables de entorno faltantes: {', '.join(missing_vars)}")
    
    @property
    def api_key(self):
        """Retorna la API key de Azure OpenAI."""
        return os.getenv("AZURE_OPENAI_API_KEY")
    
    @property
    def api_version(self):
        """Retorna la versión de la API de Azure OpenAI."""
        return os.getenv("AZURE_OPENAI_API_VERSION")
    
    @property
    def azure_endpoint(self):
        """Retorna el endpoint de Azure OpenAI."""
        return os.getenv("AZURE_OPENAI_ENDPOINT")
    
    @property
    def chat_deployment_name(self):
        """Retorna el nombre del deployment del modelo de chat."""
        return os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    
    def get_client(self):
        """
        Crea y retorna un cliente de Azure OpenAI configurado.
        
        Returns:
            AsyncAzureOpenAI: Cliente configurado de Azure OpenAI
        """
        return AsyncAzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.azure_endpoint,
        )