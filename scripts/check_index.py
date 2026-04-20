import json
with open('skills-index.json', encoding='utf-8') as f:
    idx = json.load(f)
total = idx["total_count"]
print("total_count:", total)
print()
for cat, info in idx["by_category"].items():
    count = len(info["skills"])
    print(f"  {cat:25s}: {count:3d} skills")
