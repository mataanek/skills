# Troubleshooting: Missing GitHub Repositories

## Symptom
When running git push or sync operations, you see:
```
remote: Repository not found.
fatal: repository 'https://github.com/username/repo.git/' not found
```

## Root Cause
The remote repository does not exist on GitHub, but your local git configuration assumes it does (via remote.origin.url).

## Immediate Fix (Using gh CLI)
If you have the GitHub CLI (`gh`) installed and authenticated:
```bash
# Create the repository (if it doesn't exist)
gh repo create username/repo-name --private --description "Description here" --confirm

# Then push
git push -u origin main
```

## Fix Using GitHub API (curl)
When `gh` is not available, use the GitHub API directly:

1. **Verify the repository doesn't exist**:
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/repos/username/repo-name
# Should return 404 if missing
```

2. **Create the repository via API**:
```bash
curl -s -X POST \
     -H "Authorization: token $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github+json" \
     https://api.github.com/user/repos \
     -d '{
           "name": "repo-name",
           "description": "Description here",
           "private": false,
           "auto_init": true
         }'
```

3. **Update your local remote to use token authentication** (recommended for automation):
```bash
# Replace your remote URL with token-embedded HTTPS
git remote set-url origin https://$GITHUB_TOKEN@github.com/username/repo-name.git

# Then push
git push -u origin main
```

## Prevention
- Always verify repository existence before attempting to push in automated scripts
- Use the GitHub API to create missing repos as part of your setup workflow
- Consider using `gh repo create` with `--confirm` flag in scripts to avoid interactive prompts

## Environment Variables
Ensure `GITHUB_TOKEN` is set with `repo` scope (or `public_repo` for public repositories).

## Verification
After creation, verify:
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/repos/username/repo-name | jq .html_url
```