# Skill: Python CLI & Tool Creation Best Practices

## 1. Typer & Rich CLI Design Standards
When developing command-line applications and custom utilities:
1. **Framework Selection**: Always use `Typer` for command routing and argument parsing, paired with `Rich` for terminal styling, markdown rendering, tables, and progress spinners.
2. **Stealth Aesthetic Styling**:
   * Use consistent, high-contrast color palettes: `bold #00ffff` (Neon Cyan) for info/headers, `bold #5d3fd3` (Deep Purple) for status/spinners, `bold yellow` for warnings, and `bold red` for errors.
   * Wrap interactive prompts and startup banners in `rich.panel.Panel.fit(...)` with colored borders.
3. **Progress Feedback**: Any network operation, LLM API call, or file processing task taking > 300ms MUST be wrapped in a live status spinner:
   ```python
   with console.status("[bold #5d3fd3]Processing data payload...[/bold #5d3fd3]"):
       result = run_heavy_task()
   ```

## 2. Error Handling & User Experience
* **No Raw Tracebacks for Users**: Catch expected CLI exceptions (`FileNotFoundError`, `httpx.ConnectError`, `typer.Exit`) and print clean, user-friendly Rich error boxes rather than dumping 50-line Python stack traces to the console.
* **Help & Documentation**: Every Typer command (`@app.command()`) and argument (`typer.Option(...)`, `typer.Argument(...)`) must have a clear `help="..."` string explaining its usage and defaults.
