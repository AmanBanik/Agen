# Contributing to Agen

First off, thank you for considering contributing to Agen! 

Agen is transitioning from a standalone Python CLI into a **V3 Autonomous Swarm Architecture**. We are building a future where software engineers pair-program with asynchronous, stateful AI agents directly from their terminal.

This document outlines the guidelines for contributing to the repository.

---

## 🤖 The Autonomous Contributor Protocol

Unlike traditional repositories, Agen is designed to be maintained **by AI agents, for AI agents**. We heavily encourage you to use AI coding assistants (like Claude, Gemini, or Agen itself) to write your Pull Requests. 

To facilitate this, this repository contains a special `.agent/` directory.

### The `.agent/skills/` Framework
Before your AI agent touches any code, you **must** instruct it to read the `.agent/agent.md` file and the relevant skill files in `.agent/skills/`. 
These markdown files act as the "system prompt" for our repository. They define our strict engineering standards, such as:
*   **Workspace Security Boundaries:** How the agent is sandboxed to `os.getcwd()`.
*   **Cross-Platform Builds:** How to manage `pyinstaller` without bloating the `.exe`.
*   **Terminal UI:** How to use the `rich` and `prompt_toolkit` libraries.

If you are contributing a new architectural pattern, your first step should be updating or creating a skill in `.agent/skills/` so future autonomous agents understand your pattern.

---

## 🛠️ Local Development Setup

To test Agen locally and build upon the core engine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AmanBanik/Agen.git
   cd Agen
   ```

2. **Create an isolated virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the engine in editable mode:**
   ```bash
   pip install -e .
   ```
   *Note: This automatically installs all required dependencies (LangChain, ChromaDB, Rich, Typer, MCP).*

4. **Run the CLI:**
   ```bash
   agen
   ```

---

## 🧪 Testing Infrastructure (Coming Soon)

We are actively building out a dedicated `tests/` directory powered by `pytest`. 
Because Agen relies on a ReAct (Reason + Act) loop, testing edge cases (like MCP server timeouts, prompt injections, or workspace boundary escapes) is critical. 

When submitting a Pull Request, please ensure you:
1. Write isolated unit tests for any new `backend.tools` you add.
2. Verify that the agent successfully hits the `PermissionError` when attempting to escape the workspace directory.

*(To run tests locally, you will simply use the `pytest` command once the suite is fully merged.)*

---

## 🚀 Submitting a Pull Request

1. **Fork the repository** and create a new branch (`feat/your-feature-name` or `fix/issue-description`).
2. **Consult the Swarm:** Ensure your code aligns with the `.agent/skills/` architecture.
3. **Commit your changes:** Use clear, descriptive commit messages.
4. **Push to your fork** and submit a Pull Request to the `v2-stable` branch.

### Code of Conduct
By participating in this project, you agree to abide by our [Code of Conduct](./CODE_OF_CONDUCT.md). We expect all human and autonomous contributors to maintain a respectful, collaborative environment.
