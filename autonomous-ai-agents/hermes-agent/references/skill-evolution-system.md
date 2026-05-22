# Skill Evolution and Performance Tracking System

## Overview

Hermes Agent includes an automatic skill performance tracking and evolution system that monitors skill executions, collects performance data, and suggests improvements without manual intervention.

## Components

### 1. Automatic Performance Tracking
- Integrated into `model_tools.py` in the `handle_function_call()` function
- Activates after duration_ms calculation and before post_tool_call hooks
- Only tracks tools in the "skills" toolset to avoid overhead on core operations
- Records both objective metrics (success/failure, execution time) and contextual data

### 2. Performance Data Storage
- Uses the existing ClawMem system via the memory tool
- Each record includes:
  - `skill_name`: Name of the executed skill
  - `timestamp`: ISO format timestamp of execution
  - `success`: Boolean indicating if the skill execution succeeded
  - `metrics`: Object containing:
    - `execution_time_ms`: Duration of skill execution
    - `toolset`: Toolset the skill belongs to (always "skills" for tracked skills)
  - `context`: Object containing:
    - `trigger`: How the skill was invoked (manual, automatic, etc.)
    - `function_name`: The specific tool function that was called
    - `safe_arguments`: Sanitized input parameters (for debugging)
    - `task_id`: Session task ID if available
    - `session_id`: Session identifier if available

### 3. Skill Evolution Tool
- Available as `hermes skills skill_evolve <skill_name>`
- Analyzes performance data for a specific skill
- Identifies trends and patterns in success/failure rates
- Suggests specific improvements based on historical data
- Can be run manually or scheduled via cron jobs

### 4. Performance Tracking Tool
- Available as `hermes skills track_skill_performance`
- Manual tool for recording skill performance data
- Primarily used for testing and validation of the tracking system
- Automatic tracking makes manual invocation rarely necessary

## Data Flow

1. Skill is executed via normal tool invocation
2. `handle_function_call()` in `model_tools.py` detects if tool is in "skills" toolset
3. If yes, performance tracking logic executes:
   - Calculates execution duration
   - Determines success based on tool result analysis
   - Collects contextual information
   - Formats data for ClawMem storage
   - Calls memory tool to store the record
4. Data persists in ClawMem across sessions
5. `skill_evolve` tool can read and analyze this data to generate insights

## Configuration

The system is active by default and requires no configuration to begin tracking.
To disable (not recommended), modify the tracking logic in `model_tools.py`.

## Usage Examples

### Viewing Skill Performance
```bash
hermes skills skill_evolve news-digest
```

### Manual Performance Recording (testing only)
```bash
hermes skills track_skill_performance --skill-name news-digest --success true --execution-time 1250
```

### Scheduling Regular Analysis
Add a cron job to regularly analyze underperforming skills:
```bash
hermes cron create "0 2 * * *"   # Every day at 2 AM
```
When prompted, provide: `hermes skills skill_evolve --analyze-all --threshold 0.8`

## Benefits

- **Zero Manual Overhead**: Tracking happens automatically during normal skill execution
- **Evidence-Based Improvements**: Evolution suggestions based on actual performance data
- **Early Warning System**: Detects declining performance before it impacts users
- **Continuous Learning**: System improves over time without external intervention
- **Transparency**: Performance data available for inspection and audit

## Implementation Notes

- Tracking is designed to be lightweight and fail-safe
- Errors in tracking do not affect the execution of the tracked skill
- Only skills toolset is tracked to avoid performance impact on core operations (terminal, file, etc.)
- Data structure is extensible for future enhancement
- Integrates seamlessly with existing memory and skills systems

## Related Files

- `model_tools.py`: Contains the automatic tracking implementation
- `scripts/skill_evolve.py`: Skill evolution analysis tool
- `scripts/track_skill_performance.py`: Performance tracking tool (manual)
- `~/.hermes/clawmem/`: Storage for performance records (managed by memory tool)

## Best Practices

- Trust the automatic system - no need to manually invoke tracking tools
- Use `skill_evolve` regularly to identify improvement opportunities
- Pay attention to skills with low success rates or increasing execution times
- Consider evolutionary suggestions when planning skill updates
- The system works best with sufficient data (minimum 5-10 executions for meaningful analysis)