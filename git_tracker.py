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
            return None
            
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None

def hours_since_last_commit():
    """
    Calculate hours since last commit.
    Returns: float (hours) or 0 if no commits/errors
    """
    last_commit = get_last_commit_time()
    
    if last_commit is None:
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
        # Commit message
        message_result = subprocess.run(
            ['git', 'log', '-1', '--format=%s'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Author
        author_result = subprocess.run(
            ['git', 'log', '-1', '--format=%an'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Get date
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


def get_git_graph(max_lines=8):
    """
    Get ASCII art git commit graph.
    Returns: string with graph or None
    """
    try:
        result = subprocess.run(
            ['git', 'log', '--graph', '--oneline', '--all', 
             f'--max-count={max_lines}', '--color=never'],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        if result.stdout.strip():
            return result.stdout.strip()
        return None
    except:
        return None
