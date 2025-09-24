# AI Foundry Agents Samples

Una colección organizada de ejemplos y demos para trabajar con AI Agents y MCP (Model Context Protocol) usando Azure OpenAI.

## 📁 Estructura del Proyecto

```### 🔍 Inspección de Herramientas
- Listar todas las herramientas disponibles
- Describir capacidades de cada herramientary-agents-samples/
├── ai_agents/                  # Configuración de agentes AI
│   ├── __init__.py
│   └── agent_factory.py       # Factory para crear agentes especializados
├── servers/                    # Configuración de servidores MCP
│   ├── __init__.py
│   └── server_manager.py      # Manager para servidores MCP
├── tests/                      # Pruebas y demos específicos
│   ├── __init__.py
│   ├── filesystem_test.py     # Demo de sistema de archivos
│   ├── playwright_test.py     # Demo de Playwright
│   └── combined_test.py       # Demo combinado
├── examples/                   # Ejemplos de uso
│   ├── __init__.py
│   ├── basic_usage.py        # Ejemplos básicos del cliente Azure
│   └── tool_inspection.py    # Inspección de herramientas
├── utils/                      # Utilidades compartidas
│   ├── __init__.py
│   └── azure_client.py       # Cliente de Azure OpenAI
├── sample_files/              # Archivos de ejemplo para demos
├── run_demos.py              # Script principal unificado
├── pyproject.toml
└── README.md
```

## 🚀 Inicio Rápido

### Prerrequisitos

1. **Node.js y npm** instalados (para MCP servers)
2. **Python 3.8+** 
3. **Azure OpenAI** configurado

### Configuración

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd ai-foundry-agents-samples
```

2. **Instalar dependencias con UV:**
```bash
# Instalar dependencias del proyecto
uv sync

# O instalar UV si no lo tienes
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Configurar variables de entorno:**
Crea un archivo `.env` con:
```env
AZURE_OPENAI_API_KEY=tu_api_key
AZURE_OPENAI_API_VERSION=2024-06-01
AZURE_OPENAI_ENDPOINT=https://tu-recurso.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4
```

### Uso del Script Principal

El proyecto incluye un script unificado `run_demos.py` que te permite ejecutar diferentes demos fácilmente:

```bash
# Ver ayuda
uv run python run_demos.py help

# Ejecutar demo de sistema de archivos
uv run python run_demos.py filesystem

# Ejecutar demo de Playwright (automatización web)
uv run python run_demos.py playwright

# Ejecutar demo combinado (filesystem + web)
uv run python run_demos.py combined

# Inspeccionar herramientas disponibles
uv run python run_demos.py tools

# Modo interactivo para preguntas personalizadas
uv run python run_demos.py interactive
```

## 📚 Componentes Principales

### 🤖 Agent Factory (`ai_agents/agent_factory.py`)

Factory centralizado para crear diferentes tipos de agentes especializados:

- **`create_filesystem_agent()`** - Especializado en operaciones de archivos
- **`create_web_automation_agent()`** - Para automatización web con Playwright
- **`create_tool_inspector_agent()`** - Para inspeccionar herramientas disponibles
- **`create_combined_agent()`** - Combina capacidades de archivos y web

### 🖥️ Server Manager (`servers/server_manager.py`)

Gestor centralizado para servidores MCP con context managers:

- **`create_filesystem_server()`** - Servidor para operaciones de archivos
- **`create_playwright_server()`** - Servidor para automatización web
- **`create_combined_servers()`** - Múltiples servidores simultáneos

### 🔧 Azure Client (`utils/azure_client.py`)

Utilidades para Azure OpenAI:

- **`get_azure_openai_client()`** - Cliente configurado
- **`get_chat_deployment_name()`** - Nombre del deployment
- **`AzureOpenAIConfig`** - Clase para configuración avanzada

## 💡 Ejemplos de Uso

### Uso Básico

```python
from agents.agent_factory import AgentFactory
from servers.server_manager import ServerManager
from agents import Runner

async def ejemplo_basico():
    async with ServerManager.create_filesystem_server() as server:
        agent = AgentFactory.create_filesystem_agent([server])
        
        result = await Runner.run(
            starting_agent=agent,
            input="List the files in the sample_files directory"
        )
        print(result.final_output)
```

### Uso con Comandos del Sistema

```python
from ai_agents.agent_factory import AgentFactory
from servers.server_manager import ServerManager
from agents import Runner

async def ejemplo_basico():
    async with ServerManager.create_filesystem_server() as server:
        agent = AgentFactory.create_filesystem_agent([server])
        
        result = await Runner.run(
            starting_agent=agent,
            input="List the files in the sample_files directory"
        )
        print(result.final_output)
```

## 🧪 Ejecutar Tests Individuales

Si prefieres ejecutar tests específicos en lugar del script unificado:

```bash
# Test de sistema de archivos
uv run python tests/filesystem_test.py

# Test de Playwright
uv run python tests/playwright_test.py

# Test combinado
uv run python tests/combined_test.py

# Inspección de herramientas
uv run python examples/tool_inspection.py

# Ejemplos básicos del cliente Azure
uv run python examples/basic_usage.py
```

## 📋 Funcionalidades Disponibles

### 📁 Sistema de Archivos
- Leer archivos en el directorio `sample_files/`
- Crear nuevos archivos con código
- Analizar y sugerir mejoras de código
- Gestionar estructuras de archivos

### 🌐 Automatización Web (Playwright)
- Navegar a páginas web
- Interactuar con elementos (clicks, formularios)
- Tomar capturas de pantalla
- Extraer información de páginas
- Automatizar flujos de trabajo web

### �️ Comandos del Sistema (⚠️ Usar con precaución)
- Ejecutar comandos básicos del sistema (ls, pwd, cat, etc.)
- Navegar por el sistema de archivos
- Analizar logs y archivos del sistema
- Monitorear procesos y recursos
- **ADVERTENCIA**: Requiere confirmación explícita por seguridad

### 📝 Control de Versiones Git
- Verificar estado del repositorio
- Analizar historial de commits
- Revisar cambios y diferencias
- Gestionar branches y tags
- Obtener información de repositorios

### �🔍 Inspección de Herramientas
- Listar todas las herramientas disponibles
- Describir capacidades de cada herramienta
- Proporcionar ejemplos de uso
- Organizar herramientas por categorías

## 🐛 Solución de Problemas

### Error: "npx no está instalado"
```bash
# Instalar Node.js y npm
sudo apt update
sudo apt install nodejs npm
```

### Error de variables de entorno
Asegúrate de que tu archivo `.env` esté en la raíz del proyecto y contenga todas las variables necesarias.

### Error de conexión con Azure OpenAI
Verifica que:
- Las credenciales sean correctas
- El endpoint esté disponible
- El deployment name sea correcto

### Error de permisos con Shell Server
Si obtienes errores de permisos al usar comandos del sistema:
- Asegúrate de tener los permisos necesarios
- Ejecuta solo comandos seguros
- Confirma que entiendes los riesgos de seguridad

### Error con Git Server
## 🔧 Servidores MCP Adicionales Disponibles

Si quieres expandir las capacidades, estos son otros servidores MCP disponibles:

```bash
# Búsqueda web con Brave
@modelcontextprotocol/server-brave-search

# Base de datos SQLite
@modelcontextprotocol/server-sqlite  

# APIs REST genéricas
@modelcontextprotocol/server-fetch

# Integración con Slack
@modelcontextprotocol/server-slack

# Servidor de memoria persistente
@modelcontextprotocol/server-memory

# Procesamiento de PDFs
@modelcontextprotocol/server-pdf
```

## 🤝 Contribuir

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Sube la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Si tienes problemas o preguntas, por favor abre un [issue](https://github.com/your-repo/issues) en GitHub.
