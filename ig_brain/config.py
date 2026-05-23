"""
Central config for thegurukul.online Instagram Brain
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env", override=True)

# Account
ACCOUNT_USERNAME = "thegurukul.online"
ACCOUNT_USER_ID  = 67178598327
ACCOUNT_NICHE    = "Online education, ancient Indian wisdom, modern learning, gurukul philosophy, personal growth and skill-building"

# Posting schedule (24h IST hours to post)
POSTING_HOURS    = [9, 13, 18, 21]
POSTS_PER_DAY    = 2

# Comment reply settings
REPLY_CHECK_INTERVAL = 300
REPLY_SLEEP_MIN      = 5
REPLY_SLEEP_MAX      = 15

# Evolution
EVOLUTION_AFTER_POSTS = 5

# Paths
BASE_DIR      = Path(__file__).parent.parent
MEMORY_FILE   = BASE_DIR / "brain_memory.json"
POSTED_FILE   = BASE_DIR / "posted_content.json"
REPLIED_FILE  = BASE_DIR / "replied_comments.json"
IMAGES_DIR    = BASE_DIR / "generated_images"
IMAGES_DIR.mkdir(exist_ok=True)

# API Keys
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GROQ_KEY      = os.environ.get("GROQ_API_KEY", "")

# Content pillars
CONTENT_PILLARS = [
    "Ancient Gurukul wisdom applied to modern education",
    "Study techniques and learning psychology backed by science",
    "Indian knowledge systems — Vedas, Upanishads, Arthashastra",
    "Success habits and discipline inspired by ancient masters",
    "Online courses and skill-building for today's generation",
    "Motivation and mindset for students and learners",
    "Mythology lessons that teach life skills",
    "Technology and AI tools for better learning",
    "Career guidance and purpose-finding for youth",
    "Spiritual intelligence and emotional resilience for students",
]

HASHTAG_POOLS = {
    "education":    ["#education", "#learning", "#onlineeducation", "#studygram", "#studentlife", "#knowledgeispower", "#gurukul", "#studymotivation"],
    "india":        ["#india", "#indianculture", "#ancientindia", "#vedic", "#hinduwisdom", "#bharath", "#sanskriti"],
    "motivation":   ["#motivation", "#inspiration", "#growthmindset", "#successmindset", "#disciplineiskey", "#selfimprovement", "#personaldevelopment"],
    "youth":        ["#youth", "#students", "#collegelife", "#skilldevelopment", "#careerguidance", "#youngminds"],
    "wisdom":       ["#wisdom", "#ancientwisdom", "#philosophy", "#lifelessons", "#mindfulness", "#spirituality"],
    "ai":           ["#AIlearning", "#edtech", "#futureoflearning", "#technology", "#artificialintelligence"],
    "general":      ["#reels", "#explore", "#viral", "#trending", "#instareels", "#instagram", "#content"],
}
