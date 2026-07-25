import typer
import httpx
from typing import Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel
import os
import shutil
import subprocess
import base64
import json
import re
from rich.theme import Theme

stealth_theme = Theme({
    "info": "bold #00ffff",        # neon cyan
    "warning": "bold yellow",
    "error": "bold red",
    "status": "bold #5d3fd3",      # deep purple
})
app = typer.Typer(help="Terminal Agent CLI", no_args_is_help=False)
console = Console(theme=stealth_theme)

@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context):
    """Terminal Agent CLI - AI Assistant for Data Science and Hardware-Accelerated Computing."""
    if ctx.invoked_subcommand is None:
        interactive_repl()

def load_system_context():
    skills_dir = ".agent_skills"
    context = ""
    if os.path.exists(skills_dir):
        for filename in os.listdir(skills_dir):
            if filename.endswith(".md") or filename.endswith(".txt"):
                try:
                    with open(os.path.join(skills_dir, filename), "r", encoding="utf-8") as f:
                        context += f"--- Context from {filename} ---\n{f.read()}\n\n"
                except Exception:
                    pass
    return context

BACKEND_URL = "http://localhost:8000"
SKILLS_LIBRARY_DIR = os.path.join(os.path.dirname(__file__), "skills_library")
MCP_CONFIG_FILE = ".agent_mcp.json"

def load_mcp_servers():
    if os.path.exists(MCP_CONFIG_FILE):
        try:
            with open(MCP_CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("servers", [])
        except Exception:
            return []
    return []

def save_mcp_servers(servers: list[str]):
    with open(MCP_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"servers": sorted(list(set(servers)))}, f, indent=2)

LOCAL_CONFIG_FILE = ".agent_local.json"

def load_local_config():
    if os.path.exists(LOCAL_CONFIG_FILE):
        try:
            with open(LOCAL_CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_local_config(provider: str, model: str):
    with open(LOCAL_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"provider": provider, "model": model}, f, indent=2)

def expand_file_references(prompt: str) -> str:
    """Parses @filepath syntax and embeds file contents into the prompt"""
    def replace_match(match):
        filepath = match.group(1).strip()
        if os.path.exists(filepath) and os.path.isfile(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                return f"\n--- Included File: {filepath} ---\n{content}\n--- End of {filepath} ---\n"
            except Exception as e:
                return f"[Error reading file {filepath}: {e}]"
        return match.group(0)

    # Match @filepath (supporting relative and absolute paths, e.g. @client/cli.py or @main.py)
    expanded = re.sub(r'@([a-zA-Z0-9_\-\./\\]+)', replace_match, prompt)
    return expanded

@app.command()
def init(
    list_skills: bool = typer.Option(False, "--list", "-l", help="List all available predefined skills in the library"),
    add: Optional[list[str]] = typer.Option(None, "--add", "-a", help="Specific skill names to install from the library"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p", help="Install a skill profile: 'ds' (Data Science), 'dev' (Engineering), or 'all'"),
    all_skills: bool = typer.Option(False, "--all", help="Install all available skills from the library")
):
    """Initializes .agent_skills/ context or installs custom skills from the library"""
    skills_dir = ".agent_skills"
    if not os.path.exists(skills_dir):
        os.makedirs(skills_dir)
        console.print(f"[info]Created {skills_dir}/ directory for project skills.[/info]")
        
    if list_skills:
        if os.path.exists(SKILLS_LIBRARY_DIR):
            available = [f[:-3] for f in os.listdir(SKILLS_LIBRARY_DIR) if f.endswith(".md")]
            console.print("[info]Available Predefined Skills in Library:[/info]")
            for s in sorted(available):
                console.print(f"  • [bold green]{s}[/bold green]")
        else:
            console.print("[warning]Skills library directory not found.[/warning]")
        return

    skills_to_install = set()
    if all_skills or profile == "all":
        if os.path.exists(SKILLS_LIBRARY_DIR):
            skills_to_install.update([f[:-3] for f in os.listdir(SKILLS_LIBRARY_DIR) if f.endswith(".md")])
    elif profile == "ds":
        skills_to_install.update([
            "ds_eda_and_plotting", "ds_data_interpretation", "ds_feature_extraction",
            "ds_statistical_analysis", "ds_predictive_modeling", "dl_scripting",
            "writing_style_and_tone", "markdown_documentation"
        ])
    elif profile == "dev":
        skills_to_install.update([
            "code_style", "review_loop", "py_tool_creation", "custom_adk_skill",
            "writing_style_and_tone", "markdown_documentation"
        ])
        
    if add:
        for s in add:
            skills_to_install.add(s)
            
    if not skills_to_install and not os.listdir(skills_dir):
        default_skill_path = os.path.join(skills_dir, "workflow.md")
        with open(default_skill_path, "w", encoding="utf-8") as f:
            f.write("# Default Workflow\n\nBe concise and prioritize high-performance code practices.")
        console.print(f"[info]Generated default skill file at {default_skill_path}[/info]")
        console.print("[yellow]Tip: Use `agen init --list` or `agen init --profile ds` to install advanced skills![/yellow]")
        return

    installed_count = 0
    for s in sorted(skills_to_install):
        src_path = os.path.join(SKILLS_LIBRARY_DIR, f"{s}.md")
        if os.path.exists(src_path):
            dst_path = os.path.join(skills_dir, f"{s}.md")
            shutil.copyfile(src_path, dst_path)
            console.print(f"[info]Installed skill:[/info] [bold green]{s}.md[/bold green] -> {skills_dir}/")
            installed_count += 1
        else:
            console.print(f"[warning]Skill '{s}' not found in library.[/warning]")
            
    if installed_count > 0:
        console.print(f"\n[status]Successfully loaded {installed_count} skill(s) into {skills_dir}/![/status]")

def interactive_repl(session_id: str = "default", tough: bool = False):
    console.print(Panel.fit(
        "[bold #00ffff]TERMINAL AGENT v0.2.0[/bold #00ffff] | [bold #5d3fd3]Split-Brain Architecture[/bold #5d3fd3]\n"
        f"Active Session: [bold green]{session_id}[/bold green] | Mode: [bold purple]{'Tough' if tough else 'Light'}[/bold purple]\n"
        "Type [bold yellow]/session <id>[/bold yellow] to switch sessions, [bold yellow]/clear[/bold yellow] to clear history, or [bold red]exit[/bold red] to quit.",
        title="[bold #00ffff]Ready[/bold #00ffff]",
        border_style="#5d3fd3"
    ))
    
    current_session = session_id
    current_tough = tough
    system_context = load_system_context()
    mcp_servers = load_mcp_servers()
    
    local_cfg = load_local_config()
    current_provider = local_cfg.get("provider", "gemini")
    current_model = local_cfg.get("model", "gemma:7b")
    
    while True:
        try:
            mode_badge = f"[local:{current_model}]" if current_provider == "ollama" else ("" if not current_tough else "[tough]")
            user_input = Prompt.ask(f"[bold #5d3fd3]agen({current_session}){mode_badge}>[/bold #5d3fd3]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[info]Exiting interactive session...[/info]")
            break
            
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "/q"):
            console.print("[info]Exiting interactive session... Goodbye![/info]")
            break
        if user_input.lower() in ("/help", "/h", "?"):
            console.print(Panel.fit(
                "[bold #00ffff]Interactive REPL Slash Commands:[/bold #00ffff]\n"
                "  • [bold yellow]/session <id>[/bold yellow] : Switch conversation session\n"
                "  • [bold yellow]/sessions[/bold yellow]     : List all saved sessions\n"
                "  • [bold yellow]/clear[/bold yellow]        : Clear current session memory\n"
                "  • [bold yellow]/local <model>[/bold yellow] : Switch to offline Ollama LLM (e.g. `/local gemma:7b`)\n"
                "  • [bold yellow]/gemini[/bold yellow]       : Switch back to cloud Gemini API\n"
                "  • [bold yellow]/models[/bold yellow]       : List installed local Ollama models\n"
                "  • [bold yellow]/help[/bold yellow]         : Show this help menu\n"
                "  • [bold red]/exit[/bold red] or [bold red]/q[/bold red]  : Quit REPL\n\n"
                "[bold #5d3fd3]Special File Input Syntax:[/bold #5d3fd3]\n"
                "  • Use [bold green]@filepath[/bold green] inside your prompt to inject file contents automatically!\n"
                "    Example: `Review this script for bugs: @client/cli.py`",
                title="[bold green]REPL Guide & Commands[/bold green]",
                border_style="#00ffff"
            ))
            continue
        if user_input.startswith("/session "):
            parts = user_input.split(" ", 1)
            if len(parts) > 1:
                current_session = parts[1].strip()
                console.print(f"[info]Switched to session: [bold green]{current_session}[/bold green][/info]")
            continue
        if user_input.lower() == "/clear":
            try:
                httpx.delete(f"{BACKEND_URL}/sessions/{current_session}")
                console.print(f"[info]Cleared conversation history for session: {current_session}[/info]")
            except Exception as e:
                console.print(f"[error]Failed to clear session: {e}[/error]")
            continue
        if user_input.lower() == "/sessions":
            try:
                res = httpx.get(f"{BACKEND_URL}/sessions")
                s_list = res.json().get("sessions", [])
                console.print(f"[info]Available sessions: {', '.join(s_list)}[/info]")
            except Exception as e:
                console.print(f"[error]Failed to fetch sessions: {e}[/error]")
            continue
        if user_input.startswith("/local"):
            parts = user_input.split(" ", 1)
            target_model = parts[1].strip() if len(parts) > 1 else current_model or "gemma:7b"
            current_provider = "ollama"
            current_model = target_model
            save_local_config(current_provider, current_model)
            console.print(f"[info]Switched to Offline Local LLM Mode (Ollama):[/info] [bold green]{current_model}[/bold green] (Unlimited Tokens!)")
            continue
        if user_input.lower() == "/gemini":
            current_provider = "gemini"
            save_local_config("gemini", "")
            console.print("[info]Switched back to Cloud Gemini API Mode.[/info]")
            continue
        if user_input.lower() == "/models":
            try:
                res = httpx.get(f"{BACKEND_URL}/local/models")
                m_list = res.json().get("models", [])
                if m_list:
                    names = [m.get("name", "unknown") for m in m_list]
                    console.print(f"[info]Installed Ollama models:[/info] [bold green]{', '.join(names)}[/bold green]")
                else:
                    console.print("[warning]No local models found or Ollama is not running on port 11434.[/warning]")
            except Exception as e:
                console.print(f"[error]Failed to query local models: {e}[/error]")
            continue
            
        task_type = "tough" if current_tough else "light"
        expanded_prompt = expand_file_references(user_input)
        with console.status(f"[status]Agent is thinking ({current_provider} mode)...[/status]"):
            try:
                response = httpx.post(
                    f"{BACKEND_URL}/chat",
                    json={
                        "prompt": expanded_prompt,
                        "task_type": task_type,
                        "system_context": system_context,
                        "session_id": current_session,
                        "mcp_servers": mcp_servers,
                        "provider": current_provider,
                        "model": current_model
                    },
                    timeout=120.0
                )
                response.raise_for_status()
                data = response.json()
                console.print(Markdown(data["response"]))
            except Exception as e:
                console.print(f"[error]Error communicating with backend:[/error] {e}")

@app.command()
def chat(
    prompt: Optional[str] = typer.Argument(None, help="Prompt to send. Leave empty to open interactive REPL."),
    tough: bool = typer.Option(False, "--tough", "-t", help="Use the tougher reasoning model"),
    session: str = typer.Option("default", "--session", "-s", help="Session ID for conversation persistence"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Enter interactive REPL after prompt"),
    local: bool = typer.Option(False, "--local", "-l", help="Use local offline LLM (Ollama/Gemma)"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Specific local model name (e.g. gemma:7b, gemma4, llama3)")
):
    """Opens an interactive session or sends a single prompt"""
    if prompt is None:
        interactive_repl(session_id=session, tough=tough)
        return
        
    task_type = "tough" if tough else "light"
    system_context = load_system_context()
    mcp_servers = load_mcp_servers()
    
    local_cfg = load_local_config()
    provider = "ollama" if (local or model or local_cfg.get("provider") == "ollama") else "gemini"
    target_model = model or local_cfg.get("model", "gemma:7b")
    
    expanded_prompt = expand_file_references(prompt)
    with console.status(f"[status]Agent is thinking ({provider} mode)...[/status]"):
        try:
            response = httpx.post(
                f"{BACKEND_URL}/chat",
                json={
                    "prompt": expanded_prompt,
                    "task_type": task_type,
                    "system_context": system_context,
                    "session_id": session,
                    "mcp_servers": mcp_servers,
                    "provider": provider,
                    "model": target_model
                },
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            console.print(Markdown(data["response"]))
        except httpx.RequestError as e:
            console.print(f"[bold red]Error connecting to backend:[/bold red] {e}")
            console.print("[yellow]Make sure the FastAPI server is running on http://localhost:8000[/yellow]")
        except httpx.HTTPStatusError as e:
            console.print(f"[bold red]Backend returned an error:[/bold red] {e.response.text}")
            
    if interactive:
        interactive_repl(session_id=session, tough=tough)

session_app = typer.Typer(help="Manage persistent chat sessions")
app.add_typer(session_app, name="session")

@session_app.command("list")
def session_list():
    """List all saved chat sessions"""
    try:
        res = httpx.get(f"{BACKEND_URL}/sessions")
        s_list = res.json().get("sessions", [])
        if s_list:
            console.print(f"[info]Saved sessions:[/info] {', '.join(s_list)}")
        else:
            console.print("[warning]No saved sessions found.[/warning]")
    except Exception as e:
        console.print(f"[error]Error communicating with backend:[/error] {e}")

@session_app.command("clear")
def session_clear(session_id: str = typer.Argument("default", help="Session ID to clear")):
    """Clear history for a specific session"""
    try:
        httpx.delete(f"{BACKEND_URL}/sessions/{session_id}")
        console.print(f"[info]Cleared conversation history for session: [bold green]{session_id}[/bold green][/info]")
    except Exception as e:
        console.print(f"[error]Error communicating with backend:[/error] {e}")

mcp_app = typer.Typer(help="Manage Model Context Protocol (MCP) integrations")
app.add_typer(mcp_app, name="mcp")

@mcp_app.command("list")
def mcp_list():
    """List all available MCP servers in the registry"""
    try:
        res = httpx.get(f"{BACKEND_URL}/mcp")
        servers = res.json().get("servers", {})
        active = set(load_mcp_servers())
        
        console.print("[info]Model Context Protocol (MCP) Server Registry:[/info]\n")
        for name, info in sorted(servers.items()):
            status_badge = "[bold green][ENABLED][/bold green]" if name in active else "[bold #5d3fd3][AVAILABLE][/bold #5d3fd3]"
            console.print(f"{status_badge} [bold white]{name}[/bold white] ({info.get('type', 'general')})")
            console.print(f"  • {info.get('description', '')}")
            tools_str = ", ".join([f"`{t}`" for t in info.get("tools", [])])
            console.print(f"  • [dim]Tools:[/dim] {tools_str}\n")
    except Exception as e:
        console.print(f"[error]Error communicating with backend:[/error] {e}")

@mcp_app.command("enable")
def mcp_enable(server_name: str = typer.Argument(..., help="Name of MCP server to enable")):
    """Enable an MCP server for the current workspace"""
    try:
        res = httpx.get(f"{BACKEND_URL}/mcp/{server_name}")
        if res.status_code == 200:
            active = load_mcp_servers()
            if server_name not in active:
                active.append(server_name)
                save_mcp_servers(active)
            console.print(f"[info]Enabled MCP server:[/info] [bold green]{server_name}[/bold green]")
        else:
            console.print(f"[error]Server '{server_name}' not found in registry. Use `agen mcp list` to see valid servers.[/error]")
    except Exception as e:
        console.print(f"[error]Error connecting to backend:[/error] {e}")

@mcp_app.command("disable")
def mcp_disable(server_name: str = typer.Argument(..., help="Name of MCP server to disable")):
    """Disable an MCP server for the current workspace"""
    active = load_mcp_servers()
    if server_name in active:
        active.remove(server_name)
        save_mcp_servers(active)
        console.print(f"[info]Disabled MCP server:[/info] [yellow]{server_name}[/yellow]")
    else:
        console.print(f"[warning]Server '{server_name}' was not enabled.[/warning]")

@mcp_app.command("status")
def mcp_status():
    """Show currently enabled MCP servers"""
    active = load_mcp_servers()
    if active:
        console.print(f"[info]Active MCP Servers in workspace:[/info] [bold green]{', '.join(active)}[/bold green]")
    else:
        console.print("[warning]No MCP servers enabled. Use `agen mcp list` and `agen mcp enable <name>` to connect external data silos![/warning]")

local_app = typer.Typer(help="Manage local offline LLMs (Ollama / Gemma)")
app.add_typer(local_app, name="local")

@local_app.command("list")
def local_list():
    """List all installed local offline models from Ollama"""
    try:
        res = httpx.get(f"{BACKEND_URL}/local/models")
        m_list = res.json().get("models", [])
        if m_list:
            console.print("[info]Installed Offline Ollama Models:[/info]\n")
            for m in m_list:
                console.print(f"  • [bold green]{m.get('name')}[/bold green] ([dim]{m.get('details', {}).get('parameter_size', '')}[/dim])")
        else:
            console.print("[warning]No local models found. Make sure Ollama is installed and running on port 11434![/warning]")
            console.print("[info]Tip: Run `ollama run gemma:7b` in a terminal to pull and run Gemma![/info]")
    except Exception as e:
        console.print(f"[error]Error communicating with backend:[/error] {e}")

@local_app.command("use")
def local_use(model_name: str = typer.Argument("gemma:7b", help="Model name to set as default offline LLM")):
    """Set the default offline LLM model for your project"""
    save_local_config("ollama", model_name)
    console.print(f"[info]Set default offline LLM to:[/info] [bold green]{model_name}[/bold green] (Ollama Mode)")

@local_app.command("cloud")
def local_cloud():
    """Switch back to Google Gemini API (Cloud Mode)"""
    save_local_config("gemini", "")
    console.print("[info]Switched LLM Provider back to:[/info] [bold #00ffff]Google Gemini API[/bold #00ffff] (Cloud Mode)")

@local_app.command("reset")
def local_reset():
    """Reset LLM provider to default Cloud Mode"""
    save_local_config("gemini", "")
    console.print("[info]Reset LLM Provider to default Cloud Mode (Gemini API).[/info]")

@local_app.command("status")
def local_status():
    """Check active LLM provider mode"""
    cfg = load_local_config()
    provider = cfg.get("provider", "gemini")
    model = cfg.get("model", "gemma:7b")
    if provider == "ollama":
        console.print(f"[info]Current LLM Provider:[/info] [bold green]Offline Ollama[/bold green] (Model: {model}) — Unlimited Free Tokens!")
    else:
        console.print("[info]Current LLM Provider:[/info] [bold #00ffff]Google Gemini API[/bold #00ffff] (Cloud Mode)")

@app.command()
def exec(
    prompt: str,
    local: bool = typer.Option(False, "--local", "-l", help="Use local offline LLM"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Specific local model name")
):
    """Executes generated scripts locally"""
    system_context = load_system_context()
    mcp_servers = load_mcp_servers()
    local_cfg = load_local_config()
    provider = "ollama" if (local or model or local_cfg.get("provider") == "ollama") else "gemini"
    target_model = model or local_cfg.get("model", "gemma:7b")
    
    expanded_prompt = expand_file_references(prompt)
    with console.status(f"[status]Agent is writing code ({provider} mode)...[/status]"):
        try:
            response = httpx.post(
                f"{BACKEND_URL}/exec",
                json={"prompt": expanded_prompt, "system_context": system_context, "mcp_servers": mcp_servers, "provider": provider, "model": target_model},
                timeout=60.0
            )
            response.raise_for_status()
            code = response.json()["response"]
            
            script_path = ".agent_tmp.py"
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(code)
                
            console.print("[info]Executing generated script...[/info]")
            result = subprocess.run(["python", script_path], capture_output=True, text=True)
            
            if result.stdout:
                console.print(result.stdout)
            if result.stderr:
                console.print(f"[error]{result.stderr}[/error]")
                
            os.remove(script_path)
            
        except Exception as e:
            console.print(f"[error]Execution failed: {e}[/error]")

@app.command()
def review(file_path: str, focus: str = typer.Option("general", "--focus", "-f")):
    """Read-only analysis of a file"""
    if not os.path.exists(file_path):
        console.print(f"[error]File not found: {file_path}[/error]")
        return
        
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
        
    prompt_str = f"Review the following file focusing on '{focus}'.\n\nFile contents:\n{file_content}"
    # Call the chat command internally
    chat(prompt=prompt_str, tough=True, session="default")

@app.command()
def vision(
    image_path: str,
    prompt: str,
    local: bool = typer.Option(False, "--local", "-l", help="Use local offline LLM"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Specific local model name")
):
    """Processes an image file"""
    if not os.path.exists(image_path):
        console.print(f"[error]Image not found: {image_path}[/error]")
        return
        
    system_context = load_system_context()
    mcp_servers = load_mcp_servers()
    local_cfg = load_local_config()
    provider = "ollama" if (local or model or local_cfg.get("provider") == "ollama") else "gemini"
    target_model = model or local_cfg.get("model", "gemma:7b")
    
    with console.status(f"[status]Agent is analyzing the image ({provider} mode)...[/status]"):
        try:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            
            response = httpx.post(
                f"{BACKEND_URL}/vision",
                json={"prompt": prompt, "image_base64": image_base64, "system_context": system_context, "mcp_servers": mcp_servers, "provider": provider, "model": target_model},
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            console.print(Markdown(data["response"]))
            
        except Exception as e:
            console.print(f"[error]Vision analysis failed: {e}[/error]")

def main():
    app()

if __name__ == "__main__":
    main()
