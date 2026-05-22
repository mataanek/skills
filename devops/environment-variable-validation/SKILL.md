---
name: environment-variable-validation
description: Validate that environment variables (especially URLs, ports, and credentials) point to the correct running services. Prevents cron job failures, authentication errors, and misconfigured integrations caused by outdated or incorrect .env values.
---

# Environment Variable Validation Skill

## Purpose
Validate that environment variables (especially URLs, ports, and credentials) point to the correct running services. Prevents cron job failures, authentication errors, and misconfigured integrations caused by outdated or incorrect .env values.

## When to Use
- After deploying or restarting services (Docker, local processes, cloud endpoints).
- When automated scripts (cron jobs, backups, data collectors) fail with authentication or connection errors.
- Before trusting a configuration that was manually edited or copied from another environment.

## Steps
1. **Identify the service** referenced by the environment variable (e.g., `FRESHRSS_GREADER_URL`, `NETATMO_USERNAME`).
2. **Determine the actual endpoint**:
   - For Docker services: run `docker ps` and inspect the `PORTS` column to see host‑port mappings.
   - For local services: check listening ports with `ss -tlnp` or `netstat -tlnp`.
   - For cloud services: verify the hostname and any required path prefixes from the provider’s documentation.
3. **Extract the current value** from the environment file (usually `~/.hermes/.env` or a service‑specific config).
4. **Compare**:
   - Does the host/IP match (`localhost` vs `127.0.0.1` vs service name)?
   - Does the port match the host‑side port from `docker ps`?
   - Does the path prefix exist (e.g., `/api/greader.php`)?
5. **Update if mismatched**:
   - Edit the `.env` file with the correct value.
   - Preserve any required formatting (quotes, no trailing spaces).
6. **Validate the fix**:
   - Run a quick test (e.g., `curl -s <url>/health` or the script that uses the variable).
   - Confirm the command returns a successful status (HTTP 200, expected JSON, etc.).
7. **Document the change** (optional): add a comment in `.env` noting the date and reason for the update.

## Pitfalls & How to Avoid Them
- **Assuming default ports**: Many containers map internal ports to random host ports; always check `docker ps`.
- **Ignoring path prefixes**: A service may be mounted under a sub‑path (e.g., `/api/`). Verify the full URL.
- **Overlooking credentials**: If the variable includes username/password, ensure they are still valid (not expired or rotated).
- **Editing the wrong file**: Hermes may load `.env` from the home directory; verify you are editing the active file (`~/.hermes/.env`).
- **Skipping validation**: After changing a variable, always run a quick test; otherwise the cron job may still fail.

## Example: FreshRSS URL Fix
Given the variable `FRESHRSS_GREADER_URL="http://localhost:8080/api/greader.php"` but the FreshRSS container is exposed on host port 8081:

1. `docker ps` shows `0.0.0.0:8081->80/tcp` for the `freshrss/freshrss` container.
2. The correct host URL is `http://localhost:8081/api/greader.php`.
3. Update `.env`:
   ```bash
   sed -i 's|http://localhost:8080/api/greader.php|http://localhost:8081/api/greader.php|' ~/.hermes/.env
   ```
4. Validate:
   ```bash
   curl -s http://localhost:8081/api/greader.php/accounts/ClientLogin -X POST -d "Email=mataanek&Passwd=Misanthrope-01"
   ```
   Should return `SID=...` and `Auth=...` tokens.

## References
- See `references/docker-port-check.md` for a quick guide on reading `docker ps` output.
- See `scripts/validate-env-url.sh` for a reusable verification script.

## Related Skills
- `cronjob` – for scheduling validation runs.
- `netatmo-control` – another service that often requires URL/port checks.
- `hermes-agent` – for general Hermes configuration practices.

---
*Auto‑generated from session where the morning‑news‑digest cron failed due to a stale FreshRSS port in .env.*