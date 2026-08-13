<div align="center">

```text
      ▄▄████▄▄      
    ▄██████████▄    
   ████▀▀  ▀▀████   
  ████        ████  
 ██████████████████ 
█████▀▀▀▀▀▀▀▀▀▀█████
████            ████
███              ███
```

# 🚀 Agen V2
**The Autonomous AI Engineering CLI**

[![CI Status](https://github.com/AmanBanik/Agen/actions/workflows/ci.yml/badge.svg)](https://github.com/AmanBanik/Agen/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/AmanBanik/Agen/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-green.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Agen is a terminal-native, highly capable autonomous AI coding assistant. It uses a LangChain ReAct loop under the hood to write code, execute commands, run tools natively on your machine, and spawn swarm agents to complete complex software engineering tasks.

[View Releases](https://github.com/AmanBanik/Agen/releases) • [Report Bug](https://github.com/AmanBanik/Agen/issues) • [Request Feature](https://github.com/AmanBanik/Agen/issues)

</div>

---

## ✨ Key Features

* 🧠 **Multi-Agent Swarm Architecture:** Agen can use the `invoke_subagent` tool to spawn independent, asynchronous clones of itself in the background to handle multi-tasking (e.g., monitoring a server while simultaneously writing a frontend).
* 🖥️ **Interactive REPL UI:** Built with `prompt_toolkit` and `rich`. Includes native `/` commands and intelligent `@` file/folder attachment parsing without relying on slow shell commands.
* 🔌 **Model Context Protocol (MCP):** Connects to any standard MCP server (Tavily, GitHub, Puppeteer, Postgres, Docker) to dynamically load new tool capabilities on the fly.
* 📚 **RAG Semantic Memory:** Use the `/index` command to chunk and embed your entire codebase into a local ChromaDB vector database. The agent will automatically recall relevant snippets from your codebase during conversations!
* ☁️ **Multi-Provider Support:** Switch between Cloud mode (Google Gemini) and Local execution mode (Ollama Llama3/Gemma) instantly via `/gemini` or `/ollama` commands.

---

## 📦 Installation & Setup

### Option 1: Standalone Windows Executable (Recommended)
You do not need Python installed. Download and run the standalone binary directly from GitHub.

**Via PowerShell (Fastest):**
```powershell
irm https://github.com/AmanBanik/Agen/releases/download/v2.0.0/agen.exe -OutFile agen.exe
.\agen.exe
```

**Via Browser:**
1. Go to the [Releases Page](https://github.com/AmanBanik/Agen/releases/latest).
2. Download `agen.exe`.
3. Double-click to run!

---

### Option 2: Build from Source (Global CLI)
For developers who want to run the python source code natively across Linux, macOS, or Windows.

```bash
# 1. Clone the repository
git clone https://github.com/AmanBanik/Agen.git
cd Agen

# 2. Run the platform-specific installer
# For Windows:
setup.bat

# For macOS / Linux:
chmod +x install.sh
./install.sh
```
*This installs Agen globally via pip. You can now launch it anywhere by typing `agen` in your terminal.*

---

## 🛠️ Usage & Commands

Simply type `agen` (or run `agen.exe`) in your terminal to boot up the interactive UI.

### In-Chat Commands
* `/help` - Show the interactive help menu.
* `/index <dir>` - Generate vector embeddings of your project for semantic memory.
* `/skill pull <github_url>` - Clone a community AI workflow skill into your local `.agent_skills` directory.
* `/ollama` - Switch the agent to use local hardware via Ollama.
* `/gemini` - Switch the agent to use cloud APIs.
* `/clear` - Clear the terminal interface.
* `/exit` - Quit the CLI.

### File Attachments
Use the `@` symbol anywhere in your prompt to attach files or entire directories instantly.
> `agen> Can you refactor the code inside @backend/agent.py ?`

---

## ⚙️ Configuration
If you are using Cloud Mode (Gemini), make sure you set your API key before chatting:
```bash
agen key "YOUR_GEMINI_API_KEY"
```

## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create.
This repository comes packed with a GitHub Actions CI pipeline that automatically tests the backend Swarm orchestration engine and verifies that the `agen.exe` PyInstaller build succeeds on every PR. 

Please review our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.
