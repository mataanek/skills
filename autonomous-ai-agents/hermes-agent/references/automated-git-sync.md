# Automated Git Synchronization for Hermes Directories

This document describes the automated synchronization system for Hermes directories (skills, wiki, scripts, workflows) with a Git repository.

## Overview

To ensure that Hermes directories are backed up and synchronized across devices, an automated Git synchronization system has been implemented. This system:

1. Tracks changes in four key directories:
   - `~/.hermes/skills` (branch: `skills`)
   - `~/.hermes/wiki` (branch: `wiki`)
   - `~/.hermes/scripts` (branch: `scripts`)
   - `~/.hermes/workflows` (branch: `workflows`)

2. Uses a cron job that runs every 6 hours (00:00, 06:00, 12:00, 18:00 UTC) to:
   - Fetch latest changes from the remote repository
   - Fast-forward local branches if they are behind
   - Commit local changes with an auto-sync timestamp
   - Push changes to the remote repository (with rebase on conflict if needed)

## Implementation Details

### Synchronization Script

The synchronization is handled by the script: `~/.hermes/scripts/sync_hermes_repos.sh`

Key features of the script:
- Uses `set -euo pipefail` for robust error handling
- Implements a `sync_repo` function that handles each directory/branch pair
- Properly handles branch checking, fetching, fast-forwarding, local change detection, committing, and pushing
- Includes automatic conflict resolution via `pull --rebase` when needed
- Provides logging with timestamps for debugging

### Cron Job

The synchronization is automated via a Hermes cron job:
- **Name**: `hermes-repo-sync`
- **Schedule**: `0 0,6,12,18 * * *` (every 6 hours)
- **Script**: `sync_hermes_repos.sh` (relative to `~/.hermes/scripts/`)
- **Agent**: `no_agent` (runs in a no-agent context for reliability)

### Authentication

The system uses SSH key authentication for secure Git operations:
- SSH key stored at: `/home/mataanek/.ssh/id_ed25519_github`
- Corresponding public key added to GitHub account
- SSH agent is started and key loaded before cron execution

### Repository Structure

All directories are synchronized to the same GitHub repository:
- URL: `git@github.com:mataanek/hermes-local.git`
- Each directory uses a separate branch to avoid conflicts:
  - `skills` branch for `~/.hermes/skills`
  - `wiki` branch for `~/.hermes/wiki`
  - `scripts` branch for `~/.hermes/scripts`
  - `workflows` branch for `~/.hermes/workflows`

## Usage Guidelines

### Making Changes

When making changes to any of the synchronized directories:
1. Make your changes as usual
2. The next cron run (within 6 hours) will automatically commit and push your changes
3. For immediate synchronization, you can run the script manually:
   ```bash
   ~/.hermes/scripts/sync_hermes_repos.sh
   ```

### Receiving Changes

Changes made to the repository from other devices or directly on GitHub will be pulled during the next cron run. To manually pull changes:
```bash
# For skills
cd ~/.hermes/skills && git checkout skills && git pull

# For wiki
cd ~/.hermes/wiki && git checkout wiki && git pull

# For scripts
cd ~/.hermes/scripts && git checkout scripts && git pull

# For workflows
cd ~/.hermes/workflows && git checkout workflows && git pull
```

### Troubleshooting

If the synchronization fails:
1. Check the cron job status: `hermes cron list`
2. Check the last run output in the cron job results
3. Verify SSH authentication: `ssh -T git@github.com`
4. Check that the synchronization script is executable: `ls -l ~/.hermes/scripts/sync_hermes_repos.sh`
5. Verify Java is installed (required for some operations): `java -version`

## Benefits

- **Automatic backup**: All changes are regularly backed up to GitHub
- **Cross-device synchronization**: Work on one device is available on others within 6 hours
- **Version history**: Complete history of all changes is maintained
- **Conflict minimization**: Separate branches for each directory reduce merge conflicts
- **Zero manual overhead**: No need to remember to run `git push`/`git pull` manually

## Customization

To change the synchronization schedule:
1. Edit the cron job: `hermes cron edit hermes-repo-sync`
2. Update the schedule field (uses standard cron syntax)

To change the synchronization script:
1. Modify `~/.hermes/scripts/sync_hermes_repos.sh`
2. The cron job will automatically use the updated script on its next run

## Security Considerations

- The SSH key used for synchronization should be kept secure
- The repository should be set to private if it contains sensitive information
- Regularly review the synchronized directories to ensure no unintended files are being tracked
- Consider adding a `.gitignore` file to each directory if there are files that should not be synchronized
