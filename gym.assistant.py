import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="FitZone Gym Assistant",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    /* Main gradient background */
    .main {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        padding: 20px;
    }
    
    /* Title styling */
    h1 {
        color: white !important;
        text-align: center;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        font-size: 3rem !important;
        margin-bottom: 10px;
    }
    
    h3 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: rgba(255,255,255,0.95) !important;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Input box styling */
    .stChatInputContainer {
        border-top: 2px solid rgba(255,255,255,0.3);
        padding-top: 20px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: rgba(255,255,255,0.1);
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(255,255,255,0.9);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Success/info messages */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 10px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: rgba(255,255,255,0.2);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header with emoji and tagline
st.title("💪 FitZone Gym & Fitness")
st.markdown("""
<div style='text-align: center; color: white; margin-bottom: 30px;'>
    <p style='font-size: 1.4rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
        🏋️ Your AI Fitness Assistant | Transform Your Body, Transform Your Life
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key input
    api_key = st.text_input(
        "Google API Key:",
        type="password",
        key="api_key_input",
        help="Enter your Google Gemini API key to start chatting"
    )
    
    # API Key validation
    if api_key:
        if api_key.startswith("AIza") and len(api_key) > 30:
            st.success("✅ API Key Activated!")
        else:
            st.warning("⚠️ Invalid API key format")
    else:
        st.info("👆 Enter API key to activate assistant")
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    
    quick_questions = [
        "What are membership prices?",
        "Show class schedule",
        "Tell me about personal training",
        "What are your hours?",
        "Do you have a pool?"
    ]
    
    for question in quick_questions:
        if st.button(question, use_container_width=True):
            st.session_state.quick_question = question
    
    st.markdown("---")
    
    # Gym Stats
    st.subheader("📊 Gym Info")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Members", "2,500+", "+120")
        st.metric("Classes/Week", "45", "+5")
    with col2:
        st.metric("Rating", "4.8⭐", "+0.2")
        st.metric("Trainers", "15", "Certified")
    
    st.markdown("---")
    
    # Contact Info
    st.subheader("📞 Contact")
    st.markdown("""
    **Phone:** (555) 456-7890
    
    **Email:** info@fitzonegym.com
    
    **Hours:**  
    Mon-Fri: 5 AM - 11 PM  
    Weekends: 7 AM - 9 PM
    
    **Location:**  
    456 Fitness Ave, Downtown
    """)

# Comprehensive gym information database
gym_info = """
FITZONE GYM & FITNESS CENTER - COMPLETE INFORMATION

=== BASIC INFORMATION ===
Name: FitZone Gym & Fitness Center
Location: 456 Fitness Avenue, Downtown
Phone: (555) 456-7890
Email: info@fitzonegym.com
Website: www.fitzonegym.com
Instagram: @fitzonegym
Facebook: FitZone Gym
Established: 2015
Total Members: 2,500+
Rating: 4.8/5 stars (1,200+ reviews)

=== HOURS OF OPERATION ===
Monday-Friday: 5:00 AM - 11:00 PM
Saturday-Sunday: 7:00 AM - 9:00 PM
Holidays: 8:00 AM - 6:00 PM
24/7 Access: Available for Premium members only
Front Desk: Open during all operating hours
Last check-in: 30 minutes before closing

=== MEMBERSHIP PLANS ===

1. BASIC MEMBERSHIP - $30/month
   - Access to all gym equipment
   - Locker room with showers
   - Free WiFi
   - No contract required
   - Cancel anytime
   - Peak hours restrictions apply (5-8 PM weekdays)

2. STANDARD MEMBERSHIP - $50/month
   - Everything in Basic PLUS:
   - Unlimited group fitness classes
   - Access during all hours (no restrictions)
   - 2 free guest passes per month
   - Towel service included
   - Discount on personal training (10% off)

3. PREMIUM MEMBERSHIP - $80/month
   - Everything in Standard PLUS:
   - 24/7 gym access (key card entry)
   - 4 free guest passes per month
   - Free parking (reserved spot)
   - Complimentary locker rental
   - 1 personal training session per month (FREE)
   - Priority class booking
   - Access to VIP lounge
   - Massage chair access
   - 20% discount on all services

4. COUPLES MEMBERSHIP - $120/month (2 people)
   - Standard membership benefits for 2 people
   - Save $20/month vs individual memberships
   - Shared guest passes (4 per month)

5. FAMILY PLAN - $150/month (up to 4 people)
   - Standard membership for entire family
   - Kids under 16 included free
   - Family locker available
   - Save $50/month vs individual memberships

6. STUDENT DISCOUNT - 20% OFF any plan
   - Valid student ID required
   - Must be enrolled full-time
   - Ages 16-24

7. SENIOR DISCOUNT (60+) - 25% OFF any plan
   - Valid ID required
   - Special senior fitness classes included

8. DAY PASS - $15/day
   - Full gym access for one day
   - All equipment included
   - Group classes included
   - Towel rental: +$3

=== FACILITIES & EQUIPMENT ===

CARDIO ZONE:
- 30 treadmills (with TV screens)
- 20 elliptical machines
- 15 stationary bikes
- 10 rowing machines
- 5 stair climbers
- Virtual cycling studio

STRENGTH TRAINING:
- Complete free weight section (5-100 lbs dumbbells)
- 20 cable machines
- 15 plate-loaded machines
- Smith machines (3)
- Power racks (4)
- Deadlift platforms (2)
- Leg press machines
- All major muscle group equipment

FUNCTIONAL TRAINING AREA:
- TRX suspension trainers
- Battle ropes
- Kettlebells (10-50 lbs)
- Medicine balls
- Plyometric boxes
- Agility ladder
- Slam balls
- Resistance bands

SPECIALIZED AREAS:
- Olympic lifting platform with bumper plates
- Boxing area (heavy bags, speed bags, boxing ring)
- Stretching area with mats
- Core training zone
- Mobility tools section

POOL & WATER FACILITIES:
- 25-meter heated lap pool (6 lanes)
- Hot tub/Jacuzzi (seats 8)
- Steam room
- Sauna (dry heat)
- Pool hours: 6 AM - 9 PM daily
- Lap swimming: Always available
- Water aerobics classes in pool

OTHER AMENITIES:
- Private shower stalls (individual, not communal)
- Lockers (free day-use, $10/month rental)
- Hair dryers
- Changing rooms
- Bathroom facilities
- Water fountains with bottle fillers
- Smoothie & juice bar
- Retail area (supplements, gear, apparel)
- Free parking lot (200 spaces)
- Bike racks
- WiFi throughout facility

=== GROUP FITNESS CLASSES ===

SCHEDULE (45 classes per week):

MONDAY:
- 6:00 AM - Sunrise Yoga (60 min)
- 7:00 AM - HIIT Bootcamp (45 min)
- 9:00 AM - Pilates (60 min)
- 12:00 PM - Lunchtime Express HIIT (30 min)
- 5:30 PM - Spin Class (45 min)
- 6:30 PM - Zumba (60 min)
- 7:30 PM - Strength & Conditioning (60 min)

TUESDAY:
- 6:00 AM - Morning Spin (45 min)
- 9:00 AM - Senior Fitness (45 min)
- 12:00 PM - Core Blast (30 min)
- 5:30 PM - CrossFit Style (60 min)
- 6:30 PM - Kickboxing (45 min)
- 7:30 PM - Yoga Flow (60 min)

WEDNESDAY:
- 6:00 AM - Sunrise Yoga (60 min)
- 7:00 AM - HIIT Bootcamp (45 min)
- 9:00 AM - Barre Fitness (60 min)
- 12:00 PM - Lunchtime Express HIIT (30 min)
- 5:30 PM - Spin Class (45 min)
- 6:30 PM - Body Pump (60 min)
- 7:30 PM - Stretching & Recovery (45 min)

THURSDAY:
- 6:00 AM - Morning Spin (45 min)
- 9:00 AM - Aqua Aerobics (45 min, in pool)
- 12:00 PM - Abs & Core (30 min)
- 5:30 PM - CrossFit Style (60 min)
- 6:30 PM - Zumba (60 min)
- 7:30 PM - Yoga Flow (60 min)

FRIDAY:
- 6:00 AM - HIIT Bootcamp (45 min)
- 9:00 AM - Pilates (60 min)
- 12:00 PM - Express Cardio (30 min)
- 5:30 PM - Friday Night Spin Party (45 min)
- 6:30 PM - Full Body Strength (60 min)

SATURDAY:
- 8:00 AM - Weekend Warrior HIIT (60 min)
- 9:00 AM - Yoga (75 min)
- 10:30 AM - Spin & Core Combo (60 min)
- 11:30 AM - Family Fitness Fun (45 min)
- 1:00 PM - Aqua Fit (45 min)

SUNDAY:
- 9:00 AM - Gentle Yoga (60 min)
- 10:00 AM - Stretch & Recover (45 min)
- 11:00 AM - Sunday Spin (45 min)
- 12:00 PM - HIIT Express (30 min)

CLASS DETAILS:
- Average class size: 15-20 people
- Maximum capacity: 25 per class
- Booking: Reserve spot up to 7 days in advance
- Cancellation: Free up to 2 hours before class
- Late cancellation: Counts as used class
- Drop-ins: Available if space permits
- All equipment provided
- Bring: Water bottle, towel, workout clothes

=== PERSONAL TRAINING ===

RATES:
- Single Session: $60 (60 minutes)
- 5-Session Package: $275 (save $25)
- 10-Session Package: $500 (save $100)
- 20-Session Package: $900 (save $300)
- Monthly Unlimited: $800/month (minimum 2x/week)

FIRST SESSION:
- Complimentary consultation (30 min) - FREE
- Fitness assessment included
- Goal setting session
- Custom workout plan created

WHAT'S INCLUDED:
- Personalized workout programs
- Nutrition guidance (basic)
- Progress tracking
- Form correction
- Motivation & accountability
- Exercise variations for injuries
- Flexible scheduling

TRAINER SPECIALIZATIONS:
- Weight loss programs
- Muscle building & bodybuilding
- Sports performance training
- Senior fitness
- Post-injury rehabilitation
- Prenatal/postnatal fitness
- Functional fitness
- Marathon/endurance training
- Powerlifting coaching
- Olympic lifting

NUMBER OF TRAINERS: 15 certified trainers
All trainers are:
- Nationally certified (ACE, NASM, or ISSA)
- CPR/First Aid certified
- Background checked
- Experienced (minimum 2 years)

SMALL GROUP TRAINING:
- 2-4 people: $40/person per session
- Must book together
- Great for friends/couples
- Semi-private attention

=== BOOKING & POLICIES ===

HOW TO JOIN:
1. Visit gym for tour (walk-ins welcome!)
2. Choose membership plan
3. Fill out membership agreement
4. Provide valid ID and payment info
5. Get member key card
6. Orientation tour included (15 min)

PAYMENT OPTIONS:
- Credit/debit card (Visa, Mastercard, Amex, Discover)
- ACH bank transfer
- Cash (in-person only)
- Monthly auto-pay (required for memberships)
- Annual payment option (save 2 months)

JOINING FEES:
- Enrollment fee: $50 (one-time)
- WAIVED this month! (Limited time promotion)
- No long-term contracts
- Cancel anytime with 30-day notice

CANCELLATION POLICY:
- 30-day written notice required
- No cancellation fees
- Pro-rated refunds not available
- Freeze membership: $10/month (max 3 months)
- Medical freeze: Free with doctor's note

GUEST POLICY:
- Guests must be 16+ years old
- Valid ID required
- Guest pass needed (from member)
- Waiver must be signed
- Guest fee: $10 (or free with guest passes)

AGE REQUIREMENTS:
- Minimum age: 16 years old
- Ages 16-17: Parent/guardian signature required
- Youth programs: Ages 12-15 (supervised classes only)
- Senior programs: 60+ years

DRESS CODE:
- Athletic shoes required (closed-toe)
- Workout appropriate clothing
- Shirt must be worn at all times
- No jeans or street clothes
- Towel recommended

GYM ETIQUETTE:
- Wipe down equipment after use
- Re-rack weights after use
- Respect 30-min cardio limit during peak hours
- No dropping weights (except designated areas)
- Keep noise levels reasonable
- Cell phone calls in lobby only

=== SPECIAL PROGRAMS & SERVICES ===

NUTRITION SERVICES:
- Nutritionist consultations: $75/session
- Meal planning service: $150/month
- Body composition analysis: $30
- Metabolic testing: $100

MASSAGE THERAPY:
- 30-minute session: $50
- 60-minute session: $90
- 90-minute session: $130
- Sports massage specialist available

CHILDCARE:
- Available during peak hours (8 AM - 12 PM, 5 PM - 8 PM)
- Ages: 6 months - 12 years
- Cost: $5/hour per child
- Max 2 hours per visit
- Reservation recommended

SPECIAL EVENTS:
- Monthly fitness challenges
- Quarterly transformation contests ($1,000 prize)
- Member appreciation events
- Bring-a-friend week (1x per quarter)
- Holiday boot camps
- Charity fitness events

CORPORATE MEMBERSHIPS:
- Available for companies (10+ employees)
- 15% discount per membership
- Flexible billing options
- Wellness program support
- On-site demonstrations available

=== PROMOTIONS & SPECIALS ===

CURRENT OFFERS:
- NO ENROLLMENT FEE (limited time!)
- First month: 50% OFF (new members only)
- Refer a friend: Get 1 month free (both of you!)
- Birthday month: 25% off any service
- Military/First Responders: 15% off (with ID)
- Teacher discount: 10% off (with ID)

LOYALTY REWARDS:
- 1 year membership: Free personal training session
- 2 year membership: 1 month free
- 3+ years: VIP status (extra perks!)

=== COVID-19 & SAFETY ===

SAFETY MEASURES:
- Enhanced cleaning protocols (hourly)
- Hand sanitizer stations throughout
- Air filtration system (HEPA filters)
- Social distancing markers (when needed)
- Masks optional (member choice)
- Contactless check-in available
- Equipment spacing maintained

=== FAQS ===

Q: Do you have showers?
A: Yes! Individual private shower stalls in both locker rooms.

Q: Can I cancel anytime?
A: Yes, with 30-day written notice. No penalties.

Q: Do you have childcare?
A: Yes, during peak hours for $5/hour per child.

Q: Is parking free?
A: Yes, 200-space free parking lot.

Q: What if I'm a beginner?
A: Perfect! We offer beginner classes and free orientation.

Q: Can I freeze my membership?
A: Yes, $10/month fee, max 3 months. Medical freezes are free.

Q: Do you have personal trainers?
A: Yes, 15 certified trainers available. First consultation is FREE.

Q: Is there a pool?
A: Yes! 25-meter heated lap pool plus hot tub, sauna, and steam room.

Q: What equipment do you have?
A: Full cardio section, free weights, machines, functional training, Olympic lifting platform, boxing area, and more!

Q: How do I book classes?
A: Through our app, website, or at front desk. Book up to 7 days ahead.

=== TESTIMONIALS ===

"Best gym I've ever joined! Equipment is always clean, staff is super friendly." - Sarah M. ⭐⭐⭐⭐⭐

"Lost 30 pounds with the help of my trainer. Life-changing!" - Mike D. ⭐⭐⭐⭐⭐

"Love the group classes! The instructors are motivating and fun." - Jessica L. ⭐⭐⭐⭐⭐

"Great value for the price. Way better than those big chain gyms." - Tom R. ⭐⭐⭐⭐⭐

=== CONTACT & VISIT ===

PHONE: (555) 456-7890
Available: 5 AM - 11 PM daily
Quick questions: Text or call

EMAIL: info@fitzonegym.com
Response time: Within 24 hours
For: General inquiries, memberships, bookings

SOCIAL MEDIA:
Instagram: @fitzonegym (daily workout tips!)
Facebook: FitZone Gym (events & news)
YouTube: FitZone Fitness (workout videos)

ADDRESS:
456 Fitness Avenue
Downtown
(Next to Whole Foods, across from Central Park)

FREE GYM TOUR:
- Walk-ins welcome anytime during business hours
- Guided tour: 15-20 minutes
- Try a class for free
- No pressure, no obligation
- Meet our trainers
- See all facilities

VIRTUAL TOUR:
- Available on website: www.fitzonegym.com/tour
- 360-degree facility view
- Equipment showcase video

HOW TO GET STARTED:
1. Visit for a free tour (no appointment needed!)
2. Choose your membership plan
3. Sign up (takes 10 minutes)
4. Get your access card
5. Start your fitness journey TODAY!

We're excited to help you reach your fitness goals! 💪
"""

def ask_fitness_assistant(question, api_key):
    """AI Fitness Assistant powered by Gemini"""
    
    if not api_key or len(api_key) < 30:
        return "❌ Please enter a valid Google API key in the sidebar to start chatting with your fitness assistant!"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    full_prompt = f"""You are Max, an enthusiastic and knowledgeable fitness assistant at FitZone Gym & Fitness Center.

Your personality:
- Energetic, positive, and motivating
- Expert on fitness, memberships, and gym facilities
- Helpful and encouraging
- Use fitness emojis occasionally (💪🏋️🔥)
- Make people excited about their fitness journey
- Professional but friendly

Answer customer questions using ONLY the information provided below. If someone asks something you don't know, be honest and suggest they call the gym or visit in person.

COMPLETE GYM INFORMATION:
{gym_info}

CUSTOMER QUESTION: {question}

YOUR RESPONSE (be energetic, helpful, and motivating):"""
    
    payload = {
        "contents": [{
            "parts": [{
                "text": full_prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 700
        }
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
        if response.status_code != 200:
            error_msg = f"❌ API Error {response.status_code}"
            try:
                error_detail = response.json()
                if 'error' in error_detail:
                    error_msg += f": {error_detail['error'].get('message', 'Unknown error')}"
            except:
                pass
            return f"{error_msg}\n\nPlease check your API key and try again!"
        
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                parts = candidate['content']['parts']
                if len(parts) > 0 and 'text' in parts[0]:
                    return parts[0]['text']
        
        return "Sorry, I couldn't generate a response. Please try asking your question differently! 💪"
        
    except requests.exceptions.Timeout:
        return "⏰ Request timed out. Please try again!"
    except requests.exceptions.ConnectionError:
        return "❌ Connection error. Please check your internet connection and try again."
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# Main chat interface
if api_key and len(api_key) > 30:
    
    # Initialize chat
    if 'gym_messages' not in st.session_state:
        st.session_state.gym_messages = []
        
        # Welcome message
        welcome = """Hey there! 👋 I'm Max, your personal fitness assistant at FitZone Gym!

Welcome to your fitness journey! 🏋️💪

I'm here to help you with:
✅ Membership plans and pricing
✅ Class schedules and bookings
✅ Personal training information
✅ Gym facilities and equipment
✅ Special offers and promotions
✅ Any questions about getting started!

Whether you're a complete beginner or a seasoned athlete, we've got everything you need to reach your fitness goals!

What would you like to know? 🔥"""
        
        st.session_state.gym_messages.append({
            "role": "assistant",
            "content": welcome
        })
    
    # Handle quick questions from sidebar
    if 'quick_question' in st.session_state:
        question = st.session_state.quick_question
        st.session_state.gym_messages.append({"role": "user", "content": question})
        
        with st.spinner("💪 Getting that info for you..."):
            answer = ask_fitness_assistant(question, api_key)
            st.session_state.gym_messages.append({"role": "assistant", "content": answer})
        
        del st.session_state.quick_question
        st.rerun()
    
    # Display chat history
    for message in st.session_state.gym_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about FitZone Gym! 💪"):
        
        # Add user message
        st.session_state.gym_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("💪 Getting you the info..."):
                answer = ask_fitness_assistant(prompt, api_key)
                st.write(answer)
                st.session_state.gym_messages.append({"role": "assistant", "content": answer})

else:
    # No API key - show instructions
    st.info("👈 Please enter your Google API key in the sidebar to chat with Max, your fitness assistant!")
    
    with st.expander("📖 How to Get Started", expanded=True):
        st.markdown("""
        ### Quick Setup Guide:
        
        1. **Get your FREE Google API key:**
           - Visit: https://aistudio.google.com/app/apikey
           - Click "Create API key"
           - Copy the key (starts with "AIza...")
        
        2. **Paste it in the sidebar** (on the left ←)
        
        3. **Start asking questions!**
        
        ### 💬 Popular Questions to Try:
        - "What are your membership prices?"
        - "Do you have group fitness classes?"
        - "Tell me about personal training"
        - "What time do you open?"
        - "Do you have a pool and sauna?"
        - "Can I get a student discount?"
        - "What equipment do you have?"
        - "How do I cancel my membership?"
        """)
    
    # Feature highlights
    st.markdown("---")
    st.markdown("### 🌟 Why Choose FitZone?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **💰 Great Value**
        - From $30/month
        - No contracts
        - Student discounts
        - Free trial available
        """)
    
    with col2:
        st.markdown("""
        **🏋️ Top Facilities**
        - Modern equipment
        - 25m heated pool
        - Sauna & steam room
        - Boxing area
        """)
    
    with col3:
        st.markdown("""
        **🎯 Expert Support**
        - 15 certified trainers
        - 45 classes/week
        - Nutrition guidance
        - Free consultation
        """)
    
    # Special offers
    st.markdown("---")
    st.markdown("""
    <div style='background: rgba(255,255,255,0.9); padding: 30px; border-radius: 15px; text-align: center;'>
        <h2 style='color: #FF6B6B; margin-bottom: 15px;'>🎉 LIMITED TIME OFFER!</h2>
        <p style='font-size: 1.2rem; color: #333; margin-bottom: 10px;'><strong>50% OFF First Month</strong></p>
        <p style='font-size: 1.1rem; color: #666;'>+ NO Enrollment Fee + Free Personal Training Session</p>
        <p style='color: #999; margin-top: 15px;'>New members only • Expires end of month</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: white; padding: 20px;'>
    <h3 style='color: white; margin-bottom: 15px;'>💪 FitZone Gym & Fitness Center</h3>
    <p style='font-size: 1.1rem; margin: 5px 0;'>📍 456 Fitness Avenue, Downtown</p>
    <p style='font-size: 1.1rem; margin: 5px 0;'>📞 (555) 456-7890</p>
    <p style='font-size: 1.1rem; margin: 5px 0;'>✉️ info@fitzonegym.com</p>
    <p style='font-size: 1.1rem; margin: 15px 0;'>
        <strong>Hours:</strong> Mon-Fri 5AM-11PM | Weekends 7AM-9PM
    </p>
    <p style='font-size: 0.9rem; opacity: 0.8; margin-top: 25px;'>
        🤖 Powered by AI • Your Personal Fitness Assistant 24/7
    </p>
</div>
""", unsafe_allow_html=True)