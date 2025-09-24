"""
Server manager for MCP servers.
Centraliza la configuración y creación de diferentes tipos de servidores MCP.
"""

import os
import shutil
from typing import Dict, Any, Optional
from agents.mcp import MCPServerStdio
from contextlib import asynccontextmanager


class ServerConfig:
    """Configuración base para servidores MCP."""
    
    def __init__(self, name: str, command: str, args: list[str]):
        self.name = name
        self.command = command
        self.args = args


class ServerManager:
    """Gestor centralizado para servidores MCP."""
    
    @staticmethod
    def _check_npx_available():
        """Verifica que npx esté disponible."""
        if not shutil.which("npx"):
            raise RuntimeError("❌ ERROR: npx no está instalado. Se necesita Node.js y npm.")
        print("✅ npx encontrado")
    
    @staticmethod
    def get_filesystem_server_config(samples_dir: Optional[str] = None) -> ServerConfig:
        """
        Obtiene la configuración para el servidor filesystem.
        
        Args:
            samples_dir: Directorio de archivos de ejemplo. Si None, usa sample_files.
            
        Returns:
            ServerConfig: Configuración del servidor filesystem
        """
        if samples_dir is None:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            samples_dir = os.path.join(current_dir, "sample_files")
        
        return ServerConfig(
            name="Filesystem Server",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", samples_dir]
        )
    
    @staticmethod
    def get_playwright_server_config(headless: bool = True, browser: str = "chromium") -> ServerConfig:
        """
        Obtiene la configuración para el servidor Playwright.
        
        Args:
            headless: Si ejecutar en modo headless
            browser: Navegador a usar (chromium, firefox, webkit)
            
        Returns:
            ServerConfig: Configuración del servidor Playwright
        """
        args = ["-y", "@playwright/mcp@latest"]
        if headless:
            args.append("--headless")
        args.extend(["--browser", browser])
        
        return ServerConfig(
            name="Playwright Server",
            command="npx", 
            args=args
        )
    
    @staticmethod
    def get_github_server_config() -> ServerConfig:
        """
        Obtiene la configuración para el servidor GitHub.
        
        Returns:
            ServerConfig: Configuración del servidor GitHub
            
        Note:
            Requiere GITHUB_TOKEN en las variables de entorno
        """
        return ServerConfig(
            name="GitHub Server",
            command="npx",
            args=["-y", "@skhatri/github-mcp"]
        )
    
    @staticmethod
    def get_sequential_thinking_server_config() -> ServerConfig:
        """
        Obtiene la configuración para el servidor Sequential Thinking.
        
        Returns:
            ServerConfig: Configuración del servidor Sequential Thinking
            
        Note:
            Servidor oficial de MCP para pensamiento estructurado paso a paso
        """
        return ServerConfig(
            name="Sequential Thinking Server",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-sequential-thinking"]
        )
    
    @staticmethod
    def get_fetch_server_config() -> ServerConfig:
        """
        Obtiene la configuración para el servidor Fetch.
        
        Returns:
            ServerConfig: Configuración del servidor Fetch
            
        Note:
            Servidor oficial de MCP para realizar llamadas HTTP/REST API
        """
        return ServerConfig(
            name="Fetch Server",
            command="uvx",
            args=["mcp-server-fetch"]
        )
    
    @staticmethod
    def get_playwright_alternative_config() -> ServerConfig:
        """
        Obtiene la configuración alternativa para el servidor Playwright.
        
        Returns:
            ServerConfig: Configuración alternativa del servidor Playwright
        """
        return ServerConfig(
            name="Playwright Server Alt",
            command="npx",
            args=["-y", "@microsoft/playwright-mcp"]
        )
    
    @staticmethod
    @asynccontextmanager
    async def create_filesystem_server(samples_dir: Optional[str] = None):
        """
        Context manager para crear un servidor filesystem.
        
        Args:
            samples_dir: Directorio de archivos de ejemplo
            
        Yields:
            MCPServerStdio: Servidor filesystem configurado
        """
        ServerManager._check_npx_available()
        config = ServerManager.get_filesystem_server_config(samples_dir)
        
        async with MCPServerStdio(
            name=config.name,
            params={
                "command": config.command,
                "args": config.args,
            },
        ) as server:
            print(f"✅ {config.name} conectado exitosamente")
            yield server
    
    @staticmethod
    @asynccontextmanager
    async def create_playwright_server(headless: bool = True, browser: str = "chromium"):
        """
        Context manager para crear un servidor Playwright.
        
        Args:
            headless: Si ejecutar en modo headless
            browser: Navegador a usar
            
        Yields:
            MCPServerStdio: Servidor Playwright configurado
        """
        ServerManager._check_npx_available()
        config = ServerManager.get_playwright_server_config(headless, browser)
        
        try:
            async with MCPServerStdio(
                name=config.name,
                params={
                    "command": config.command,
                    "args": config.args,
                },
            ) as server:
                print(f"✅ {config.name} conectado exitosamente")
                yield server
                
        except Exception as e:
            print(f"❌ ERROR al conectar con {config.name}: {e}")
            print("🔄 Intentando con versión alternativa...")
            
            # Intentar con versión alternativa
            alt_config = ServerManager.get_playwright_alternative_config()
            try:
                async with MCPServerStdio(
                    name=alt_config.name,
                    params={
                        "command": alt_config.command,
                        "args": alt_config.args,
                    },
                ) as alt_server:
                    print(f"✅ {alt_config.name} conectado exitosamente")
                    yield alt_server
            except Exception as e2:
                print(f"❌ ERROR también con versión alternativa: {e2}")
                raise
    
    @staticmethod
    @asynccontextmanager
    async def create_github_server():
        """
        Context manager para crear un servidor GitHub.
        
        Yields:
            MCPServerStdio: Servidor GitHub configurado
            
        Note:
            Requiere GITHUB_TOKEN en las variables de entorno
        """
        import os
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise RuntimeError("❌ ERROR: GITHUB_TOKEN no está configurado en las variables de entorno.")
        
        ServerManager._check_npx_available()
        config = ServerManager.get_github_server_config()
        
        print("🔧 Conectando con GitHub MCP Server...")
        print("   Asegúrate de que el token tenga los permisos necesarios")
        
        async with MCPServerStdio(
            name=config.name,
            params={
                "command": config.command,
                "args": config.args,
                "env": {"GITHUB_TOKEN": github_token}
            },
        ) as server:
            print(f"✅ {config.name} conectado exitosamente")
            yield server

    @staticmethod
    @asynccontextmanager
    async def create_sequential_thinking_server():
        """
        Context manager para crear un servidor Sequential Thinking.
        
        Yields:
            MCPServerStdio: Servidor Sequential Thinking configurado
            
        Note:
            Servidor oficial de MCP para pensamiento estructurado paso a paso
        """
        ServerManager._check_npx_available()
        config = ServerManager.get_sequential_thinking_server_config()
        
        print("🧠 Conectando con Sequential Thinking MCP Server...")
        print("   Iniciando pensamiento estructurado paso a paso")
        
        async with MCPServerStdio(
            name=config.name,
            params={
                "command": config.command,
                "args": config.args,
            },
        ) as server:
            print(f"✅ {config.name} conectado exitosamente")
            yield server

    @staticmethod
    @asynccontextmanager
    async def create_fetch_server():
        """
        Context manager para crear un servidor Fetch.
        
        Yields:
            MCPServerStdio: Servidor Fetch configurado
            
        Note:
            Servidor oficial de MCP para realizar llamadas HTTP/REST API
        """
        # Nota: Fetch server usa uvx, no necesita verificar npx
        config = ServerManager.get_fetch_server_config()
        
        print("🌐 Conectando con Fetch MCP Server...")
        print("   Iniciando capacidades HTTP/REST API")
        
        async with MCPServerStdio(
            name=config.name,
            params={
                "command": config.command,
                "args": config.args,
            },
        ) as server:
            print(f"✅ {config.name} conectado exitosamente")
            yield server

    @staticmethod
    @asynccontextmanager 
    async def create_combined_servers(samples_dir: Optional[str] = None,
                                      headless: bool = True,
                                      browser: str = "chromium"):
        """
        Context manager para crear múltiples servidores MCP.
        
        Args:
            samples_dir: Directorio de archivos de ejemplo
            headless: Si ejecutar Playwright en modo headless
            browser: Navegador a usar en Playwright
            
        Yields:
            tuple: (filesystem_server, playwright_server)
        """
        ServerManager._check_npx_available()
        
        fs_config = ServerManager.get_filesystem_server_config(samples_dir)
        pw_config = ServerManager.get_playwright_server_config(headless, browser)
        
        async with MCPServerStdio(
            name=fs_config.name,
            params={
                "command": fs_config.command,
                "args": fs_config.args,
            },
        ) as filesystem_server, MCPServerStdio(
            name=pw_config.name,
            params={
                "command": pw_config.command,
                "args": pw_config.args,
            },
        ) as playwright_server:
            print(f"✅ {fs_config.name} y {pw_config.name} conectados exitosamente")
            yield filesystem_server, playwright_server