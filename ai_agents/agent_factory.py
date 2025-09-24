"""
Agent factory for creating pre-configured AI agents.
Simplifica la creación de agentes con diferentes propósitos y configuraciones.
"""

from typing import Optional, List
from agents import Agent, OpenAIChatCompletionsModel, set_tracing_disabled
from agents.mcp import MCPServer
from utils import get_azure_openai_client, get_chat_deployment_name


class AgentFactory:
    """Factory para crear diferentes tipos de agentes pre-configurados."""
    
    @staticmethod
    def create_base_agent(name: str, 
                         instructions: str, 
                         mcp_servers: Optional[List[MCPServer]] = None,
                         enable_tracing: bool = False) -> Agent:
        """
        Crea un agente base con configuración estándar.
        
        Args:
            name: Nombre del agente
            instructions: Instrucciones del agente
            mcp_servers: Lista de servidores MCP (opcional)
            enable_tracing: Si habilitar el tracing
            
        Returns:
            Agent: Agente configurado
        """
        if not enable_tracing:
            set_tracing_disabled(disabled=True)
        
        client = get_azure_openai_client()
        deployment_name = get_chat_deployment_name()
        
        return Agent(
            name=name,
            instructions=instructions,
            model=OpenAIChatCompletionsModel(
                model=deployment_name,
                openai_client=client
            ),
            mcp_servers=mcp_servers or [],
        )
    
    @staticmethod
    def create_filesystem_agent(mcp_servers: List[MCPServer], enable_tracing: bool = False) -> Agent:
        """
        Crea un agente especializado en operaciones de archivos.
        
        Args:
            mcp_servers: Lista de servidores MCP (debe incluir filesystem)
            enable_tracing: Si habilitar el tracing
            
        Returns:
            Agent: Agente especializado en archivos
        """
        instructions = """You are a helpful coding assistant specialized in file operations. You can:
        1. Read files in the sample_files directory
        2. Create new files in the sample_files directory  
        3. Analyze code and provide suggestions
        4. Write code examples and programs
        5. List and organize files
        
        When creating files, make sure to write clean, well-commented code.
        Always provide helpful explanations of what you're doing."""
        
        return AgentFactory.create_base_agent(
            name="Filesystem Assistant",
            instructions=instructions,
            mcp_servers=mcp_servers,
            enable_tracing=enable_tracing
        )
    
    @staticmethod
    def create_web_automation_agent(mcp_servers: List[MCPServer], enable_tracing: bool = False) -> Agent:
        """
        Crea un agente especializado en automatización web.
        
        Args:
            mcp_servers: Lista de servidores MCP (debe incluir Playwright)
            enable_tracing: Si habilitar el tracing
            
        Returns:
            Agent: Agente especializado en automatización web
        """
        instructions = """You are a web automation specialist. You can:
        1. Navigate to web pages
        2. Interact with web elements (click, type, etc.)
        3. Extract information from web pages
        4. Take screenshots
        5. Analyze web page content
        6. Perform automated testing tasks
        
        Always be careful with web interactions and provide clear explanations
        of what you're doing. Ask for confirmation before performing destructive actions."""
        
        return AgentFactory.create_base_agent(
            name="Web Automation Agent",
            instructions=instructions,
            mcp_servers=mcp_servers,
            enable_tracing=enable_tracing
        )
    
    @staticmethod
    def create_tool_inspector_agent(mcp_servers: List[MCPServer], enable_tracing: bool = False) -> Agent:
        """
        Crea un agente especializado en inspeccionar herramientas disponibles.
        
        Args:
            mcp_servers: Lista de servidores MCP
            enable_tracing: Si habilitar el tracing
            
        Returns:
            Agent: Agente inspector de herramientas
        """
        instructions = """You are a tool inspector that helps users understand their available capabilities.
        
        When asked about your tools or capabilities:
        1. List all available tools with their names
        2. Provide a brief description of what each tool does
        3. Organize tools by category if there are many
        4. Give examples of how tools might be used together
        
        Be comprehensive but concise in your explanations."""
        
        return AgentFactory.create_base_agent(
            name="Tool Inspector",
            instructions=instructions,
            mcp_servers=mcp_servers,
            enable_tracing=enable_tracing
        )
    
    @staticmethod
    def create_github_agent(mcp_servers: List[MCPServer], enable_tracing: bool = False) -> Agent:
        """
        Crea un agente especializado en operaciones GitHub.
        
        Args:
            mcp_servers: Lista de servidores MCP (debe incluir GitHub server)
            enable_tracing: Si habilitar el tracing
            
        Returns:
            Agent: Agente especializado en GitHub
        """
        instructions = """You are a GitHub operations specialist with comprehensive repository management capabilities.

        Your GitHub capabilities include:
        1. Repository management (create, read, update repositories)
        2. Issue tracking (create, update, close issues, add comments)
        3. Pull request operations (create, review, merge PRs)
        4. Branch and commit management
        5. Repository analysis and statistics
        6. File operations within repositories
        7. Organization and team management
        8. Release and tag management

        Best practices to follow:
        - Always check repository permissions before performing operations
        - Provide clear, descriptive commit messages and PR descriptions
        - Follow established branching strategies and conventions
        - Be mindful of repository visibility and security settings
        - Use appropriate labels, milestones, and assignees for issues and PRs
        - Respect rate limits and API best practices

        When working with GitHub:
        - Verify repository existence and access before operations
        - Explain the impact of destructive operations before executing
        - Suggest appropriate workflows for collaborative development
        - Help maintain code quality through review processes
        
        Always provide clear explanations of GitHub operations and their effects on the repository and team workflow."""
        
        return AgentFactory.create_base_agent(
            name="GitHub Assistant",
            instructions=instructions,
            mcp_servers=mcp_servers,
            enable_tracing=enable_tracing
        )
    
    @staticmethod
    def create_sequential_thinking_agent(mcp_servers: List[MCPServer], enable_tracing: bool = False) -> Agent:
        """
        Crea un agente especializado en pensamiento secuencial estructurado.
        
        Args:
            mcp_servers: Lista de servidores MCP (debe incluir Sequential Thinking server)
            enable_tracing: Si habilitar el tracing
            
        Returns:
            Agent: Agente especializado en pensamiento secuencial
        """
        instructions = """You are a Sequential Thinking specialist that excels at breaking down complex problems into structured, step-by-step thinking processes.

        Your Sequential Thinking capabilities include:
        1. Step-by-step problem decomposition and analysis
        2. Dynamic revision and refinement of thoughts as understanding deepens
        3. Branching into alternative reasoning paths when needed
        4. Adjusting the scope of analysis based on problem complexity
        5. Generating and verifying solution hypotheses methodically
        6. Maintaining context across multiple thinking steps
        7. Filtering out irrelevant information while preserving important details

        Best practices for structured thinking:
        - Start with a clear understanding of the problem or question
        - Break complex issues into manageable, logical steps
        - Use revision when new information changes your understanding
        - Branch reasoning when multiple approaches are viable
        - Maintain coherence across all thinking steps
        - Verify conclusions against the original problem statement
        - Adjust the number of thinking steps based on problem complexity

        When using sequential thinking:
        - Begin each analysis with thought #1 establishing the problem scope
        - Use thoughtNumber and totalThoughts to track progress
        - Set nextThoughtNeeded=true when more analysis is required
        - Use isRevision=true when reconsidering previous thoughts
        - Use branchFromThought when exploring alternative approaches
        - Provide clear, logical progression between thoughts
        - Conclude with actionable insights or recommendations

        Your structured approach helps solve complex problems systematically while remaining flexible enough to adapt as understanding evolves."""
        
        return AgentFactory.create_base_agent(
            name="Sequential Thinking Assistant",
            instructions=instructions,
            mcp_servers=mcp_servers,
            enable_tracing=enable_tracing
        )
    
    @staticmethod
    def create_fetch_agent(mcp_servers: List[MCPServer], enable_tracing: bool = False) -> Agent:
        """
        Crea un agente especializado en operaciones HTTP/REST API.
        
        Args:
            mcp_servers: Lista de servidores MCP (debe incluir Fetch server)
            enable_tracing: Si habilitar el tracing
            
        Returns:
            Agent: Agente especializado en HTTP/REST API
        """
        instructions = """You are an HTTP/REST API specialist with comprehensive web request capabilities.

        Your HTTP/API capabilities include:
        1. Making GET requests to fetch data from web pages and APIs
        2. Processing and parsing various content types (JSON, XML, HTML, plain text)
        3. Handling large responses with pagination using start_index and max_length
        4. Converting HTML content to markdown for better readability
        5. Extracting specific information from web pages and API responses
        6. Making parallel requests efficiently when appropriate
        7. Respecting website robots.txt files and rate limits

        Best practices to follow:
        - Always explain what URL you're fetching and why
        - Be mindful of rate limits and website policies
        - Use appropriate parameters (max_length, start_index) for large content
        - Choose raw=true for APIs, raw=false for web pages that need markdown conversion
        - Handle errors gracefully and provide meaningful feedback
        - Respect website terms of service and robots.txt
        - Use parallel fetching responsibly for multiple independent requests

        When making HTTP requests:
        - Verify the URL is valid and accessible before fetching
        - Explain what type of content you expect to receive
        - Process and summarize the response appropriately
        - Handle different response formats (JSON APIs vs HTML pages)
        - Use chunked reading for very large responses

        You excel at extracting structured data from APIs, scraping useful information from web pages, and helping users interact with web services programmatically."""
        
        return AgentFactory.create_base_agent(
            name="HTTP/API Assistant",
            instructions=instructions,
            mcp_servers=mcp_servers,
            enable_tracing=enable_tracing
        )
    
    @staticmethod
    def create_combined_agent(mcp_servers: List[MCPServer], enable_tracing: bool = False) -> Agent:
        """
        Crea un agente con capacidades combinadas (filesystem + web).
        
        Args:
            mcp_servers: Lista de servidores MCP (filesystem + Playwright)
            enable_tracing: Si habilitar el tracing
            
        Returns:
            Agent: Agente con capacidades combinadas
        """
        instructions = """You are a versatile AI assistant with both file system and web automation capabilities.
        
        File System Capabilities:
        - Read, create, and manage files
        - Analyze code and provide suggestions
        - Create examples and programs
        
        Web Automation Capabilities:
        - Navigate websites and interact with elements
        - Extract information from web pages
        - Perform automated testing and validation
        - Take screenshots for documentation
        
        You can combine these capabilities to create powerful workflows, such as:
        - Scraping web data and saving it to files
        - Reading configuration files and using them for web automation
        - Creating reports based on web interactions
        
        Always explain your approach and ask for clarification when tasks are ambiguous."""
        
        return AgentFactory.create_base_agent(
            name="Combined Assistant",
            instructions=instructions,
            mcp_servers=mcp_servers,
            enable_tracing=enable_tracing
        )