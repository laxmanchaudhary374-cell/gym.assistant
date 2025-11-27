import streamlit as st
import requests
import json
import os
import time
import hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Page config
st.set_page_config(page_title="FitZone Gym - Production", page_icon="💪", layout="centered")

# Initialize session state
if 'gym_messages' not in st.session_state:
    st.session_state.gym_messages = []
if 'response_cache' not in st.session_state:
    st.session_state.response_cache = {}
if 'request_count' not in st.session_state:
    st.session_state.request_count = 0
if 'rate_limit_reset' not in st.session_state:
    st.session_state.rate_limit_reset = datetime.now() + timedelta(minutes=1)

# Custom CSS (your existing styles)
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%); padding: 20px; }
    h1 { color: white !important; text-align: center; text-shadow: 3px 3px 6px rgba(0,0,0,0.3); }
</style>
""", unsafe_allow_html=True)

st.title("💪 FitZone Gym (Production)")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key handling
    if GOOGLE_API_KEY:
        st.success("✅ API Key Configured")
        api_key = GOOGLE_API_KEY
    else:
        api_key = st.text_input("API Key (Dev Mode):", type="password")
    
    st.markdown("---")
    
    # Admin Panel
    with st.expander("🔐 Admin"):
        admin_pass = st.text_input("Password:", type="password")
        if admin_pass == "admin123":
            st.success("Admin Access")
            st.metric("Total Messages", len(st.session_state.gym_messages))
            st.metric("Cached Responses", len(st.session_state.response_cache))
            st.metric("Requests This Minute", st.session_state.request_count)

# Your gym_info variable (keep existing)
gym_info = """[Your existing gym info here]"""

def check_rate_limit():
    """Rate limiting"""
    if datetime.now() > st.session_state.rate_limit_reset:
        st.session_state.request_count = 0
        st.session_state.rate_limit_reset = datetime.now() + timedelta(minutes=1)
    
    if st.session_state.request_count >= 10:
        time_left = (st.session_state.rate_limit_reset - datetime.now()).seconds
        return False, f"⏳ Rate limit! Wait {time_left}s"
    
    st.session_state.request_count += 1
    return True, None

def get_cache_key(question):
    """Generate cache key"""
    return hashlib.md5(question.lower().strip().encode()).hexdigest()

def ask_fitness_assistant(question, api_key):
    """Production-ready AI assistant"""
    
    # Check cache
    cache_key = get_cache_key(question)
    if cache_key in st.session_state.response_cache:
        logger.info("Cache hit")
        return st.session_state.response_cache[cache_key]
    
    logger.info(f"Processing question: {question[:50]}...")
    start_time = datetime.now()
    
    if not api_key or len(api_key) < 30:
        return "❌ Invalid API key"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    full_prompt = f"""You are Max, fitness assistant at FitZone.
    
{gym_info}

Question: {question}

Answer:"""
    
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"temperature": 0.8, "maxOutputTokens": 700}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        response_time = (datetime.now() - start_time).total_seconds()
        
        if response.status_code != 200:
            logger.error(f"API error: {response.status_code}")
            return f"❌ API Error {response.status_code}"
        
        result = response.json()
        answer = result['candidates'][0]['content']['parts'][0]['text']
        
        # Cache response
        st.session_state.response_cache[cache_key] = answer
        logger.info(f"Response time: {response_time:.2f}s")
        
        return answer
        
    except requests.exceptions.Timeout:
        logger.error("Request timeout")
        return "⏰ Request timed out"
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"❌ Error: {e}"

# Main chat
if api_key and len(api_key) > 30:
    
    # Initialize with welcome
    if not st.session_state.gym_messages:
        welcome = "Hey! 👋 I'm Max, your fitness assistant at FitZone! What can I help you with?"
        st.session_state.gym_messages.append({"role": "assistant", "content": welcome})
    
    # Display messages
    for msg in st.session_state.gym_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input with rate limiting
    if prompt := st.chat_input("Ask about FitZone! 💪"):
        
        # Rate limit check
        allowed, error_msg = check_rate_limit()
        if not allowed:
            st.error(error_msg)
        else:
            # Add user message
            st.session_state.gym_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            # Get response
            with st.chat_message("assistant"):
                with st.spinner("💪 Thinking..."):
                    answer = ask_fitness_assistant(prompt, api_key)
                    st.write(answer)
                    st.session_state.gym_messages.append({"role": "assistant", "content": answer})

else:
    st.info("👈 Configure API key to start!")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; color:white;'>💪 FitZone Gym | Production v1.0</p>", unsafe_allow_html=True)