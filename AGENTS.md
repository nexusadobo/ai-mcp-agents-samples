# AGENTS.md - AI Foundry Agents Samples

## Build/Lint/Test Commands
- **Run single test**: `uv run python tests/<test_name>.py`
- **Run demo**: `uv run python run_demos.py <mode>` (filesystem, github, thinking, fetch, playwright, combined, interactive, tools)
- **Install deps**: `uv sync`
- **No linting/formatting tools configured** - follow existing code style

## Code Style Guidelines

### Imports & Structure
- **Import order**: Standard library → Third-party → Local modules
- **Path-safe imports**: Use `sys.path.append(str(Path(__file__).parent.parent))` in subdirectory scripts
- **Type hints**: Use `typing` module for all function parameters and return types

### Naming Conventions
- **Functions/variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_CASE`
- **Private methods**: `_leading_underscore`

### Language Convention
- **Docstrings/comments**: Spanish (descriptive, clear explanations)
- **Agent instructions/UI**: English (technical, user-facing)
- **Error messages**: Spanish with clear context

### Async/Await Patterns
- **All MCP operations**: Use `async/await` throughout
- **Context managers**: Standard pattern for server lifecycle
- **Factory + Context Manager**: Core pattern for agent creation

### Error Handling
- **Clear error messages**: Include context and actionable guidance
- **Validation**: Check prerequisites (npx, environment variables) early
- **Fallback strategies**: Implement alternatives for MCP server failures

### Security & Best Practices
- **No secrets in code**: Use environment variables for all credentials
- **Sandboxing**: File operations limited to `sample_files/` directory
- **Tracing**: Disabled by default for cleaner output

## Copilot Instructions
See `.github/copilot-instructions.md` for detailed architecture overview, development patterns, and MCP integration points.