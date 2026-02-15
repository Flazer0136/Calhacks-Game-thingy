from git_tracker import (
    is_git_repo, 
    get_last_commit_time, 
    hours_since_last_commit,
    get_total_commits,
    get_commit_info
)

print("🔍 Git Repository Check")
print(f"Is git repo: {is_git_repo()}")
print(f"Total commits: {get_total_commits()}")

print("\n⏰ Last Commit Info")
last_commit = get_last_commit_time()
if last_commit:
    print(f"Last commit: {last_commit}")
    print(f"Hours since: {hours_since_last_commit():.2f}")
    
    info = get_commit_info()
    if info:
        print(f"Message: {info['message']}")
        print(f"Author: {info['author']}")
        print(f"Time ago: {info['time_ago']}")
else:
    print("No commits found")

print("\n💡 For memory decay:")
hours = hours_since_last_commit()
if hours < 24:
    print(f"✅ Pet memory intact (only {hours:.1f}h since commit)")
elif hours < 48:
    print(f"⚠️  Pet starting to forget ({hours:.1f}h)")
else:
    print(f"❌ Pet has forgotten a lot ({hours:.1f}h = {hours/24:.1f} days!)")
