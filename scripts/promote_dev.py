import os
import base64
import requests

REPO = "Jarom-W/Anima"
PATH = "charts/second-app/env/dev/values.yaml"
BRANCH = f"ci/promote-dev-{os.environ['SHA']}"
SHA = os.environ["SHA"]
TOKEN = os.environ["GH_TOKEN"]

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# 1. Get file
url = f"https://api.github.com/repos/{REPO}/contents/{PATH}"
r = requests.get(url, headers=headers)
data = r.json()

file_sha = data["sha"]
content = base64.b64decode(data["content"]).decode()

# 2. Modify tag
lines = content.splitlines()
new_lines = []
for line in lines:
    if "tag:" in line:
        new_lines.append(f"  tag: {SHA}")
    else:
        new_lines.append(line)

new_content = "\n".join(new_lines)
encoded = base64.b64encode(new_content.encode()).decode()

# 3. Create branch (simple approach: same as main)
# (we’ll refine this later with real branch API)

# 4. Update file
update = {
    "message": f"promote dev image {SHA}",
    "content": encoded,
    "sha": file_sha
}

resp = requests.put(url, headers=headers, json=update)
print(resp.status_code, resp.text)
