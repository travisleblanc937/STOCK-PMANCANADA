# Builds images.json: {product handle: first photo URL} from the public pokemancanada.com product feed.
import json, urllib.request, time
out, page = {}, 1
while True:
    url = f"https://www.pokemancanada.com/products.json?limit=250&page={page}"
    req = urllib.request.Request(url, headers={"User-Agent": "stock-page-images/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        products = json.load(r).get("products", [])
    if not products:
        break
    for p in products:
        imgs = p.get("images") or []
        if p.get("handle") and imgs and imgs[0].get("src"):
            out[p["handle"]] = imgs[0]["src"]
    page += 1
    time.sleep(1)
if len(out) < 10:
    raise SystemExit(f"Only {len(out)} images found; leaving images.json unchanged")
with open("images.json", "w") as f:
    json.dump(out, f, separators=(",", ":"), sort_keys=True)
print(len(out), "images")
