"""
Run from GitHub Actions to create a cloud-IP instagrapi session.
If Instagram sends a STEP_NAME (Bloks) challenge:
  1. Open Instagram app on phone for this account
  2. Approve the 'New login from unknown device' notification
  3. Re-run this workflow (login.yml) manually
"""
import os, sys, json, time
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired, ChallengeUnknownStep
from pathlib import Path

username = os.environ["IG_USERNAME"]
password = os.environ["IG_PASSWORD"]

print(f"Logging in as {username}...")
cl = Client()
cl.delay_range = [2, 4]

MAX_RETRIES = 2
for attempt in range(1, MAX_RETRIES + 1):
    try:
        cl.login(username, password)
        print(f"Login OK  user_id={cl.user_id}")
        break
    except ChallengeUnknownStep as e:
        print(f"\n[!] Instagram sent a Bloks/App challenge (attempt {attempt}/{MAX_RETRIES}).")
        print("[!] ACTION REQUIRED:")
        print("[!]   1. Open Instagram app on your phone")
        print(f"[!]   2. Log in as @{username}")
        print("[!]   3. You should see: 'Suspicious login attempt from a new device'")
        print("[!]   4. Tap 'This was me' / 'Approve'")
        print("[!]   5. Re-run the Login & Save Session workflow on GitHub Actions")
        sys.exit(3)  # Exit code 3 = needs manual approval
    except ChallengeRequired as e:
        print(f"[!] Challenge required (type: {type(e).__name__}) — attempt {attempt}")
        if attempt < MAX_RETRIES:
            print("[!] Waiting 20s before retry...")
            time.sleep(20)
        else:
            print("[!] All retries failed. Check phone/email for verification code.")
            sys.exit(3)
    except Exception as e:
        print(f"[!] Login error: {e}")
        sys.exit(1)

settings = cl.get_settings()
data = {"_instagrapi": settings, "user_id": str(cl.user_id)}
Path("ig_settings.json").write_text(json.dumps(data, indent=2))
print("ig_settings.json saved")
