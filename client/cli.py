import sys
import os

try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import json
import httpx
import typer
import subprocess
import re
from pylatexenc.latex2text import LatexNodes2Text
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion, PathCompleter, WordCompleter
from prompt_toolkit.formatted_text import HTML

app = typer.Typer(invoke_without_command=True)
console = Console()
latex_parser = LatexNodes2Text()

def parse_math(match):
    latex_math = match.group(1)
    try:
        text = latex_parser.latex_to_text(latex_math)
        return text.replace("\n", "  \n")
    except Exception:
        return match.group(0)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(max(0, min(255, rgb[0]))), int(max(0, min(255, rgb[1]))), int(max(0, min(255, rgb[2]))))

def interpolate_color(color1, color2, factor):
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    rgb = [rgb1[i] + (rgb2[i] - rgb1[i]) * factor for i in range(3)]
    return rgb_to_hex(rgb)

def print_gradient_logo():
    # An imposing, chunky stylized 'A' (Alpha) using block characters!
    logo_lines = [
        "      ▄▄████▄▄      ",
        "    ▄██████████▄    ",
        "   ████▀▀  ▀▀████   ",
        "  ████        ████  ",
        " ██████████████████ ",
        "█████▀▀▀▀▀▀▀▀▀▀█████",
        "████            ████",
        "███              ███"
    ]
    
    # Lime -> Silver -> Golden -> Orange
    stops = ["#32cd32", "#c0c0c0", "#ffd700", "#ffa500"]
    
    def get_color(x, y, width, height):
        # Create a smooth diagonal gradient map (0.0 to 1.0)
        factor = (y / (height - 1)) * 0.6 + (x / (width - 1)) * 0.4
        idx = factor * (len(stops) - 1)
        idx_int = int(idx)
        if idx_int >= len(stops) - 1:
            return stops[-1]
        
        local_factor = idx - idx_int
        return interpolate_color(stops[idx_int], stops[idx_int + 1], local_factor)
        
    console.print()
    for y, line in enumerate(logo_lines):
        text_obj = Text()
        for x, char in enumerate(line):
            if char == " ":
                text_obj.append(char)
            else:
                color = get_color(x, y, len(line), len(logo_lines))
                text_obj.append(char, style=f"bold {color}")
        console.print(text_obj)
    
    console.print(Text("Agen v2.0", style="bold white"), " - Autonomous AI Engineering CLI")
    console.print(Text("~", style="dim white"))
    console.print()

class AgenCompleter(Completer):
    def __init__(self):
        self.path_completer = PathCompleter()
        self.commands = ['/help', '/exit', '/clear', '/index', '/skill', '/ollama', '/gemini', '/model', '/tokens', '/swarm', '/tools', '/skills']
        
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split(' ')
        
        # Only autocomplete commands if we are typing the FIRST word
        if len(words) == 1 and text.startswith('/'):
            for cmd in self.commands:
                if cmd.startswith(text):
                    yield Completion(cmd, start_position=-len(text))
                
        # File completion for @ symbol anywhere in the string
        last_word = words[-1] if words else ''
        if last_word.startswith('@'):
            # create a pseudo document for path completion
            path_text = last_word[1:]
            path_doc = document.__class__(text=path_text, cursor_position=len(path_text))
            for c in self.path_completer.get_completions(path_doc, complete_event):
                yield c

# Global provider state
current_provider = "gemini"
current_model = None

@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context):
    global current_provider, current_model
    if ctx.invoked_subcommand is None:
        print_gradient_logo()
        console.print("[dim]Welcome to Agen V2 Interactive Mode! Type '/help' for commands, '@' for file completion, or '/exit' to quit.[/dim]\n")
        
        session = PromptSession(completer=AgenCompleter())
        
        while True:
            try:
                # Use prompt_toolkit session
                user_input = session.prompt(HTML("<b><ansicyan>agen></ansicyan></b> "))
                
                cmd = user_input.strip()
                if cmd.lower() in ("/exit", "/quit", "exit", "quit"):
                    break
                elif cmd.lower() == "/clear":
                    console.clear()
                    print_gradient_logo()
                    continue
                elif cmd.lower() == "/help":
                    console.print(Panel(
                        "Available Commands:\n"
                        "[bold cyan]/help[/bold cyan]   - Show this help menu\n"
                        "[bold cyan]/clear[/bold cyan]  - Clear the terminal screen\n"
                        "[bold cyan]/exit[/bold cyan]   - Quit the CLI\n"
                        "[bold cyan]/ollama[/bold cyan] - Switch to Local Ollama Mode (e.g. Llama3/Gemma)\n"
                        "[bold cyan]/gemini[/bold cyan] - Switch to Google Gemini Cloud Mode\n"
                        "[bold cyan]/model[/bold cyan]  - Swap specific model (e.g., /model gemini-1.5-pro)\n"
                        "[bold cyan]/tokens[/bold cyan] - Show session token telemetry\n"
                        "[bold cyan]/swarm[/bold cyan]  - Display active async subagents\n"
                        "[bold cyan]/tools[/bold cyan]  - List active MCP and Native tools\n"
                        "[bold cyan]/skills[/bold cyan] - View loaded autonomous engineering standards\n"
                        "[bold cyan]/skill[/bold cyan]  - Pull a community skill (usage: /skill pull <url>)\n\n"
                        "Shortcuts:\n"
                        "[bold magenta]@[/bold magenta]       - Type @ to autocomplete and attach local files/folders\n",
                        title="💡 [bold yellow]Agen Help[/bold yellow]", border_style="yellow"
                    ))
                    continue
                elif cmd.lower().startswith("/skill"):
                    args = cmd.split()
                    if len(args) == 3 and args[1].lower() == "pull":
                        skill_command("pull", args[2])
                    else:
                        console.print("[red]Usage: /skill pull <github_url>[/red]")
                    continue
                elif cmd.lower().startswith("/index"):
                    args = cmd.split()
                    path = args[1] if len(args) > 1 else "."
                    index_repo(path)
                    continue
                elif cmd.lower() == "/ollama":
                    current_provider = "ollama"
                    console.print("[bold green]Switched to Local Ollama Provider![/bold green] (Make sure ollama is running on your system)")
                    continue
                elif cmd.lower() == "/gemini":
                    current_provider = "gemini"
                    current_model = None
                    console.print("[bold green]Switched to Google Gemini Provider![/bold green]")
                    continue
                elif cmd.lower().startswith("/model"):
                    args = cmd.split()
                    if len(args) > 1:
                        current_model = args[1]
                        console.print(f"[bold green]Switched specific model to:[/bold green] {current_model}")
                    else:
                        console.print("[red]Usage: /model <model_name>[/red]")
                    continue
                elif cmd.lower() == "/skills":
                    table = Table(title="Loaded Autonomous Skills", border_style="cyan")
                    table.add_column("Skill Path", style="dim")
                    table.add_column("Type")
                    
                    for base_dir, stype in [(".agent/skills", "Core Standards"), (".agent_skills", "Community Skill")]:
                        full_path = os.path.join(os.path.dirname(__file__), "..", base_dir)
                        if os.path.exists(full_path):
                            for root, dirs, files in os.walk(full_path):
                                for f in files:
                                    if f.endswith(".md"):
                                        rel_path = os.path.relpath(os.path.join(root, f), os.path.dirname(__file__) + "/..")
                                        table.add_row(rel_path, stype)
                    console.print(table)
                    continue
                elif cmd.lower() == "/tools":
                    table = Table(title="Active MCP & Native Tools", border_style="magenta")
                    table.add_column("Tool Name", style="bold cyan")
                    table.add_column("Source", style="dim")
                    table.add_row("read_file", "Native (ReAct)")
                    table.add_row("write_file", "Native (ReAct)")
                    table.add_row("list_dir", "Native (ReAct)")
                    table.add_row("execute_shell", "Native (ReAct)")
                    table.add_row("read_browser_page", "Native (ReAct)")
                    table.add_row("invoke_subagent", "Native (Swarm)")
                    table.add_row("search_web", "MCP (Tavily)")
                    table.add_row("github_*", "MCP (GitHub)")
                    console.print(table)
                    continue
                elif cmd.lower() == "/swarm":
                    table = Table(title="Asynchronous Swarm Fleet", border_style="yellow")
                    table.add_column("Task ID", style="bold yellow")
                    table.add_column("Status", style="green")
                    
                    try:
                        response = httpx.get("http://localhost:8000/swarm_status", timeout=2.0)
                        if response.status_code == 200:
                            tasks = response.json().get("active_tasks", [])
                            if not tasks:
                                table.add_row("No active subagents.", "-")
                            else:
                                for t in tasks:
                                    table.add_row(str(t), "Running")
                        else:
                            table.add_row("Backend unreachable", "Error")
                    except Exception:
                        table.add_row("Backend unreachable", "Error")
                        
                    console.print(table)
                    continue
                elif cmd.lower() == "/tokens":
                    console.print(Panel(
                        "Token usage tracking is enabled via LangChain callbacks.\nCheck backend console for exact counts.", 
                        title="📊 [bold blue]Token Telemetry[/bold blue]", border_style="blue"
                    ))
                    continue
                    
                if cmd:
                    # Inject file contents if @ attachments exist
                    final_prompt = cmd
                    # Find all words starting with @
                    attachments = [w[1:] for w in cmd.split() if w.startswith('@') and len(w) > 1]
                    if attachments:
                        context_str = "\n\n--- ATTACHED FILES ---\n"
                        for att in attachments:
                            if os.path.exists(att):
                                if os.path.isfile(att):
                                    try:
                                        with open(att, 'r', encoding='utf-8') as f:
                                            context_str += f"File: {att}\n{f.read()}\n\n"
                                    except Exception as e:
                                        console.print(f"[red]Could not read attached file {att}: {e}[/red]")
                                elif os.path.isdir(att):
                                    context_str += f"Directory: {att}\nFiles:\n"
                                    try:
                                        for root, dirs, files in os.walk(att):
                                            # Limit depth or file count for sanity
                                            level = root.replace(att, '').count(os.sep)
                                            if level < 3: 
                                                indent = ' ' * 4 * (level)
                                                context_str += f"{indent}{os.path.basename(root)}/\n"
                                                subindent = ' ' * 4 * (level + 1)
                                                for f in files:
                                                    context_str += f"{subindent}{f}\n"
                                    except Exception as e:
                                        console.print(f"[red]Could not read attached directory {att}: {e}[/red]")
                                    context_str += "\n"
                        final_prompt += context_str
                        
                    chat(final_prompt)
            except (KeyboardInterrupt, EOFError):
                break

@app.command()
def chat(prompt: str):
    """Start a real-time streaming chat with Agen v2"""
    console.print(f"[bold cyan]You:[/bold cyan] {prompt}")
    console.print("[bold magenta]Agen:[/bold magenta] ")
    
    payload = {
        "prompt": prompt, 
        "system_context": "You are a highly capable autonomous AI Engineering CLI assistant. You can write, read, and execute files/commands to solve problems.", 
        "task_type": "tough",
        "provider": current_provider,
        "model": current_model
    }
    
    current_text = ""
    live = None
    
    def start_live():
        nonlocal live, current_text
        current_text = ""
        live = Live(Markdown(current_text), console=console, refresh_per_second=15)
        live.start()
        
    def stop_live():
        nonlocal live
        if live:
            live.stop()
            live = None
            
    try:
        start_live()
        with httpx.stream("POST", "http://localhost:8000/stream_chat", json=payload, timeout=300.0) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                        msg_type = data.get("type")
                        
                        if msg_type == "text":
                            current_text += data.get("content", "")
                            if live:
                                md_text = current_text
                                # Dynamically convert LaTeX symbols to beautiful Unicode math!
                                md_text = re.sub(r'\$\$(.*?)\$\$', parse_math, md_text, flags=re.DOTALL)
                                md_text = re.sub(r'\\\[(.*?)\\\]', parse_math, md_text, flags=re.DOTALL)
                                md_text = re.sub(r'\$(.*?)\$', parse_math, md_text)
                                live.update(Markdown(md_text))
                        elif msg_type == "tool_start":
                            stop_live()
                            tool_name = data.get("tool_name", "")
                            tool_args = data.get("tool_args", {})
                            console.print(Panel(f"Arguments: {json.dumps(tool_args)}", title=f"🔧 [bold cyan]Agent executing:[/bold cyan] {tool_name}", border_style="cyan"))
                        elif msg_type == "tool_end":
                            tool_name = data.get("tool_name", "")
                            res = data.get("result", "")
                            res_preview = res[:200] + "..." if len(res) > 200 else res
                            console.print(Panel(res_preview, title=f"✅ [bold green]Result:[/bold green] {tool_name}", border_style="green"))
                            start_live()
                        elif msg_type == "error":
                            stop_live()
                            console.print(f"\n[red]Error from agent:[/red] {data.get('content')}")
                            
                        # Fallback for old format
                        elif "text" in data:
                            current_text += data.get("text", "")
                            if live:
                                live.update(Markdown(current_text))
                            
                    except json.JSONDecodeError:
                        if "error" in data_str:
                            stop_live()
                            console.print(f"\n[red]Backend Error:[/red] {data_str}")
        stop_live()
        print()
    except Exception as e:
        stop_live()
        console.print(f"\n[red]Failed to connect to backend: {e}[/red]\n[dim]Make sure the V2 FastAPI server is running on localhost:8000[/dim]")

@app.command("key")
def set_api_key(api_key: str = typer.Argument(..., help="Your Google Gemini API Key")):
    """Set and save your Google Gemini API key"""
    env_path = os.path.join(os.path.dirname(__file__), "..", "backend", ".env")
    home_env = os.path.expanduser("~/.agent_env")
    
    try:
        with open(home_env, "w", encoding="utf-8") as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
    except Exception:
        pass
        
    try:
        os.makedirs(os.path.dirname(env_path), exist_ok=True)
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
    except Exception:
        pass
        
    console.print("[info]Google Gemini API Key saved successfully![/info] [bold green]Ready for Cloud Mode![/bold green]")

@app.command("index")
def index_repo(path: str = typer.Argument(".", help="Directory to index into ChromaDB")):
    """Scan and index a directory for RAG (Semantic Memory)"""
    abs_path = os.path.abspath(path)
    console.print(f"[bold cyan]Indexing repository:[/bold cyan] {abs_path}")
    
    try:
        with console.status("[status]Chunking files and generating embeddings...[/status]"):
            response = httpx.post(
                "http://localhost:8000/index_repo",
                json={"directory": abs_path},
                timeout=300.0
            )
            response.raise_for_status()
            data = response.json()
            chunks = data.get("chunks_indexed", 0)
        
        console.print(f"[bold green]Success![/bold green] Indexed {chunks} chunks into semantic memory.")
        console.print("[dim]You can now use `agen chat` and it will automatically pull relevant context from these files![/dim]")
    except Exception as e:
        console.print(f"\n[red]Failed to index repository: {e}[/red]\n[dim]Make sure the V2 FastAPI server is running.[/dim]")

@app.command("skill")
def skill_command(action: str = typer.Argument(..., help="'pull'"), url: str = typer.Argument(..., help="GitHub URL of the skill repository")):
    """Manage Agen Skills (e.g., agen skill pull <github_url>)"""
    if action.lower() != "pull":
        console.print("[red]Only 'pull' action is currently supported![/red]")
        return
        
    skills_dir = os.path.join(os.path.dirname(__file__), "..", ".agent_skills")
    os.makedirs(skills_dir, exist_ok=True)
    repo_name = url.split("/")[-1].replace(".git", "")
    target_path = os.path.abspath(os.path.join(skills_dir, repo_name))
    
    console.print(f"[bold cyan]Pulling Community Skill:[/bold cyan] {url}")
    
    try:
        with console.status("[status]Cloning repository...[/status]"):
            result = subprocess.run(["git", "clone", url, target_path], capture_output=True, text=True)
            if result.returncode != 0:
                console.print(f"[red]Git clone failed:[/red]\n{result.stderr}")
                return
                
        console.print(f"[bold green]Success![/bold green] Skill repository cloned to {target_path}")
        console.print("[dim]Agen will automatically read these skills during Autonomous loops![/dim]")
    except Exception as e:
        console.print(f"[red]Error pulling skill:[/red] {e}")

def main():
    app()

if __name__ == "__main__":
    main()
