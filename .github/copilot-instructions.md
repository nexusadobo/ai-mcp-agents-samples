# AI Foundry Agents Samples - Copilot Instructions

This is a **MCP (Model Context Protocol) AI agents framework** using Azure OpenAI with a modular, factory-based architecture.

## Architecture Overview

### Three-Layer System
1. **Server Layer** (`servers/server_manager.py`): Manages MCP server lifecycle via context managers
2. **Agent Layer** (`ai_agents/agent_factory.py`): Factory pattern for creating specialized AI agents  
3. **Execution Layer** (`run_demos.py`): Unified entry point with multiple demo modes

### Core Pattern: Context Manager + Factory
```python
# Standard workflow pattern used throughout
async with ServerManager.create_filesystem_server() as server:
    agent = AgentFactory.create_filesystem_agent([server])
    result = await Runner.run(starting_agent=agent, input="...")
```

## Key Components

### ServerManager (`servers/server_manager.py`)
- **Context managers** for MCP servers (filesystem, Playwright, GitHub, Sequential Thinking, Fetch, combined)
- **npx validation** - always checks Node.js availability first (except Fetch which uses uvx)
- **Fallback strategies** - Playwright has primary + alternative server configs
- **Environment validation** - GitHub server requires GITHUB_TOKEN
- Supports **filesystem**, **Playwright**, **GitHub**, **Sequential Thinking**, and **Fetch** servers

### AgentFactory (`ai_agents/agent_factory.py`)  
- **Factory methods** return pre-configured `Agent` instances with specialized instructions
- Agent types: **filesystem**, **web automation**, **GitHub operations**, **Sequential Thinking**, **HTTP/REST API (Fetch)**, **tool inspector**, **combined**
- All agents use centralized Azure OpenAI client from `utils.azure_client`
- **Tracing disabled by default** for cleaner output

### Azure Client Centralization (`utils/azure_client.py`)
- **Single source** for Azure OpenAI configuration across all scripts
- Environment validation with clear error messages
- Supports both function-based and class-based approaches

## Development Patterns

### Project Structure
- **Entry point**: `run_demos.py` (unified CLI with help system)
- **Individual tests**: `tests/` and `examples/` for standalone execution
- **Path handling**: Tests use `sys.path.append(str(Path(__file__).parent.parent))` for imports
- **Sample data**: Always in project root `sample_files/`, not test subdirectories

### Environment & Dependencies
- **UV package manager** - all commands use `uv run python`
- **Node.js required** - MCP servers run via `npx @modelcontextprotocol/server-*`
- **Azure OpenAI** - configured via `.env` with specific deployment names
- **GitHub Token** - GITHUB_TOKEN required for GitHub MCP Server operations

### Error Handling Conventions
- MCP connection errors trigger fallback server attempts (Playwright)
- Missing npx shows clear installation instructions
- Path resolution uses `Path(__file__).parent.parent` for cross-directory imports

## Critical Commands

```bash
# Primary workflow
uv run python run_demos.py help           # See all available demos
uv run python run_demos.py filesystem     # Safe file operations demo
uv run python run_demos.py github         # GitHub repository operations demo
uv run python run_demos.py thinking       # Sequential thinking structured analysis demo
uv run python run_demos.py fetch          # HTTP/REST API operations demo
uv run python run_demos.py interactive    # Multi-server selection mode

# Individual test execution  
uv run python tests/filesystem_test.py    # Direct test execution
uv run python examples/tool_inspection.py # Tool capability analysis
uv run python test_sequential_thinking.py # Sequential thinking server test
uv run python test_github.py             # GitHub MCP server test
uv run python test_playwright.py         # Playwright MCP server test
uv run python test_code_analysis.py      # GitHub code analysis test
uv run python test_fetch.py              # Fetch MCP server test
```

## MCP Integration Points

- **Filesystem Server**: `@modelcontextprotocol/server-filesystem` with sandboxed `sample_files/`
- **Playwright Server**: `@playwright/mcp@latest` with `@microsoft/playwright-mcp` fallback
- **GitHub Server**: `@skhatri/github-mcp` with GITHUB_TOKEN authentication
- **Sequential Thinking Server**: `@modelcontextprotocol/server-sequential-thinking` for structured analysis
- **Fetch Server**: `mcp-server-fetch` via uvx for HTTP/REST API operations
- **Combined Mode**: Runs multiple servers simultaneously with tuple return pattern

## Code Conventions

- **Async/await throughout** - all MCP operations are asynchronous
- **Mixed language convention** - docstrings and print statements in Spanish, but agent instructions and user interfaces in English
- **Factory + Context Manager** - standard combination for agent creation
- **Path-safe imports** - all subdirectory scripts handle parent directory imports