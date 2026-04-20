from pydriller import Repository
from statistics import mean
import re

issue_ids = [
    "LUCENE-12",
    "LUCENE-17",
    "LUCENE-701",
    "LUCENE-1200",
    "LUCENE-1799"
]

issue_to_commits = {}
all_commit_hashes = set()
commit_data = []

for commit in Repository('.').traverse_commits():
    if commit.merge:
        continue

    for issue in issue_ids:
        pattern = r'\b' + issue + r'\b'
        if re.search(pattern, commit.msg):
            issue_to_commits.setdefault(issue, set()).add(commit.hash)
            all_commit_hashes.add(commit.hash)


print("\nIssue → commits mapping:")
for issue in issue_ids:
    count = len(issue_to_commits.get(issue, []))
    print(issue, "→", count)

print("Total unique commits found:", len(all_commit_hashes))


for commit in Repository('.').traverse_commits():
    if commit.hash not in all_commit_hashes:
        continue

    dmm_size = commit.dmm_unit_size if commit.dmm_unit_size is not None else 0
    dmm_complexity = commit.dmm_unit_complexity if commit.dmm_unit_complexity is not None else 0
    dmm_interface = commit.dmm_unit_interfacing if commit.dmm_unit_interfacing is not None else 0

    commit_data.append({
        "files": len(commit.modified_files),
        "dmm_size": dmm_size,
        "dmm_complexity": dmm_complexity,
        "dmm_interface": dmm_interface
    })

print("Commits after processing:", len(commit_data))


if len(commit_data) == 0:
    print("\n❌ No valid commits found.")
    print("👉 Likely reasons:")
    print("- Issue IDs not present in commit messages")
    print("- Very old issues (Lucene history limitation)")
    exit()

avg_files = mean(c["files"] for c in commit_data)
avg_size = mean(c["dmm_size"] for c in commit_data)
avg_complexity = mean(c["dmm_complexity"] for c in commit_data)
avg_interface = mean(c["dmm_interface"] for c in commit_data)




print("\n===== FINAL RESULTS =====")
print("Total unique commits:", len(commit_data))
print("Average files changed:", avg_files)
print("\nDMM Averages:")
print("Size:", avg_size)
print("Complexity:", avg_complexity)
print("Interface:", avg_interface)