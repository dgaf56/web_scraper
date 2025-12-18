import os
import json
import time
import hashlib
import requests

# ------------------ SETTINGS (you edit these) ------------------
QUERY = "cats"          # what you want to search
MAX_NEW = 10            # how many NEW (non-duplicate) images to save
SLEEP = 0.25            # small delay between downloads

OUT_DIR = "images"      # folder inside your project
HASH_DB = "hashes.json" # stores hashes so duplicates are skipped across runs

SERPER_ENDPOINT = "https://google.serper.dev/images"
SERPER_KEY = os.getenv("SERPER_KEY")  # you set this in CMD
# ---------------------------------------------------------------

def sha256_bytes(b: bytes) -> str:
    """Fingerprint of the file content (bytes). Same bytes -> same hash."""
    return hashlib.sha256(b).hexdigest()

def load_hashes() -> set[str]:
    """Load previously seen hashes so we can skip duplicates across runs."""
    if not os.path.exists(HASH_DB):
        return set()
    with open(HASH_DB, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_hashes(hashes: set[str]) -> None:
    """Save hashes back to disk (your scraper's memory)."""
    with open(HASH_DB, "w", encoding="utf-8") as f:
        json.dump(sorted(hashes), f, indent=2)

def search_image_urls(query: str, num: int = 100) -> list[str]:
    """
    SEARCH stage:
    Ask Serper for image results and return a list of direct image URLs.
    """
    if not SERPER_KEY:
        raise RuntimeError(
            "SERPER_KEY is not set. In CMD: set SERPER_KEY=your_real_key"
        )

    headers = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": num}  # num = how many results Serper returns

    r = requests.post(SERPER_ENDPOINT, headers=headers, json=payload, timeout=20)
    r.raise_for_status()
    data = r.json()

    urls = []
    for item in data.get("images", []):
        url = item.get("imageUrl")
        if url:
            urls.append(url)
    return urls

def download_image(url: str) -> tuple[bytes, str] | None:
    """
    DOWNLOAD stage:
    Download image bytes. Return (bytes, content_type) or None if it fails.
    """
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()

        ctype = r.headers.get("Content-Type", "")
        if "image" not in ctype:
            return None

        return r.content, ctype
    except requests.RequestException:
        return None

def pick_extension(content_type: str) -> str:
    """Best-effort file extension based on Content-Type header."""
    ct = content_type.lower()
    if "jpeg" in ct or "jpg" in ct:
        return "jpg"
    if "png" in ct:
        return "png"
    if "webp" in ct:
        return "webp"
    if "gif" in ct:
        return "gif"
    return "bin"

def main():
    # SAVE stage prep: make sure folder exists
    os.makedirs(OUT_DIR, exist_ok=True)

    known = load_hashes()
    print(f"Loaded {len(known)} known hashes")

    # Get a bunch of candidates because some fail or are duplicates
    urls = search_image_urls(QUERY, num=100)
    print(f"Found {len(urls)} candidate image URLs for '{QUERY}'")

    saved = 0
    for idx, url in enumerate(urls, start=1):
        if saved >= MAX_NEW:
            break

        result = download_image(url)
        if not result:
            continue

        img_bytes, ctype = result
        h = sha256_bytes(img_bytes)

        # DE-DUPE stage
        if h in known:
            continue

        ext = pick_extension(ctype)
        filename = f"{QUERY}_{saved:03d}_{h[:10]}.{ext}"
        path = os.path.join(OUT_DIR, filename)

        with open(path, "wb") as f:
            f.write(img_bytes)

        known.add(h)
        saved += 1
        print(f"[{idx}/{len(urls)}] Saved: {path}")

        time.sleep(SLEEP)

    save_hashes(known)
    print(f"Done. Saved {saved} NEW images into '{OUT_DIR}/'. Duplicates skipped.")

if __name__ == "__main__":
    main()
