#!/usr/bin/env python3
"""Cross-Poster — generates one topic and posts adapted content to all 4 IG accounts."""

import os, sys, json, time, random
from urllib.parse import quote
from dotenv import load_dotenv
import requests

load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GRAPH_BASE = "https://graph.facebook.com/v21.0"

ACCOUNTS = [
    {
        "name": "thegurukul.online",
        "token_env": "GURUKUL_TOKEN",
        "ig_id_env": "GURUKUL_IG_ID",
        "niche": "Indian ancient wisdom and gurukul education",
        "image_style": "ancient Indian gurukul forest ashram, golden sunrise, Vedic atmosphere, cinematic",
    },
    {
        "name": "ooumph_official",
        "token_env": "OFFICIAL_TOKEN",
        "ig_id_env": "OFFICIAL_IG_ID",
        "niche": "Web3, OoumphCoin, and crypto/blockchain",
        "image_style": "futuristic Web3 blockchain digital art, glowing coins, neon blue purple, tech aesthetic",
    },
    {
        "name": "bharat.vistas",
        "token_env": "VISTAS_TOKEN",
        "ig_id_env": "VISTAS_IG_ID",
        "niche": "Indian travel photography and cultural exploration",
        "image_style": "breathtaking Indian landscape, vibrant colors, golden hour, temples, cinematic photography",
    },
    {
        "name": "muggedmoments",
        "token_env": "MUGGED_TOKEN",
        "ig_id_env": "MUGGED_IG_ID",
        "niche": "coffee culture and aesthetic lifestyle",
        "image_style": "cozy aesthetic coffee shop, latte art, warm light, minimalist, Instagram aesthetic",
    },
]


def groq_generate(prompt: str, model: str = "llama-3.3-70b-versatile", max_tokens: int = 150) -> str:
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.9,
    }
    resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def generate_image(style_prompt: str) -> str:
    """Return a Pollinations URL for the image."""
    seed = random.randint(1, 99999)
    encoded = quote(f"{style_prompt}, high quality, 1:1 aspect ratio")
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1080&nologo=true&seed={seed}"


def post_to_account(account: dict, caption: str, image_url: str) -> bool:
    token = os.environ.get(account["token_env"], "")
    ig_id = os.environ.get(account["ig_id_env"], "")

    if not token or not ig_id:
        print(f"  ⚠️  Missing secrets for {account['name']} ({account['token_env']}/{account['ig_id_env']})")
        return False

    # Create container
    url = f"{GRAPH_BASE}/{ig_id}/media"
    r = requests.post(url, data={"image_url": image_url, "caption": caption, "access_token": token}, timeout=30)
    if r.status_code != 200:
        print(f"  ✗ Container failed for {account['name']}: {r.json().get('error', {}).get('message', r.text)}")
        return False
    creation_id = r.json().get("id")

    time.sleep(3)

    # Publish
    pub_url = f"{GRAPH_BASE}/{ig_id}/media_publish"
    r2 = requests.post(pub_url, data={"creation_id": creation_id, "access_token": token}, timeout=30)
    if r2.status_code != 200:
        print(f"  ✗ Publish failed for {account['name']}: {r2.json().get('error', {}).get('message', r2.text)}")
        return False

    new_id = r2.json().get("id")
    print(f"  ✓ Posted to @{account['name']}: {new_id}")
    return True


def main():
    print("[Cross-Poster] Starting cross-platform post")

    # Generate base topic
    print("  Generating base topic...")
    base_topic = groq_generate(
        "Generate ONE compelling, universal topic that can be adapted for Instagram posts across "
        "these niches: ancient wisdom/education, Web3/crypto, Indian travel photography, and coffee culture. "
        "The topic should be about growth, discovery, or finding your unique path. "
        "Return ONLY the topic in 1 sentence.",
        max_tokens=60,
    )
    print(f"  Base topic: \"{base_topic}\"")

    # Generate image (one universal image with some versatility)
    img_style = "inspiring journey concept art, vibrant colors, cinematic composition, high quality"
    image_url = generate_image(img_style)
    print(f"  Image URL: {image_url[:80]}...")

    results = []
    for i, account in enumerate(ACCOUNTS):
        print(f"\n  [{i+1}/4] Adapting for @{account['name']} ({account['niche']})...")
        try:
            caption = groq_generate(
                f"Base topic: \"{base_topic}\"\n"
                f"Niche: {account['niche']}\n"
                f"Write an Instagram caption (max 150 chars) adapted for this niche. "
                f"Add 3-5 relevant hashtags. Be authentic to the niche voice.",
                max_tokens=100,
            )
            print(f"    Caption: \"{caption[:80]}...\"")
        except Exception as e:
            print(f"    ✗ Caption generation failed: {e}")
            results.append({"account": account["name"], "success": False, "error": str(e)})
            continue

        try:
            success = post_to_account(account, caption, image_url)
            results.append({"account": account["name"], "success": success})
        except Exception as e:
            print(f"    ✗ Post failed: {e}")
            results.append({"account": account["name"], "success": False, "error": str(e)})

        if i < len(ACCOUNTS) - 1:
            print(f"    Waiting 5s before next account...")
            time.sleep(5)

    print("\n[Cross-Poster] Summary:")
    for r in results:
        status = "✓" if r.get("success") else "✗"
        print(f"  {status} @{r['account']}")

    success_count = sum(1 for r in results if r.get("success"))
    print(f"\n  Posted to {success_count}/{len(ACCOUNTS)} accounts.")


if __name__ == "__main__":
    main()
