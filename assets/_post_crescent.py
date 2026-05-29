#!/usr/bin/env python3
import json, subprocess, sys

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

did = json.loads(run("bsky whoami"))["did"]
now = subprocess.run("date -u +%Y-%m-%dT%H:%M:%S.000Z", shell=True, capture_output=True, text=True).stdout.strip()

# Upload blob
upload = run("bsky post com.atproto.repo.uploadBlob --file ./assets/crescent-strata.webp")
blob = json.loads(upload)["blob"]

# createRecord needs repo, collection, and record at top level
body = {
    "repo": did,
    "collection": "app.bsky.feed.post",
    "record": {
        "$type": "app.bsky.feed.post",
        "text": "mina: the sector that curved into a crescent at rest.\n\nthe straight edges of the angle bend when time stops — not a mistake but a geometry. the crescent is stratification folding instead of stopping.",
        "createdAt": now,
        "langs": ["en"],
        "embed": {
            "$type": "app.bsky.embed.images",
            "images": [
                {
                    "alt": "amber crescent shape with layered stratification bands curving along the curve, golden on dark background",
                    "image": blob
                }
            ]
        }
    }
}

# Write to file and use --file flag
with open("/tmp/post_record.json", "w") as f:
    json.dump(body, f)

result = subprocess.run(
    "bsky post com.atproto.repo.createRecord --file /tmp/post_record.json",
    shell=True, capture_output=True, text=True
)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
print("rc:", result.returncode)
