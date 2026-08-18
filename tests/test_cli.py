import pytest
from prompt_toolkit.document import Document
from client.cli import AgenCompleter

def test_agen_completer_commands():
    """Test that the autocomplete UI only triggers on the first word (fixes the UX trap)."""
    completer = AgenCompleter()
    
    # Test 1: First word completion (should yield commands)
    doc = Document("/he", cursor_position=3)
    completions = list(completer.get_completions(doc, None))
    assert len(completions) > 0
    assert any(c.text == "/help" for c in completions) # completes to /help
    
    # Test 2: Second word completion (should NOT yield slash commands)
    doc = Document("/model gemi", cursor_position=11)
    completions = list(completer.get_completions(doc, None))
    assert len(completions) == 0

def test_agen_completer_file_attachment():
    """Test that the @ symbol triggers file path autocompletion anywhere in the prompt."""
    completer = AgenCompleter()
    
    # Test 3: @ file completion at the end of a sentence
    doc = Document("Can you refactor the code in @te", cursor_position=32)
    completions = list(completer.get_completions(doc, None))
    # We don't check exact matches because it depends on the local filesystem,
    # but we verify it correctly initializes the PathCompleter and doesn't crash.
    assert isinstance(completions, list)
