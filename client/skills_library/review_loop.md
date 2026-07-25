# Skill: Systematic Code & Architecture Review Loop

## Code Review Framework
When analyzing or reviewing code via `agen review` or in interactive chat, systematically inspect the codebase across these 5 pillars:

### 1. Security & Vulnerabilities
* Look for hardcoded API keys, passwords, or tokens.
* Check for SQL injection, command injection (`eval()`, untrusted `subprocess.run(..., shell=True)`), and path traversal risks.
* Verify input validation and sanitization on all external endpoints.

### 2. Algorithmic & Hardware Efficiency (Big-O)
* Analyze time complexity ($O(1)$, $O(N)$, $O(N^2)$) and space complexity.
* Identify unnecessary memory copying, redundant database queries (N+1 problem), or blocking I/O inside async loops.
* Check for GPU/CPU memory bottlenecks (e.g., failing to call `.detach()` or `.cpu()` on PyTorch tensors inside training loops).

### 3. Reliability & Edge Cases
* Test for division by zero, empty arrays, null/None propagation, and unexpected type coercions.
* Check behavior under concurrent access or race conditions.

### 4. Maintainability & Code Health
* Verify naming clarity, docstring completeness, and adherence to DRY (Don't Repeat Yourself) principles.

## Review Output Format
Organize your review into:
1. **Critical Issues (Must Fix)**: Bugs or security risks.
2. **Performance Bottlenecks**: Hardware/speed optimizations.
3. **Refactoring Suggestions**: Clean code improvements.
