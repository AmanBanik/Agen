# Agen V2 🚀
**Autonomous AI Engineering CLI**

Agen V2 is a terminal-native, highly capable autonomous AI coding assistant. It uses a LangChain ReAct loop under the hood to write code, execute commands, run tools natively on your machine, and spawn swarm agents to complete complex software engineering tasks.

## 🌟 Key Features

*   **Multi-Agent Swarm Architecture:** Agen can use the invoke_subagent tool to spawn independent, asynchronous clones of itself in the background to handle multi-tasking (e.g., monitoring a server while simultaneously writing a frontend).
*   **Interactive REPL UI:** Built with prompt_toolkit and ich. Includes native / commands and intelligent @ file/folder attachment parsing without relying on slow shell commands.
*   **Model Context Protocol (MCP):** Connects to any standard MCP server (Tavily, GitHub, Puppeteer, Postgres, Docker) to dynamically load new tool capabilities on the fly.
*   **RAG Semantic Memory:** Use the /index command to chunk and embed your entire codebase into a local ChromaDB vector database. The agent will automatically recall relevant snippets from your codebase during conversations!
*   **Multi-Provider Support:** Switch between Cloud mode (Google Gemini) and Local execution mode (Ollama Llama3/Gemma) instantly via /gemini or /ollama commands.

## 📦 Installation & Setup

You can install Agen directly via Python, or use the pre-compiled standalone executable.

### Method 1: Python Package (Global CLI)
For developers who want to run the python source code natively.
\\\ash
# For Windows
setup.bat

# For macOS / Linux
chmod +x install.sh
./install.sh
\\\
*This installs Agen globally. You can now launch it anywhere by typing \gen\ in your terminal.*

### Method 2: Standalone Executable (Windows)
If you don't want to deal with Python environments, Agen is compiled into a portable executable using PyInstaller.
1. Run uild_exe.bat to compile the app.
2. Navigate to the dist/ folder and double click gen.exe. 

## 🛠️ Usage

Simply type \gen\ in your terminal to boot up the interactive UI.

**Commands:**
*   /help - Show the interactive help menu.
*   /index <dir> - Generate vector embeddings of your project for semantic memory.
*   /skill pull <github_url> - Clone a community AI workflow skill into your local .agent_skills directory.
*   /ollama - Switch the agent to use local hardware via Ollama.
*   /gemini - Switch the agent to use cloud APIs.
*   /clear - Clear the terminal interface.
*   /exit - Quit the CLI.

**File Attachments:**
Use the @ symbol anywhere in your prompt to attach files or entire directories. For example:
\> agen> Can you refactor the code inside @backend/agent.py ?\

## ⚙️ Configuration
Make sure you set your Gemini API key before using Cloud mode!
\\\ash
agen key "YOUR_GEMINI_API_KEY"
\\\

## 🏗️ CI/CD & Contribution
This repository comes packed with a GitHub Actions CI pipeline that automatically tests the backend Swarm orchestration engine and verifies that the \gen.exe\ PyInstaller build succeeds on every PR.
