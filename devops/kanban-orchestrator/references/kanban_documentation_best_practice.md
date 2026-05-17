# Kanban Task Documentation Best Practice

After creating Kanban tasks as an orchestrator, it's valuable to create supporting documentation for future reference, audit trails, and knowledge transfer.

## Recommended Documentation Artifacts

### 1. Markdown Summary (`canban_tasks.md`)
Human-readable overview of all tasks, their assignees, dependencies, and verification criteria.

**Format:**
```markdown
# Kanban Tasks for [Project Name]

## T1: [Title]
- Assignee: [profile]
- Dependencies: [list or "none"]
- Description: [task description]
- Verification: [how to confirm completion]

## T2: [Title]
- Assignee: [profile]
- Dependencies: [list or "none"] 
- Description: [task description]
- Verification: [how to confirm completion]
```

### 2. JSON Export (`tasks.json`)
Machine-readable format with UUIDs, dependencies, and status for programmatic access.

**Structure:**
```json
{
  "project": "[Project Name]",
  "tasks": [
    {
      "id": "[uuid]",
      "title": "[Task Title]",
      "assignee": "[profile]",
      "dependencies": ["[uuid1]", "[uuid2]"],
      "description": "[Full task description]",
      "verification": "[Verification criteria]",
      "status": "todo|in_progress|done|blocked"
    }
  ]
}
```

### 3. Plan File (`plan.json`)
The original task decomposition plan that guided the creation.

## When to Use This Practice

- **Complex workflows** with multiple dependencies (3+ tasks)
- **Long-running projects** expected to span multiple sessions
- **Knowledge transfer** scenarios where others need to understand the setup
- **Audit requirements** for traceability of work decomposition
- **Reproducibility** when similar setups might be needed in the future

## Example Implementation

From the whiskey wiki Obsidian setup (session 2026-05-11):
- Created `/home/mataanek/.hermes/hermes-agent/kanban_tasks.md` - markdown summary
- Created `/home/mataanek/.hermes/hermes-agent/whiskey_kanban_tasks.json` - JSON format
- Used `/home/mataanek/.hermes/plans/obsidian_whiskey_setup.json` as guiding plan

## Benefits

1. **Verification**: Confirms all expected tasks were created correctly
2. **Dependency Tracking**: Makes dependency mappings explicit and checkable
3. **Reproducibility**: Enables recreating or adjusting the board if needed
4. **Audit Trail**: Provides traceability for reviews or compliance
5. **Knowledge Preservation**: Captures the decomposition rationale for future reference

## Quick Reference Template

```markdown
# Kanban Tasks for [DESCRIPTION]

## T1: [TITLE]
- Assignee: [ops|writer|analyst|researcher|reviewer|etc]
- Dependencies: none
- Description: [FULL DESCRIPTION FROM PLAN]
- Verification: [HOW TO CONFIRM DONE]

## T2: [TITLE]  
- Assignee: [PROFILE]
- Dependencies: T1
- Description: [FULL DESCRIPTION FROM PLAN]
- Verification: [HOW TO CONFIRM DONE]
```