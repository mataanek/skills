# Handling Hermes CLI Timeouts and Fallbacks

When calling `hermes -z '<prompt>'` in a script, always set a timeout (e.g., 30 seconds) and provide a fallback mechanism in case the command fails or times out.

Example using subprocess in Python:

```python
import subprocess
import shlex

prompt = "..."
escaped_prompt = prompt.replace("'", "'\\''")
try:
    result = subprocess.run(
        ["hermes", "-z", escaped_prompt],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        print(f"Hermes CLI error: {result.stderr}", flush=True)
        raise subprocess.CalledProcessError(result.returncode, "hermes")
    output = result.stdout.strip()
    if not output:
        raise ValueError("Empty output from hermes CLI")
except Exception as e:
    print(f"Using fallback due to: {e}", flush=True)
    # fallback logic here
```

For the freshrss digest, the fallback is a simple grouping by category.