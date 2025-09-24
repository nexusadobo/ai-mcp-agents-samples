"""Utils package for shared utilities."""
from .azure_client import get_azure_openai_client, get_chat_deployment_name, AzureOpenAIConfig

__all__ = [
    "get_azure_openai_client",
    "get_chat_deployment_name", 
    "AzureOpenAIConfig",
]