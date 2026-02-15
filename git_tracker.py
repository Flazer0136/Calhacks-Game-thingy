import subprocess
from datetime import datetime
import os

def get_last_commit_time():
    """
    Get timestamp of last git commit in current repo.
    Returns: datetime object or None if no commits/not a repo
    """
    try:
        # Get latest Git commits 
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ct'],
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.stdout.strip():
            timestamp = int(result.stdout.strip())
            return datetime.fromtimestamp(timestamp)
        else:
            # No commits yet
            return None
            
    except subprocess.CalledProcessError:
        # Not a git repo or git not installed
        return None
    except FileNotFoundError:
        # git command not found
        return None

def hours_since_last_commit():
    """
    Calculate hours since last commit.
    Returns: float (hours) or 0 if no commits/errors
    """
    last_commit = get_last_commit_time()
    
    if last_commit is None:
        # No commits yet, return 0 (no decay)
        return 0.0
    
    now = datetime.now()
    time_diff = now - last_commit
    hours = time_diff.total_seconds() / 3600
    
    return max(0, hours)  # Never negative

def get_total_commits():
    """
    Get total number of commits in repo.
    Returns: int (commit count)
    """
    try:
        result = subprocess.run(
            ['git', 'rev-list', '--count', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return int(result.stdout.strip())
    except:
        return 0

def is_git_repo():
    """Check if current directory is a git repository"""
    try:
        subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            capture_output=True,
            check=True
        )
        return True
    except:
        return False

def get_commit_info():
    """
    Get detailed info about last commit.
    Returns: dict with message, author, date
    """
    try:
        # Get commit message
        message_result = subprocess.run(
            ['git', 'log', '-1', '--format=%s'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Get author
        author_result = subprocess.run(
            ['git', 'log', '-1', '--format=%an'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Get date (human readable)
        date_result = subprocess.run(
            ['git', 'log', '-1', '--format=%ar'],
            capture_output=True,
            text=True,
            check=True
        )
        
        return {
            'message': message_result.stdout.strip(),
            'author': author_result.stdout.strip(),
            'time_ago': date_result.stdout.strip()
        }
    except:
        return None
