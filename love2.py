import streamlit as st
import time
from PIL import Image
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="💖 For My Favorite Person", 
    page_icon="💝", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- INITIALIZE STATE VARIABLES ---
if "phase" not in st.session_state:
    st.session_state.phase = -1  # Phase -1: "I Love You" gate
if "selected_birthday" not in st.session_state:
    st.session_state.selected_birthday = ""

GRID_SIZE = 3  

def generate_jumbled_board():
    board = list(range(9))
    blank_idx = 8
    for _ in range(40):
        row, col = blank_idx // GRID_SIZE, blank_idx % GRID_SIZE
        valid_moves = []
        if row > 0: valid_moves.append(blank_idx - 3)
        if row < 2: valid_moves.append(blank_idx + 3)
        if col > 0: valid_moves.append(blank_idx - 1)
        if col < 2: valid_moves.append(blank_idx + 1)
        move = random.choice(valid_moves)
        board[blank_idx], board[move] = board[move], board[blank_idx]
        blank_idx = move
    if board == list(range(9)):
        return generate_jumbled_board()
    return board

if "puzzle_board" not in st.session_state:
    st.session_state.puzzle_board = generate_jumbled_board()

if "moves_left" not in st.session_state:
    st.session_state.moves_left = 25
if "puzzle_solved" not in st.session_state:
    st.session_state.puzzle_solved = False

def get_puzzle_pieces():
    try:
        img = Image.open("puzzle_picture.jpg").convert("RGB")
    except:
        # Soft-pink fallback image if picture is missing
        img = Image.new("RGB", (450, 450), color="#ffb6c1")
    img = img.resize((450, 450))
    w, h = img.size
    piece_w, piece_h = w // GRID_SIZE, h // GRID_SIZE
    pieces = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            box = (j * piece_w, i * piece_h, (j + 1) * piece_w, (i + 1) * piece_h)
            pieces.append(img.crop(box))
    blank = Image.new("RGB", (piece_w, piece_h), color="#4A1525")
    pieces[-1] = blank
    return pieces

# --- DYNAMIC THEMING & STYLES ---
background_themes = {
    -1: "linear-gradient(135deg, #1f0010 0%, #4a0e2e 50%, #1f0010 100%)", 
    0:  "linear-gradient(135deg, #2b081a 0%, #5e1338 50%, #2b081a 100%)", 
    1:  "linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fe9a8b 100%)", 
    2:  "linear-gradient(135deg, #580c25 0%, #9e2a4b 50%, #580c25 100%)", 
    3:  "linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%)", 
}

current_bg = background_themes.get(st.session_state.phase, "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)")

# Base Global Stylesheet Injection
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@300;400;600&display=swap');

    /* Global App Background */
    .stApp {{
        background: {current_bg} !important;
        color: #FFFFFF;
        font-family: 'Poppins', sans-serif;
        transition: background 1.5s ease-in-out;
    }}

    /* Hide Streamlit Header & Footer for Clean View */
    header, footer {{ visibility: hidden; }}

    /* Romantic Glassmorphic Card */
    .romantic-card {{
        background: rgba(255, 255, 255, 0.12);
        padding: 35px 25px;
        border-radius: 28px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25), 0 0 15px rgba(255, 182, 193, 0.2);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        margin-bottom: 25px;
        text-align: center;
        animation: fadeIn 1s ease-in-out;
    }}

    .glowing-title {{
        color: #ffffff !important;
        font-family: 'Great Vibes', cursive !important;
        font-size: 3.5rem !important;
        font-weight: 400 !important;
        text-shadow: 0 0 20px rgba(255, 105, 180, 0.8), 0 0 10px rgba(255, 255, 255, 0.8);
        margin-bottom: 10px;
    }}

    .love-text {{
        font-size: 1.15rem;
        color: #fce4ec;
        font-style: italic;
        font-weight: 300;
        line-height: 1.6;
    }}

    /* --- INPUT FIELDS TYPING COLOR FIX (BLACK TEXT) --- */
    div[data-baseweb="input"] > div {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 18px !important;
        border: 2px solid rgba(255, 255, 255, 0.8) !important;
    }}

    input {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 600 !important;
        text-align: center !important;
    }}

    input::placeholder {{
        color: #666666 !important;
        -webkit-text-fill-color: #666666 !important;
        font-weight: 400 !important;
    }}

    /* Animated Romantic Buttons */
    div.stButton > button {{
        background: linear-gradient(45deg, #ff416c, #ff4b2b) !important;
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 30px !important;
        box-shadow: 0 4px 25px rgba(255, 65, 108, 0.5) !important;
        transition: all 0.3s ease-in-out !important;
        width: 100%;
    }}

    div.stButton > button:hover {{
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 8px 30px rgba(255, 65, 108, 0.8) !important;
    }}

    /* Subtle Keyframe Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# PHASE -1: INTRODUCTORY "I LOVE YOU" REVEAL GATE
# ---------------------------------------------------------
if st.session_state.phase == -1:
    st.markdown(
        """
        <style>
        .welcome-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 50vh;
            text-align: center;
        }
        .subtitle-text {
            font-size: 1.2rem;
            color: #ff85a2;
            letter-spacing: 3px;
            margin-bottom: 25px;
            text-shadow: 0 0 10px rgba(255, 133, 162, 0.5);
            text-transform: uppercase;
        }
        .glowing-heart-btn button {
            background: transparent !important;
            color: #ff416c !important;
            border: 2px solid #ff416c !important;
            font-family: 'Great Vibes', cursive !important;
            font-size: 3rem !important;
            padding: 15px 45px !important;
            border-radius: 50px !important;
            box-shadow: 0 0 25px rgba(255, 65, 108, 0.4), inset 0 0 15px rgba(255, 65, 108, 0.2) !important;
            text-shadow: 0 0 12px rgba(255, 65, 108, 0.6) !important;
            cursor: pointer;
            transition: all 0.5s ease-in-out !important;
        }
        .glowing-heart-btn button:hover {
            color: white !important;
            background: linear-gradient(45deg, #ff416c, #ff4b2b) !important;
            box-shadow: 0 0 50px rgba(255, 65, 108, 0.9) !important;
            transform: scale(1.08) !important;
        }
        </style>
        <div class="welcome-container">
            <p class="subtitle-text">✨ A Private Sanctuary For My Favorite Person ✨</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown('<div class="glowing-heart-btn" style="text-align: center;">', unsafe_allow_html=True)
        if st.button("I Love You 💖", key="intro_love_btn"):
            st.session_state.phase = 0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# PHASE 0: THE CREATIVE LOGIN GATEWAY (FIXED CREDENTIALS)
# ---------------------------------------------------------
elif st.session_state.phase == 0:
    st.markdown("<p style='font-size: 3.5rem; text-align: center;'>🌹 🔒 🌹</p>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="romantic-card">
            <h1 class="glowing-title">Vault Door Locked</h1>
            <p class="love-text">My heart accepted your answer... Now, provide the secret keys to enter our vault. ✨</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    input_username = st.text_input("Username Key:", value="", placeholder="Who are you to me?")
    input_password = st.text_input("Password Code:", value="", type="password", placeholder="Enter the special dates...")
    
    if st.button("Access Heart Core 🔑"):
        # Normalizes spaces and lowers case so typing errors/extra spaces don't fail
        clean_user = input_username.strip().lower()
        clean_pass = input_password.strip().lower()
        
        if clean_user in ["hb prince", "hb prine"] and clean_pass == "27 and 28 april":
            st.success("🎉 Access Granted! Unlocking your adventure...")
            time.sleep(1.2)
            st.session_state.phase = 1
            st.rerun()
        else:
            st.error("❌ The vault stays shut. Incorrect Credentials!")


# ---------------------------------------------------------
# PHASE 1: THE NICKNAME (Soft Pink Canvas Theme)
# ---------------------------------------------------------
elif st.session_state.phase == 1:
    st.markdown("<p style='font-size: 3.5rem; text-align: center;'>🧸 ✨ 💫</p>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="romantic-card">
            <h1 class="glowing-title">Identity Verification</h1>
            <p class="love-text">Before you step further into my heart, prove your sweet identity. What do I call you? 🥰</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    nickname = st.text_input("Enter your secret sweet nickname:", value="").strip().lower()
    
    if st.button("Submit Answer 💘"):
        if nickname in ["chandalnee", "jan"]:
            st.markdown("<h3 style='color: #ffffff; text-align:center;'>✨ Identity Authenticated! Phase 2 unlocked.</h3>", unsafe_allow_html=True)
            time.sleep(1.2)
            st.session_state.phase = 2
            st.rerun()
        else:
            st.error("❌ Access Denied! That sweet soul isn't you.")


# ---------------------------------------------------------
# PHASE 2: SLIDING PUZZLE (Crimson Passion Theme)
# ---------------------------------------------------------
elif st.session_state.phase == 2:
    st.markdown("<p style='font-size: 3.5rem; text-align: center;'>🧩 ❤️ 🔥</p>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="romantic-card">
            <h1 class="glowing-title">Assemble My Feelings</h1>
            <p class="love-text">The pieces are scrambled! Slide them into position to reveal our memory. 🔗</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    if st.session_state.puzzle_board == [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        st.session_state.puzzle_solved = True

    if st.session_state.moves_left <= 0 and not st.session_state.puzzle_solved:
        st.error("❌ Out of moves! Let's reshuffle the layout.")
        if st.button("Reshuffle Puzzle 🔄"):
            st.session_state.puzzle_board = generate_jumbled_board()
            st.session_state.moves_left = 30
            st.session_state.puzzle_solved = False
            st.rerun()
            
    else:
        col_stat1, col_stat2 = st.columns(2)
        col_stat1.metric("🎯 Moves Remaining", st.session_state.moves_left)
        col_stat2.metric("🏆 Puzzle Status", "SOLVED! ✨" if st.session_state.puzzle_solved else "Scrambled 🔥")
        
        images = get_puzzle_pieces()
        board = st.session_state.puzzle_board
        blank_idx = board.index(8)
        
        st.write("---")
        for row in range(GRID_SIZE):
            cols = st.columns(GRID_SIZE)
            for col in range(GRID_SIZE):
                linear_idx = row * GRID_SIZE + col
                piece_id = board[linear_idx]
                cols[col].image(images[piece_id], use_container_width=True)
                
                is_neighbor = False
                br, bc = blank_idx // GRID_SIZE, blank_idx % GRID_SIZE
                pr, pc = linear_idx // GRID_SIZE, linear_idx % GRID_SIZE
                if abs(br - pr) + abs(bc - pc) == 1:
                    is_neighbor = True
                
                if not st.session_state.puzzle_solved:
                    if cols[col].button("Slide", key=f"btn_{linear_idx}", disabled=not is_neighbor):
                        st.session_state.puzzle_board[blank_idx], st.session_state.puzzle_board[linear_idx] = \
                            st.session_state.puzzle_board[linear_idx], st.session_state.puzzle_board[blank_idx]
                        st.session_state.moves_left -= 1
                        st.rerun()

        st.write("---")
        puzzle_answer = st.text_input("Riddle: What goes up but never comes down?").strip().lower()
        
        if st.button("Verify & Proceed 🔓"):
            if not st.session_state.puzzle_solved:
                st.error("❌ The picture is still scrambled! Arrange the pieces first.")
            elif "age" not in puzzle_answer:
                st.error("❌ Picture looks amazing, but the riddle answer is incorrect!")
            else:
                st.markdown("<h3 style='color: #ffffff; text-align:center;'>🧩 Brilliant! Onward to the birthday step...</h3>", unsafe_allow_html=True)
                time.sleep(1.5)
                st.session_state.phase = 3
                st.rerun()


# ---------------------------------------------------------
# PHASE 3: BIRTHDATE VERIFICATION (Magical Twilight Theme)
# ---------------------------------------------------------
elif st.session_state.phase == 3:
    st.markdown("<p style='font-size: 3.5rem; text-align: center;'>🎂 🔮 ⭐</p>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="romantic-card">
            <h1 class="glowing-title">The Secret Timeline</h1>
            <p class="love-text">Enter the special date to complete validation procedures. 🎁</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    picture_puzzle_answer = st.text_input("Enter your magic birthdate (DD-MM-YYYY):").strip()
    
    if st.button("Unlock Treasure Vault 🔑"):
        if picture_puzzle_answer in ["31-10-2005", "27-11-2001"]:
            st.session_state.selected_birthday = picture_puzzle_answer
            st.balloons()
            st.toast("🎉 SURPRISE!!! YOU DID IT, MY LOVE!!! 🎉", icon="💝")
            time.sleep(1.5)
            st.session_state.phase = 4
            st.rerun()
        else:
            st.error("❌ Wrong target date context. Try again!")


# ---------------------------------------------------------
# PHASE 4: HACKER SEQUENCE (Pitch Black Terminal Theme)
# ---------------------------------------------------------
elif st.session_state.phase == 4:
    st.markdown(
        """
        <style>
        .stApp, html, body, [data-testid="stAppViewContainer"] { 
            background-color: #050002 !important; 
            background-image: none !important; 
            color: #ff0055 !important; 
        }
        h1, p, span, label { 
            color: #ff0055 !important; 
            font-family: 'Courier New', monospace !important; 
            text-shadow: 0 0 8px rgba(255, 0, 85, 0.6) !important; 
        }
        .romantic-card { 
            background: transparent !important; 
            border: 1px solid #ff0055 !important; 
            box-shadow: 0 0 15px rgba(255, 0, 85, 0.4) !important; 
        }
        div.stSpinner > div {
            border-top-color: #ff0055 !important;
        }

        /* Hacker phase terminal text style override */
        div[data-baseweb="input"] > div {
            background-color: #110005 !important;
            border: 1px solid #ff0055 !important;
        }
        input {
            color: #ff0055 !important;
            -webkit-text-fill-color: #ff0055 !important;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    st.title("⚠️ WARNING: SYSTEM OVERLOADED BY LOVE ⚠️")
    
    status_text = st.empty()
    status_text.write("👾 Overriding security protocols... Stealing your heart...")
    
    try:
        st.image("hacker.jpg", width=400)
    except:
        st.warning("[Hacker Image Missing - Place 'hacker.jpg' in your folder]")
    
    time.sleep(2.0) 
    status_text.write("👾 Downloading private_feelings.exe... Complete!")
    time.sleep(1.5)
    
    with st.spinner("⏳ Compiling a lifetime of smiles, warm hugs, and eternal memories... Please wait..."):
        time.sleep(3.0)
        
    st.session_state.phase = 5
    st.rerun()


# ---------------------------------------------------------
# PHASE 5: THE FINAL CELEBRATION REWARD
# ---------------------------------------------------------
elif st.session_state.phase == 5:
    st.balloons()
    st.markdown(
        """
        <div class="romantic-card" style="background: rgba(255, 255, 255, 0.85); border: 2px solid #ff416c;">
            <h1 class="glowing-title" style="color: #ff416c !important; text-shadow: none !important;">❤️ Access Fully Granted ❤️</h1>
            <p style="font-size: 1.3rem; font-weight: 600; color: #4A1525; margin-top: 10px;">
                Happy Birthday to the one who makes my universe skip a beat! You are my absolute finest blessing. 💖
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Secret Love Note Collapsible Section
    with st.expander("💌 Tap here to open a secret love note for you..."):
        st.write("""
        *My Dearest,*
        
        Every single day with you feels like a gift. Thank you for filling my world with your light, 
        your smile, and your sweetness. No matter where we go or what we do, you will always be my 
        favorite adventure. 
        
        *Forever & Always yours.* 🥰
        """)

    st.write("---")

    if st.session_state.selected_birthday == "31-10-2005":
        try:
            st.video("video_1.mp4")
            st.caption("✨ You Gorgeous Surprise! ✨")
        except:
            st.error("🚨 Place your 'video_1.mp4' file in the app folder to watch it here!")
    elif st.session_state.selected_birthday == "27-11-2001":
        try:
            st.video("video_2.mp4")
            st.caption("🌟 Your Magical Love Prize! 🌟")
        except:
            st.error("🚨 Place your 'video_2.mp4' file in the app folder to watch it here!")
        
    st.write("")
    if st.button("Relive The Love Again 🔄"):
        st.session_state.phase = -1  
        st.session_state.selected_birthday = ""
        st.session_state.puzzle_board = generate_jumbled_board()
        st.session_state.moves_left = 25
        st.session_state.puzzle_solved = False
        st.rerun()