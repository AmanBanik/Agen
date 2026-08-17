import os
import pytest
from unittest.mock import patch
from backend.tools import _validate_path, WORKSPACE_DIR, list_dir_tool

def test_validate_path_inside_workspace():
    """Ensure paths inside the workspace pass validation without prompting."""
    safe_file = os.path.join(WORKSPACE_DIR, "README.md")
    assert _validate_path(safe_file) == safe_file

@patch("backend.tools.Confirm.ask", return_value=False)
def test_validate_path_outside_workspace_denied(mock_confirm):
    """Ensure path outside the workspace raises a PermissionError when denied by the user."""
    # Attempt to access the parent directory of the workspace
    unsafe_file = os.path.abspath(os.path.join(WORKSPACE_DIR, "..", "secret.txt"))
    
    with pytest.raises(PermissionError) as excinfo:
        _validate_path(unsafe_file)
    
    assert "Access Denied by User" in str(excinfo.value)
    mock_confirm.assert_called_once()

@patch("backend.tools.Confirm.ask", return_value=True)
def test_validate_path_outside_workspace_granted(mock_confirm):
    """Ensure path outside the workspace is allowed if explicitly granted by the user."""
    unsafe_file = os.path.abspath(os.path.join(WORKSPACE_DIR, "..", "allowed_dir"))
    
    result = _validate_path(unsafe_file)
    assert result == unsafe_file
    mock_confirm.assert_called_once()

def test_list_dir_tool_safe():
    """Ensure the list_dir_tool correctly lists the workspace boundary."""
    result = list_dir_tool(WORKSPACE_DIR)
    assert "Contents of" in result
    # We expect standard repository folders to be listed
    assert "backend" in result or "client" in result or "README.md" in result
