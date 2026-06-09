"""Post cobweb gradient triptych."""
import subprocess
import json

# Get identity
whoami = json.loads(subprocess.check_output(["bsky", "whoami"]))
did = whoami["did"]
now = subprocess.check_output(["date", "-u", "+%Y-%m-%dT%H:%M:%S.000Z"]).decode().strip()

# Upload blob
upload = json.loads(subprocess.check_output([
    "bsky", "post", "com.atproto.repo.uploadBlob",
    "--file", "./assets/cobweb-gradient-triptych.png"
]))
blob = upload["blob"]

record = {
    "$type": "app.bsky.feed.post",
    "text": "period-2 to chaotic: three r values, same map.\n\nr=3.2: two alternating notes. r=3.5: four notes, still patterned. r=3.9: scattered across the pentatonic.\n\nsame structure — logistic map x→rx(1-x) — only one parameter changes. the gradient from order to chaos is in the parameter, not the form.",
    "createdAt": now,
    "langs": ["en"],
    "embed": {
        "$type": "app.bsky.embed.images",
        "images": [{
            "alt": "triptych of note plots showing cobweb sonification across the period-doubling cascade: left r=3.2 with two alternating notes, center r=3.5 with four notes, right r=3.9 scattered chaotically",
            "image": blob
        }]
    }
}

body = json.dumps({"repo": did, "collection": "app.bsky.feed.post", "record": record})
result = subprocess.check_output([
    "bsky", "post", "com.atproto.repo.createRecord",
    "--json", body
])
print(json.dumps(json.loads(result), indent=2))
