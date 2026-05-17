# Cron Job Delegation Guidance

Per the Hermes team workflow (nix/hex/wux), cron job management falls under wux's responsibilities as it involves precise file operations and system configuration maintenance.

## When to Delegate Cron Job Tasks to wux

Delegate to wux when:
- Creating, modifying, or deleting cron jobs
- Verifying cron job schedules match user requirements
- Troubleshooting cron job execution issues
- Checking cron job logs or status
- Any operation involving the `cronjob` tool

## Example Delegation Pattern

When a user requests a cron job change or reports an issue with scheduled tasks:

**Nix (Task Framing):**
- Understand the user's scheduling requirement (e.g., "briefings at 8AM and 4PM")
- Define the goal: "Update daily status update cron job to run at 08:00 and 16:00 daily"
- Provide context: Current schedule is 20:00, user wants 08:00/16:00
- Specify allowed operations: Use cronjob tool to update job schedule
- Define expected output: Confirmation of schedule update with new cron timing

**Delegation to wux:**
```python
delegate_task(
    goal="Update daily status update cron job to run at 08:00 and 16:00 daily",
    context="""CURRENT STATE:
    - Cron job ID: 73f621a4553b
    - Name: Daily status update
    - Current schedule: 0 20 * * * (8PM daily)
    - User requirement: Briefings at 8AM and 4PM daily
    
    REQUIRED CHANGE:
    - Update schedule from '0 20 * * *' to '0 8,16 * * *'
    - Verify update succeeds
    - Confirm next run times match expectation""",
    toolsets=['cronjob']
)
```

## Verification After wux Execution

After wux completes the cron job modification, nix should:
1. Verify the schedule change was applied correctly
2. Confirm next run times match user expectations
3. Ensure no unintended side effects
4. Report success in minimal format per rigorous-execution-protocol

## Why This Matters

Cron job modifications are system-level operations that can affect automation reliability. Following the delegation workflow ensures:
- Proper verification by execution specialist (wux)
- Context isolation for precise operations
- Adherence to user preference for no direct execution by nix
- Reliable automation that matches user requirements

## Related References

See `team-agents.md` for complete team structure and handoff rules.
See `rigorous-execution-protocol.md` for execution standards.