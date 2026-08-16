---
name: docs-and-standards
description: The voice and tone of the Agen project, maintaining documentation.
effort_level: Low
required_tools: Markdown, HTML/CSS
triggers: ["writing README", "updating docs", "docstrings", "blog"]
---
# Skill: Docs & Standards

## Overview
Agen's documentation is critical. It must maintain a highly professional, witty, and slightly dramatic tone (think "Terminal Swarm", "Prime Directive", "Technical Debt").

## Strict Rules
1. **Updating the Blog:** When making major changes, update `blog/index.html`. Keep CSS and JS separate in `blog/style.css` and `blog/script.js`—do not inline them back into the HTML.
2. **README.md:** Keep installation instructions pristine. If you break the `install.sh` script, update the README immediately.
3. **Inline Docstrings:** Use Google-style docstrings for Python. Focus on explaining edge cases and exceptions rather than restating the function name.

## Examples
- *Bad:* "Function to calculate max limit." (in a docstring)
- *Good:* "Calculates the maximum token limit. Raises `TokenLimitError` if context exceeds 128k. Ensure inputs are pre-chunked."
