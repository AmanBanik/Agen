# Skill: Code Style & High-Performance Engineering

## Python & Systems Programming Standards
1. **Strict Type Hinting**: Every function signature MUST include PEP 484 type hints for all arguments and return values (e.g., `def process_batch(data: list[dict[str, Any]]) -> pd.DataFrame:`).
2. **Vectorization Over Loops**: In Python/Data Science, never write explicit `for` loops over Pandas DataFrames or NumPy arrays. Use vectorized operations, boolean indexing, or `.apply()` with compiled Numba/Cython routines if necessary.
3. **Defensive Programming & Explicit Errors**:
   * Never use bare `except:` or catch silent errors (`except Exception: pass`).
   * Catch specific exceptions (e.g., `ValueError`, `KeyError`, `httpx.HTTPStatusError`).
   * Provide informative error messages with context.
4. **Modularity & Single Responsibility**: Functions should be under 40 lines. If a function is doing data ingestion, cleaning, and plotting, split it into three independent, testable routines.
5. **Resource Management**: Always use context managers (`with open(...) as f:`, `with httpx.Client() as client:`) for file handles, network connections, and database sessions to prevent resource leaks.
