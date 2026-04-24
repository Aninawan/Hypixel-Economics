import requests
import json
import os
from datetime import datetime, timezone

os.makedirs("data", exist_ok=True)

headers = {"User-Agent": "skyblock-analytics-dashboard/1.0"}

def fetch(url, label):
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        data = r.json()
        print(f"OK: {label} ({len(str(data))} bytes)")
        return data
    except Exception as e:
        print(f"FAILED: {label} — {e}")
        return None

baz = fetch("https://api.hypixel.net/v2/skyblock/bazaar", "bazaar")
if baz:
    with open("data/bazaar.json", "w") as f:
        json.dump(baz, f)

ah = fetch("https://api.hypixel.net/v2/skyblock/auctions_ended", "auctions_ended")
if ah:
    with open("data/auctions_ended.json", "w") as f:
        json.dump(ah, f)

meta = {
    "last_updated": datetime.now(timezone.utc).isoformat(),
    "bazaar_ok": baz is not None,
    "auctions_ok": ah is not None,
}
with open("data/meta.json", "w") as f:
    json.dump(meta, f)

print("Done.", meta)
