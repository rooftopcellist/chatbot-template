# Repository Configuration

This document explains how to configure repositories that will be automatically pulled into the `source-data/` directory when the chatbot starts.

## Overview

The chatbot can automatically clone and update git repositories to keep your source data up-to-date. This is useful for:

- Automatically pulling documentation repositories
- Keeping source data synchronized with remote sources
- Managing multiple data sources from different repositories

## Configuration

### Basic Setup

1. **Install GitPython dependency** (if not already installed):
   ```bash
   pip install GitPython>=3.1.40
   ```

2. **Configure repositories in `config.py`**:
   Edit the `TRAINING_REPOS` list in `config.py`:

   ```python
   TRAINING_REPOS = [
       {
           "url": "git@github.com:ansible/ansible-documentation.git",
           "name": "ansible-docs",  # Optional: custom directory name
           "branch": "main"  # Optional: specific branch
       }
   ]
   ```

### Configuration Options

Each repository configuration is a dictionary with the following options:

| Key | Required | Description | Example |
|-----|----------|-------------|---------|
| `url` | Yes | Git repository URL (SSH or HTTPS) | `"git@github.com:user/repo.git"` |
| `name` | No | Custom directory name in source-data/ | `"my-docs"` |
| `branch` | No | Specific branch to clone/pull | `"main"` or `"develop"` |

### Examples

#### Single Repository (Basic)
```python
TRAINING_REPOS = [
    {
        "url": "git@github.com:ansible/ansible-documentation.git"
    }
]
```

#### Single Repository (Full Configuration)
```python
TRAINING_REPOS = [
    {
        "url": "git@github.com:ansible/ansible-documentation.git",
        "name": "ansible-docs",
        "branch": "main"
    }
]
```

#### Multiple Repositories
```python
TRAINING_REPOS = [
    {
        "url": "git@github.com:ansible/ansible-documentation.git",
        "name": "ansible-docs",
        "branch": "main"
    },
    {
        "url": "https://github.com/example/other-docs.git",
        "name": "other-docs",
        "branch": "develop"
    }
]
```

## Behavior

### First Run (Clone)
- If a repository doesn't exist in `source-data/`, it will be cloned
- The directory name will be the repository name (from URL) or the custom `name` if specified
- If a `branch` is specified, that branch will be checked out

### Subsequent Runs (Update)
- If a repository already exists, it will be updated (git pull)
- If the repository has uncommitted changes, the update will be skipped with a warning
- If a different `branch` is specified in config, it will switch to that branch

### Error Handling
- If GitPython is not installed, a clear error message is shown
- If a repository fails to clone/update, a warning is shown but the chatbot continues
- Network issues or authentication problems are handled gracefully

## Testing

To test the repository configuration feature:

1. **Enable the test configuration** in `config.py`:
   ```python
   TRAINING_REPOS = [
       {
           "url": "git@github.com:ansible/ansible-documentation.git",
           "name": "ansible-docs",
           "branch": "main"
       }
   ]
   ```

2. **Run the chatbot**:
   ```bash
   python main.py
   ```

3. **Check the output** - you should see:
   ```
   Checking for configured repositories...
   Pulling 1 configured repositories...
   Processing repository: ansible-docs
     Cloning ansible-docs from git@github.com:ansible/ansible-documentation.git...
     ✓ Successfully cloned ansible-docs (branch: main)
   ```

4. **Verify the files** - check that `source-data/ansible-docs/` contains the repository files

## Troubleshooting

### GitPython Not Installed
```
Error: GitPython is not installed. Please install it to use repository features.
Run: pip install GitPython>=3.1.40
```
**Solution**: Install GitPython using pip

### SSH Key Issues
```
Failed to clone ansible-docs: Cmd('git') failed due to: exit code(128)
```
**Solution**: Ensure your SSH keys are set up correctly for the repository host

### Permission Issues
```
Failed to clone ansible-docs: Permission denied
```
**Solution**: Check repository permissions and authentication

### Repository Already Exists with Changes
```
Warning: ansible-docs has uncommitted changes, skipping update
```
**Solution**: This is normal behavior to prevent data loss. Commit or stash changes if you want updates to proceed.

## Directory Structure

After configuration, your directory structure will look like:

```
chatbot-template/
├── source-data/
│   ├── ansible-docs/          # Cloned repository
│   │   ├── docs/
│   │   ├── README.md
│   │   └── ...
│   ├── other-repo/            # Another repository if configured
│   └── handbook/              # Existing manual files
├── config.py
├── main.py
└── ...
```

## Security Considerations

- Use SSH URLs (`git@github.com:...`) for private repositories
- Ensure your SSH keys are properly secured
- Be cautious with repositories containing sensitive information
- Consider using read-only deploy keys for production environments
