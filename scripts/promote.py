from pathlib import Path
import sys
import yaml
import subprocess
import os

source = sys.argv[1]   # dev
dest = sys.argv[2]     # staging

repo_root = Path.cwd()

source_file = repo_root / f"charts/second-app/env/{source}/values.yaml"
dest_file = repo_root / f"charts/second-app/env/{dest}/values.yaml"

# 1. read source
with open(source_file) as f:
    source_values = yaml.safe_load(f)

tag = source_values["image"]["tag"]

print(f"Promoting image {tag} from {source} → {dest}")

# 2. create branch
branch = f"promote-{source}-to-{dest}-{tag}"

subprocess.run(["git", "checkout", "-b", branch], check=True)

# 3. update destination file
with open(dest_file) as f:
    dest_values = yaml.safe_load(f)

dest_values["image"]["tag"] = tag

with open(dest_file, "w") as f:
    yaml.safe_dump(dest_values, f, sort_keys=False)

# 4. commit
subprocess.run(["git", "add", str(dest_file)], check=True)
subprocess.run(["git", "commit", "-m", f"promote {tag} {source} → {dest}"], check=True)

# 5. push branch
subprocess.run(["git", "push", "-u", "origin", branch], check=True)

print(f"""
Created promotion branch: {branch}

Next step:
Open PR from {branch} → main
""")
import sys
import yaml

source = sys.argv[1]
dest = sys.argv[2]

source_file = Path(f"charts/second-app/env/{source}/values.yaml")
dest_file = Path(f"charts/second-app/env/{dest}/values.yaml")

with open(source_file) as f:
    source_values = yaml.safe_load(f)

with open(dest_file) as f:
    dest_values = yaml.safe_load(f)

dest_values["image"]["tag"] = source_values["image"]["tag"]

with open(dest_file, "w") as f:
    yaml.safe_dump(dest_values, f, sort_keys=False)

print(
    f"Promoted {source_values['image']['tag']} "
    f"from {source} to {dest}"
)
