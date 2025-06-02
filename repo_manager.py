"""
Repository manager module for handling git repository operations.
"""

import os
import shutil
from typing import List, Dict, Optional
from rich.console import Console
import config

try:
    from git import Repo, GitCommandError
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False


class RepoManager:
    """
    Manages git repository operations for training data.
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize the repository manager."""
        self.console = console or Console()
        self.training_data_dir = config.DOCS_DIR

    def pull_configured_repos(self) -> bool:
        """
        Pull all configured repositories into the source-data directory.

        Returns:
            bool: True if all operations succeeded, False if any failed
        """
        if not GIT_AVAILABLE:
            self.console.print("[bold red]Error: GitPython is not installed. Please install it to use repository features.[/bold red]")
            self.console.print("Run: pip install GitPython>=3.1.40")
            return False

        if not config.TRAINING_REPOS:
            self.console.print("[dim]No repositories configured for automatic pulling.[/dim]")
            return True

        self.console.print(f"[bold blue]Pulling {len(config.TRAINING_REPOS)} configured repositories...[/bold blue]")

        success = True
        for repo_config in config.TRAINING_REPOS:
            if not self._pull_single_repo(repo_config):
                success = False

        return success

    def _pull_single_repo(self, repo_config: Dict) -> bool:
        """
        Pull a single repository based on its configuration.

        Args:
            repo_config (Dict): Repository configuration containing url, name, branch

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            url = repo_config.get("url")
            if not url:
                self.console.print("[bold red]Error: Repository URL is required[/bold red]")
                return False

            # Determine repository name
            repo_name = repo_config.get("name")
            if not repo_name:
                # Extract name from URL
                repo_name = url.split("/")[-1].replace(".git", "")

            # Determine target directory
            target_dir = os.path.join(self.training_data_dir, repo_name)

            # Determine branch
            branch = repo_config.get("branch")

            self.console.print(f"Processing repository: [bold]{repo_name}[/bold]")

            if os.path.exists(target_dir):
                # Repository exists, try to update it
                return self._update_existing_repo(target_dir, repo_name, branch)
            else:
                # Repository doesn't exist, clone it
                return self._clone_new_repo(url, target_dir, repo_name, branch)

        except Exception as e:
            self.console.print(f"[bold red]Error processing repository {repo_config.get('url', 'unknown')}: {str(e)}[/bold red]")
            return False

    def _clone_new_repo(self, url: str, target_dir: str, repo_name: str, branch: Optional[str] = None) -> bool:
        """
        Clone a new repository.

        Args:
            url (str): Repository URL
            target_dir (str): Target directory path
            repo_name (str): Repository name for display
            branch (Optional[str]): Specific branch to clone

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.console.print(f"  Cloning [bold]{repo_name}[/bold] from {url}...")

            # Ensure parent directory exists
            os.makedirs(os.path.dirname(target_dir), exist_ok=True)

            # Clone repository
            if branch:
                repo = Repo.clone_from(url, target_dir, branch=branch)
                self.console.print(f"  ✓ Successfully cloned [bold]{repo_name}[/bold] (branch: {branch})")
            else:
                repo = Repo.clone_from(url, target_dir)
                self.console.print(f"  ✓ Successfully cloned [bold]{repo_name}[/bold]")

            return True

        except GitCommandError as e:
            self.console.print(f"  [bold red]✗ Failed to clone {repo_name}: {str(e)}[/bold red]")
            # Clean up partial clone if it exists
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            return False
        except Exception as e:
            self.console.print(f"  [bold red]✗ Unexpected error cloning {repo_name}: {str(e)}[/bold red]")
            # Clean up partial clone if it exists
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            return False

    def _update_existing_repo(self, target_dir: str, repo_name: str, branch: Optional[str] = None) -> bool:
        """
        Update an existing repository.

        Args:
            target_dir (str): Repository directory path
            repo_name (str): Repository name for display
            branch (Optional[str]): Specific branch to checkout/pull

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.console.print(f"  Updating existing [bold]{repo_name}[/bold]...")

            # Open existing repository
            repo = Repo(target_dir)

            # Check if repository is dirty
            if repo.is_dirty():
                self.console.print(f"  [bold yellow]Warning: {repo_name} has uncommitted changes, skipping update[/bold yellow]")
                return True

            # Fetch latest changes
            origin = repo.remotes.origin
            origin.fetch()

            # Switch to specified branch if provided
            if branch:
                try:
                    # Check if branch exists locally
                    if branch in [head.name for head in repo.heads]:
                        repo.heads[branch].checkout()
                    else:
                        # Create local branch tracking remote branch
                        repo.create_head(branch, origin.refs[branch])
                        repo.heads[branch].checkout()

                    self.console.print(f"  Switched to branch: {branch}")
                except Exception as e:
                    self.console.print(f"  [bold yellow]Warning: Could not switch to branch {branch}: {str(e)}[/bold yellow]")

            # Pull latest changes
            current_branch = repo.active_branch.name
            origin.pull(current_branch)

            self.console.print(f"  ✓ Successfully updated [bold]{repo_name}[/bold]")
            return True

        except GitCommandError as e:
            self.console.print(f"  [bold red]✗ Failed to update {repo_name}: {str(e)}[/bold red]")
            return False
        except Exception as e:
            self.console.print(f"  [bold red]✗ Unexpected error updating {repo_name}: {str(e)}[/bold red]")
            return False

    def add_repo_config(self, url: str, name: Optional[str] = None, branch: Optional[str] = None) -> Dict:
        """
        Helper method to create a repository configuration dictionary.

        Args:
            url (str): Repository URL
            name (Optional[str]): Custom directory name
            branch (Optional[str]): Specific branch

        Returns:
            Dict: Repository configuration dictionary
        """
        config = {"url": url}
        if name:
            config["name"] = name
        if branch:
            config["branch"] = branch
        return config
