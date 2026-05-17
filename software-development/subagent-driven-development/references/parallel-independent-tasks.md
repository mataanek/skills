# Parallel Independent Tasks Pattern

## Overview
When tasks are completely independent (no shared files, no sequential dependencies), they can be dispatched in parallel using multiple `delegate_task` calls in the same controller session. This reduces total wall-clock time by overlapping execution.

## When to Use
- Tasks have no overlapping file modifications
- Tasks don't depend on each other's outputs
- Each task has a clear, self-contained goal
- You want to minimize total execution time

## Implementation Pattern
Instead of processing tasks sequentially in a loop, dispatch all independent tasks upfront:

```python
# Dispatch all independent tasks in parallel
futures = []
for task in independent_tasks:
    future = delegate_task(
        goal=task.goal,
        context=task.context,
        toolsets=task.toolsets,
        # Note: delegate_task is synchronous, but we can start them quickly
        # and let them run in background processes
    )
    futures.append((future, task.id))

# Then collect results (this will wait for each to complete)
results = []
for future, task_id in futures:
    # In practice, you'd need to store the delegate_task results
    # and match them to task IDs
    result = collect_delegate_task_result(future)  # Pseudocode
    results.append((task_id, result))
```

## Key Considerations
1. **Toolset Isolation**: Ensure tasks don't conflict on shared resources (e.g., two agents trying to write to the same file)
2. **Context Size**: Each subagent gets full context - be mindful of token usage
3. **Error Handling**: Failures in one task don't affect others
4. **Result Collection**: You need to track which result belongs to which task

## Example from Practice
In a Hermes team session (2026-05-07), two independent tasks were executed in parallel:
- **Agent Hex**: Created `factorial.py` with recursive implementation and error handling
- **Agent Wux**: Created directory structure `test_project/{src,docs,tests}/` with placeholder files

Both tasks completed in approximately 50-53 seconds wall-clock time (vs ~100+ seconds sequential), demonstrating effective parallelization.

## Verification
After parallel execution, verify:
- All expected files were created
- Each agent stayed within their role boundaries
- No file conflicts or overwrites occurred
- Each task's success criteria were met independently