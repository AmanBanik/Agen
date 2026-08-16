---
name: comprehensive-testing
description: QA standards, pytest, mocking LLMs, and E2E agent validation.
effort_level: Expert
required_tools: Pytest, unittest.mock
triggers: ["pytest", "mocking", "writing tests", "QA"]
---
# Skill: Comprehensive Testing

## Overview
Testing autonomous agents is notoriously difficult because their outputs are non-deterministic. We require strict mocking and QA standards.

## Strict Rules
1. **Mocking LLMs:** Tests running in CI *must never* make live calls to Gemini or Claude. You must use `unittest.mock.patch` to simulate the LLM returning specific JSON tool calls or text responses.
2. **E2E Swarm Simulations:** Write integration tests that simulate a user prompt, mock the LLM's reasoning loop, and assert that the correct subagent was invoked.
3. **Edge Case Validation:** Write explicit tests for:
   - Network timeouts (mocking `requests.exceptions.Timeout`).
   - Rate limit errors (429 Too Many Requests).
   - Malformed JSON responses from the LLM.
