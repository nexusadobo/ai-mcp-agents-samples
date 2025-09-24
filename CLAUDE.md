# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a **Model Context Protocol (MCP) AI agents framework** using Azure OpenAI with a modular, factory-based architecture that enables specialized AI agents to work with different tools and capabilities.

### Three-Layer System
1. **Server Layer** (`servers/server_manager.py`): Manages MCP server lifecycle via context managers
2. **Agent Layer** (`ai_agents/agent_factory.py`): Factory pattern for creating specialized AI agents
3. **Execution Layer** (`run_demos.py`): Unified entry point with multiple demo modes

### Core Pattern: Context Manager + Factory
```python
# Standard workflow pattern used throughout the codebase
async with ServerManager.create_filesystem_server() as server:
    agent = AgentFactory.create_filesystem_agent([server])
    result = await Runner.run(starting_agent=agent, input="...")
```

## Key Components

### ServerManager (`servers/server_manager.py`)
- Provides context managers for MCP servers: **filesystem**, **Playwright**, **GitHub**, **Sequential Thinking**, **Fetch**, and **combined**
- Always checks Node.js/npx availability first (except Fetch server which uses uvx)
- Implements fallback strategies (Playwright has primary + alternative server configs)
- Validates environment variables (GitHub server requires GITHUB_TOKEN)

### AgentFactory (`ai_agents/agent_factory.py`)
- Factory methods return pre-configured `Agent` instances with specialized instructions
- Available agent types: `filesystem`, `web_automation`, `github`, `sequential_thinking`, `fetch`, `tool_inspector`, `combined`
- All agents use centralized Azure OpenAI client from `utils.azure_client`
- Tracing disabled by default for cleaner output

### Azure Client (`utils/azure_client.py`)
- Single source for Azure OpenAI configuration across all scripts
- Environment validation with clear error messages
- Supports both function-based (`get_azure_openai_client()`) and class-based (`AzureOpenAIConfig`) approaches

## Essential Commands

### Primary Development Workflow
```bash
# Main entry point - see all available demos
uv run python run_demos.py help

# Core demos
uv run python run_demos.py filesystem     # File operations with sample_files/
uv run python run_demos.py github         # GitHub repository operations
uv run python run_demos.py thinking       # Sequential structured analysis
uv run python run_demos.py fetch          # HTTP/REST API operations
uv run python run_demos.py playwright     # Web automation (requires browser setup)
uv run python run_demos.py combined       # Multiple capabilities
uv run python run_demos.py interactive    # Multi-server selection mode
uv run python run_demos.py tools          # Tool inspection
```

### Individual Test Execution
```bash
# Direct test execution bypassing main script
uv run python tests/filesystem_test.py
uv run python tests/playwright_test.py
uv run python tests/combined_test.py
uv run python examples/tool_inspection.py
uv run python examples/basic_usage.py

# Additional test files in tests/ directory
uv run python tests/test_sequential_thinking.py
uv run python tests/test_github.py
uv run python tests/test_code_analysis.py
uv run python tests/test_fetch.py
uv run python tests/test_fetch_basic.py
uv run python tests/test_playwright.py
```

### Package Management
```bash
# Install dependencies using UV
uv sync

# Install UV if needed
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Environment Configuration

Required `.env` variables:
```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_API_VERSION=2024-06-01
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4
GITHUB_TOKEN=your_token  # Required only for GitHub operations
```

## MCP Server Integration

- **Filesystem Server**: `@modelcontextprotocol/server-filesystem` sandboxed to `sample_files/`
- **Playwright Server**: `@playwright/mcp@latest` with `@microsoft/playwright-mcp` fallback
- **GitHub Server**: `@skhatri/github-mcp` with GITHUB_TOKEN authentication
- **Sequential Thinking Server**: `@modelcontextprotocol/server-sequential-thinking`
- **Fetch Server**: `mcp-server-fetch` via uvx (Python-based, not Node.js)

## Development Patterns

### Project Structure
- **Entry point**: `run_demos.py` serves as unified CLI with help system
- **Test organization**: Both `tests/` and `examples/` directories plus root-level test files
- **Path handling**: Subdirectory scripts use `sys.path.append(str(Path(__file__).parent.parent))` for imports
- **Sample data**: Always stored in project root `sample_files/` directory

### Code Conventions
- **Async/await throughout**: All MCP operations are asynchronous
- **Mixed language**: Docstrings and print statements in Spanish, agent instructions and UI in English
- **Standard pattern**: Factory + Context Manager combination for agent creation
- **Path-safe imports**: All subdirectory scripts handle parent directory imports correctly

### Error Handling
- MCP connection errors trigger fallback server attempts (especially for Playwright)
- Missing npx shows clear Node.js installation instructions
- Environment variable validation provides specific missing variable names
- Path resolution uses `Path(__file__).parent.parent` for cross-directory imports

## Prerequisites

1. **Python 3.12+** with UV package manager
2. **Node.js and npm** for MCP servers (except Fetch server)
3. **Azure OpenAI** configured with proper deployment
4. **GitHub Token** for GitHub operations (optional)