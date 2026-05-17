# Diagnosing Stuck Kanban Tasks - Session Findings

Based on the Obsidian setup session (May 11, 2026), here are specific patterns for diagnosing stuck Kanban tasks:

## Common Stuck States Observed

1. **Task shows "running" but no worker PID**
   - Task appears in `running` status in Kanban database
   - Worker PID field is null or empty
   - No actual process executing the task

2. **Empty workspace with minimal events**
   - Workspace directory exists (`/home/mataanek/.hermes/kanban/workspaces/<task_id>/`)
   - Contains only basic structure, no output files
   - Task events table shows only "created" and "claimed" events
   - No "started", "output", or "completed" events

3. **Expired claim lock**
   - Task claim has expired (check `expires` timestamp in database)
   - Current time exceeds claim expiration
   - Task remains stuck in "running" despite expired claim

## Diagnostic Commands Used

### Check task details:
```bash
hermes kanban show <task_id>
```
Look for:
- `worker_pid`: Should be non-null if work is in progress
- `status`: Should transition from claimed → running → done
- `expires`: Timestamp for claim expiration

### Inspect workspace:
```bash
ls -la /home/mataanek/.hermes/kanban/workspaces/<task_id>/
find /home/mataanek/.hermes/kanban/workspaces/<task_id>/ -type f
```
Look for any output files, logs, or results.

### Verify gateway status:
```bash
ps aux | grep hermes.*gateway
```
Should show a running gateway process.

### Check task events (if direct DB access):
```bash
sqlite3 /home/mataanek/.hermes/kanban.db "SELECT * FROM task_events WHERE task_id = '<task_id>' ORDER BY timestamp;"
```
Look for event sequence beyond just created/claimed.

## Resolution Patterns Observed

1. **Reclaim when worker PID is null/stale**
   - Use `hermes kanban reclaim <task_id>` to reset to ready state
   - This kills any stale claim and allows fresh worker assignment

2. **Reassign if profile consistently fails**
   - Try different specialist profile if current one keeps failing
   - Use `hermes kanban reassign <task_id> <new-profile> --reclaim`

3. **Manual completion for blocking tasks**
   - If task is blocked on external factors, complete manually with result
   - Use `hermes kanban complete <task_id> --result "manual completion reason"`

## Prevention Guidelines

1. **Always verify worker spawning**
   - After claiming task, check that a worker process actually starts
   - Don't assume claiming = work started

2. **Monitor early progress**
   - Check workspace for initial output within 30-60 seconds of claim
   - Lack of early output often indicates worker failed to start

3. **Validate dependencies before expecting progress**
   - For tasks with parents, ensure all parents are complete
   - Don't expect work on blocked tasks
