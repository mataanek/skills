Daily cron job for status updates

- Job ID: 73f621a4553b
- Name: Daily status update
- Schedule: 0 20 * * * (every day at 20:00)
- Script: update-status.sh (located in ~/.hermes/scripts/)
- Appends timestamp, uptime, and load average to:
    - /home/mataanek/.hermes/wiki/personal/nix-status.md
    - /home/mataanek/.hermes/wiki/personal/mataanek-profile.md
- Enabled and scheduled via Hermes cronjob tool.

To manually run: /home/mataanek/.hermes/scripts/update-status.sh
To list cron jobs: hermes cronjob list