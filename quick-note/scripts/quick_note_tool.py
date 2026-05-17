#!/usr/bin/env python3
"""
Quick Note Tool for Hermes Agent

Provides the quick-note tool to create timestamped text notes.
"""

import datetime
from pathlib import Path
from tools.registry import registry, ToolError
from hermes_constants import get_hermes_home


def quick_note_tool(content: str, task_id: str = None) -> str:
    """
    Create a timestamped note file with the given content.

    Args:
        content: The note content to save
        task_id: Optional task ID for tracing

    Returns:
        Success message with the file path
    """
    if not content or not content.strip():
        raise ToolError("Note content cannot be empty")

    # Get notes directory from config or use default
    notes_dir = get_hermes_home() / "notes"
    
    # Try to get configured directory from global config
    try:
        from agent.model import ModelManager
        config = ModelManager.shared().config
        if config.get('notes_directory'):
            notes_dir = Path(config['notes_directory']).expanduser()
    except:
        pass  # Use default if config access fails

    # Ensure notes directory exists
    notes_dir.mkdir(parents=True, exist_ok=True)

    # Generate timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"note_{timestamp}.txt"
    filepath = notes_dir / filename

    try:
        # Write the note content to file
        filepath.write_text(content.strip() + "\n", encoding="utf-8")
        
        return f"Note saved successfully: {filepath}"
    except Exception as e:
        raise ToolError(f"Failed to save note: {str(e)}")


# Register the tool
registry.register(
    name="quick-note",
    toolset="productivity",
    schema={
        "name": "quick-note",
        "description": "Create a timestamped text note",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The note content to save"
                }
            },
            "required": ["content"],
            "additionalProperties": False
        }
    },
    handler=lambda args, **kw: quick_note_tool(
        args.get("content", ""),
        task_id=kw.get("task_id")
    ),
    description="Create timestamped text notes in a dedicated notes directory"
)