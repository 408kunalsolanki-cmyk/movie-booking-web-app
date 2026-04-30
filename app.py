import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
import random
import string

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineBook – Movie Ticket Booking",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}
.stApp { background: #0a0a0f; }
.block-container { padding: 1.5rem 2rem; max-width: 1200px; }

/* ── Header ── */
.cinebook-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    background: linear-gradient(135deg, #0a0a0f 0%, #12121e 100%);
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 2rem;
}
.cinebook-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.8rem;
    letter-spacing: 4px;
    background: linear-gradient(90deg, #e63946, #f4a261, #e63946);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
}
@keyframes shimmer { to { background-position: 200% center; } }
.cinebook-tagline { color: #6b6b8a; font-size: 0.95rem; letter-spacing: 2px; text-transform: uppercase; }

/* ── Movie Cards ── */
.movie-card {
    background: linear-gradient(145deg, #12121e, #0f0f1a);
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 1.2rem;
    transition: all 0.3s ease;
    cursor: pointer;
    margin-bottom: 1rem;
}
.movie-card:hover { border-color: #e63946; transform: translateY(-4px); box-shadow: 0 12px 40px rgba(230,57,70,0.2); }
.movie-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; letter-spacing: 1px; color: #f0f0ff; margin: 0.4rem 0 0.2rem; }
.movie-meta { color: #6b6b8a; font-size: 0.82rem; margin-bottom: 0.5rem; }
.genre-badge {
    display: inline-block; background: rgba(230,57,70,0.15);
    color: #e63946; border: 1px solid rgba(230,57,70,0.3);
    border-radius: 20px; padding: 2px 10px; font-size: 0.75rem;
    margin-right: 4px; margin-top: 4px;
}
.rating-badge {
    display: inline-block; background: rgba(244,162,97,0.15);
    color: #f4a261; border: 1px solid rgba(244,162,97,0.3);
    border-radius: 20px; padding: 2px 10px; font-size: 0.75rem;
}

/* ── Section Headings ── */
.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem; letter-spacing: 2px;
    color: #f0f0ff; margin: 1.5rem 0 1rem;
    border-left: 4px solid #e63946; padding-left: 12px;
}

/* ── Seat Grid ── */
.seat-legend { display: flex; gap: 1.5rem; margin: 1rem 0; flex-wrap: wrap; }
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #9090b0; }
.legend-dot { width: 16px; height: 16px; border-radius: 4px; }

/* ── Booking Summary ── */
.summary-card {
    background: linear-gradient(145deg, #12121e, #0f0f1a);
    border: 1px solid #e63946;
    border-radius: 16px; padding: 1.5rem;
    margin-top: 1rem;
}
.summary-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #1e1e2e; }
.summary-label { color: #6b6b8a; font-size: 0.9rem; }
.summary-value { color: #f0f0ff; font-size: 0.9rem; font-weight: 500; }
.summary-total { font-size: 1.2rem !important; font-weight: 700 !important; color: #e63946 !important; }

/* ── Confirmation ── */
.ticket-card {
    background: linear-gradient(135deg, #12121e 0%, #1a1025 100%);
    border: 2px solid #e63946;
    border-radius: 20px; padding: 2rem;
    text-align: center; max-width: 480px; margin: 0 auto;
    box-shadow: 0 0 60px rgba(230,57,70,0.15);
}
.ticket-id { font-family: 'Bebas Neue', sans-serif; font-size: 2.5rem; color: #e63946; letter-spacing: 4px; }
.ticket-divider {
    border: none; border-top: 2px dashed #2a2a3e;
    margin: 1.2rem 0; position: relative;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #e63946, #c1121f) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important; letter-spacing: 1px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(230,57,70,0.4) !important; }

/* ── Inputs ── */
.stSelectbox > div > div, .stDateInput > div > div input, .stTextInput > div > div input,
.stNumberInput > div > div input {
    background: #12121e !important; color: #e8e8f0 !important;
    border: 1px solid #2a2a3e !important; border-radius: 8px !important;
}

/* ── Steps indicator ── */
.steps-bar { display: flex; gap: 0; margin-bottom: 2rem; }
.step { flex: 1; text-align: center; padding: 0.6rem; font-size: 0.82rem; font-weight: 500; color: #4a4a6a; border-bottom: 3px solid #1e1e2e; letter-spacing: 1px; }
.step.active { color: #e63946; border-bottom-color: #e63946; }
.step.done { color: #2a9d8f; border-bottom-color: #2a9d8f; }

/* ── Misc ── */
.info-pill {
    background: rgba(42,157,143,0.1); color: #2a9d8f;
    border: 1px solid rgba(42,157,143,0.3); border-radius: 8px;
    padding: 0.5rem 1rem; font-size: 0.9rem; margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
MOVIES = [
    {"id": 1, "title": "INTERSTELLAR REBORN", "genre": ["Sci-Fi", "Drama"], "duration": 169, "rating": "PG-13", "imdb": 8.7, "price": 250, "emoji": "🚀", "desc": "A crew of astronauts travels through a wormhole in search of a new home for humanity."},
    {"id": 2, "title": "SHADOW KINGDOM", "genre": ["Action", "Fantasy"], "duration": 142, "rating": "PG-13", "imdb": 8.1, "price": 220, "emoji": "⚔️", "desc": "An exiled prince returns to reclaim his throne from dark forces threatening the realm."},
    {"id": 3, "title": "THE LAST SIGNAL", "genre": ["Thriller", "Mystery"], "duration": 118, "rating": "R", "imdb": 7.9, "price": 200, "emoji": "📡", "desc": "A radio operator picks up a distress signal that leads to a terrifying conspiracy."},
    {"id": 4, "title": "NEON HEARTS", "genre": ["Romance", "Drama"], "duration": 105, "rating": "PG", "imdb": 7.5, "price": 180, "emoji": "💜", "desc": "Two strangers find love in a rain-soaked city of neon lights and broken dreams."},
    {"id": 5, "title": "APEX PREDATOR", "genre": ["Action", "Thriller"], "duration": 128, "rating": "R", "imdb": 7.8, "price": 210, "emoji": "🐆", "desc": "An elite soldier hunts the world's most dangerous criminal across three continents."},
    {"id": 6, "title": "COMIC CHAOS", "genre": ["Comedy", "Family"], "duration": 95, "rating": "PG", "imdb": 7.2, "price": 160, "emoji": "😂", "desc": "A family vacation goes hilariously wrong when their RV is hijacked by a runaway circus."},
]

THEATRES = {
    "PVR Cinemas – Phoenix Mall": {"screens": ["Screen 1 – IMAX", "Screen 2 – 4DX", "Screen 3 – Standard"]},
    "INOX – Infinity Mall":       {"screens": ["Screen A – Dolby", "Screen B – Standard", "Screen C – Premium"]},
    "Cinepolis – R-City Mall":    {"screens": ["Hall 1 – IMAX", "Hall 2 – Recliner", "Hall 3 – Standard"]},
    "Carnival Cinemas – Thane":   {"screens": ["Screen I – Standard", "Screen II – 3D"]},
}

SHOWTIMES = ["10:00 AM", "12:30 PM", "03:00 PM", "06:00 PM", "09:15 PM"]

ROWS    = ["A","B","C","D","E","F","G","H"]
COLS    = list(range(1, 11))
PRICES  = {"A": 1.5, "B": 1.5, "C": 1.2, "D": 1.2, "E": 1.0, "F": 1.0, "G": 0.9, "H": 0.9}

# ── Session State ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "step": 1,
        "selected_movie": None,
        "selected_theatre": None,
        "selected_screen": None,
        "selected_date": date.today() + timedelta(days=1),
        "selected_showtime": None,
        "selected_seats": [],
        "booked_seats": {},      # key: f"{theatre}|{screen}|{date}|{show}" → list of seats
        "booking_name": "",
        "booking_phone": "",
        "booking_email": "",
        "booking_confirmed": False,
        "booking_id": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Helpers ───────────────────────────────────────────────────────────────────
def seat_key():
    return f"{st.session_state.selected_theatre}|{st.session_state.selected_screen}|{st.session_state.selected_date}|{st.session_state.selected_showtime}"

def get_booked_seats():
    return st.session_state.booked_seats.get(seat_key(), [])

def generate_booking_id():
    return "CB" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

def go_to(step):
    st.session_state.step = step
    st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cinebook-header">
  <div class="cinebook-logo">🎬 CineBook</div>
  <div class="cinebook-tagline">Your Ultimate Movie Ticket Experience</div>
</div>
""", unsafe_allow_html=True)

# ── Steps Bar ────────────────────────────────────────────────────────────────
step = st.session_state.step
steps = ["1 · MOVIE", "2 · THEATRE", "3 · SEATS", "4 · DETAILS", "5 · CONFIRM"]
bar_html = '<div class="steps-bar">'
for i, s in enumerate(steps, 1):
    cls = "active" if i == step else ("done" if i < step else "step")
    bar_html += f'<div class="step {cls}">{s}</div>'
bar_html += '</div>'
st.markdown(bar_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════
# STEP 1 – Choose Movie
# ════════════════════════════════════════════════════
if step == 1:
    st.markdown('<div class="section-title">NOW SHOWING</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for idx, movie in enumerate(MOVIES):
        with cols[idx % 3]:
            genres_html = "".join(f'<span class="genre-badge">{g}</span>' for g in movie["genre"])
            st.markdown(f"""
            <div class="movie-card">
              <div style="font-size:3rem; text-align:center; margin-bottom:0.5rem">{movie['emoji']}</div>
              <div class="movie-title">{movie['title']}</div>
              <div class="movie-meta">⏱ {movie['duration']} min &nbsp;|&nbsp; 🎫 ₹{movie['price']}</div>
              <div>{genres_html} <span class="rating-badge">⭐ {movie['imdb']}</span></div>
              <div style="color:#8080a0; font-size:0.82rem; margin-top:0.6rem; line-height:1.4">{movie['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Book Tickets", key=f"movie_{movie['id']}"):
                st.session_state.selected_movie = movie
                go_to(2)

# ════════════════════════════════════════════════════
# STEP 2 – Choose Theatre, Date & Showtime
# ════════════════════════════════════════════════════
elif step == 2:
    m = st.session_state.selected_movie
    st.markdown(f'<div class="section-title">{m["emoji"]} {m["title"]}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 🏛️ Select Theatre")
        theatre = st.selectbox("Theatre", list(THEATRES.keys()), label_visibility="collapsed")
        st.session_state.selected_theatre = theatre

        screens = THEATRES[theatre]["screens"]
        screen = st.selectbox("Screen / Format", screens)
        st.session_state.selected_screen = screen

    with col2:
        st.markdown("#### 📅 Select Date & Time")
        min_date = date.today()
        max_date = date.today() + timedelta(days=14)
        sel_date = st.date_input("Date", value=st.session_state.selected_date, min_value=min_date, max_value=max_date)
        st.session_state.selected_date = sel_date

        showtime = st.selectbox("Showtime", SHOWTIMES)
        st.session_state.selected_showtime = showtime

    st.markdown("---")
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("◀ Back"):
            go_to(1)
    with c2:
        if st.button("Choose Seats ▶"):
            go_to(3)

# ════════════════════════════════════════════════════
# STEP 3 – Seat Selection
# ════════════════════════════════════════════════════
elif step == 3:
    m  = st.session_state.selected_movie
    booked = get_booked_seats()

    st.markdown(f'<div class="section-title">SELECT YOUR SEATS</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-pill">
        🎬 {m['title']} &nbsp;|&nbsp; 📍 {st.session_state.selected_theatre}
        &nbsp;|&nbsp; 🖥️ {st.session_state.selected_screen}
        &nbsp;|&nbsp; 📅 {st.session_state.selected_date} &nbsp;|&nbsp; ⏰ {st.session_state.selected_showtime}
    </div>
    """, unsafe_allow_html=True)

    # Legend
    st.markdown("""
    <div class="seat-legend">
      <div class="legend-item"><div class="legend-dot" style="background:#1e1e2e;border:1px solid #3a3a5e"></div>Available</div>
      <div class="legend-item"><div class="legend-dot" style="background:#e63946"></div>Selected</div>
      <div class="legend-item"><div class="legend-dot" style="background:#3a3a5e"></div>Booked</div>
      <div class="legend-item"><div class="legend-dot" style="background:rgba(244,162,97,0.3)"></div>Premium (A-B)</div>
    </div>
    """, unsafe_allow_html=True)

    # Screen bar
    st.markdown("""
    <div style="background:linear-gradient(90deg,transparent,#e63946,transparent);
                height:4px;border-radius:2px;margin:1rem 0 0.3rem"></div>
    <div style="text-align:center;color:#6b6b8a;font-size:0.75rem;letter-spacing:3px;
                margin-bottom:1.5rem">── SCREEN ──</div>
    """, unsafe_allow_html=True)

    selected = list(st.session_state.selected_seats)

    # Render seat grid
    for row in ROWS:
        cols_ui = st.columns([0.5] + [1]*10)
        cols_ui[0].markdown(f"<div style='color:#6b6b8a;text-align:center;padding-top:4px;font-weight:600'>{row}</div>", unsafe_allow_html=True)
        for ci, col_num in enumerate(COLS):
            seat_id = f"{row}{col_num}"
            is_booked   = seat_id in booked
            is_selected = seat_id in selected
            is_premium  = row in ["A", "B"]

            if is_booked:
                cols_ui[ci+1].markdown(f"<div style='background:#3a3a5e;border-radius:5px;text-align:center;padding:5px 0;font-size:0.7rem;color:#5a5a7a'>{col_num}</div>", unsafe_allow_html=True)
            else:
                label = "✓" if is_selected else str(col_num)
                bg    = "#e63946" if is_selected else ("rgba(244,162,97,0.15)" if is_premium else "#1e1e2e")
                bc    = "#e63946" if is_selected else ("#f4a261" if is_premium else "#3a3a5e")
                if cols_ui[ci+1].button(label, key=f"seat_{seat_id}", help=seat_id):
                    if is_selected:
                        selected.remove(seat_id)
                    else:
                        if len(selected) < 10:
                            selected.append(seat_id)
                    st.session_state.selected_seats = selected
                    st.rerun()

    # Pricing summary
    if selected:
        total = sum(m["price"] * PRICES[s[0]] for s in selected)
        st.markdown(f"""
        <div class="summary-card" style="margin-top:1.5rem">
          <div class="summary-row"><span class="summary-label">Selected Seats</span><span class="summary-value">{', '.join(selected)}</span></div>
          <div class="summary-row"><span class="summary-label">Base Price</span><span class="summary-value">₹{m['price']} / seat</span></div>
          <div class="summary-row"><span class="summary-label">Seats Count</span><span class="summary-value">{len(selected)}</span></div>
          <div class="summary-row" style="border:none"><span class="summary-label summary-total">TOTAL</span><span class="summary-value summary-total">₹{total:.0f}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("◀ Back"):
            go_to(2)
    with c2:
        if selected:
            if st.button(f"Proceed to Details ({len(selected)} seats) ▶"):
                go_to(4)
        else:
            st.info("Please select at least one seat.")

# ════════════════════════════════════════════════════
# STEP 4 – Booking Details
# ════════════════════════════════════════════════════
elif step == 4:
    m        = st.session_state.selected_movie
    selected = st.session_state.selected_seats
    total    = sum(m["price"] * PRICES[s[0]] for s in selected)

    st.markdown('<div class="section-title">BOOKING DETAILS</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("#### 👤 Personal Information")
        name  = st.text_input("Full Name",  value=st.session_state.booking_name,  placeholder="e.g. Rahul Sharma")
        phone = st.text_input("Phone Number", value=st.session_state.booking_phone, placeholder="+91 98765 43210")
        email = st.text_input("Email Address", value=st.session_state.booking_email, placeholder="rahul@email.com")
        st.session_state.booking_name  = name
        st.session_state.booking_phone = phone
        st.session_state.booking_email = email

        st.markdown("#### 💳 Payment Method")
        payment = st.radio("", ["💳 Credit / Debit Card", "📱 UPI / QR Code", "🏦 Net Banking", "💰 Paytm / PhonePe"], horizontal=False)

        if "UPI" in payment:
            st.text_input("Enter UPI ID", placeholder="yourname@upi")
        elif "Card" in payment:
            c1, c2 = st.columns(2)
            c1.text_input("Card Number", placeholder="•••• •••• •••• ••••", max_chars=19)
            c2.text_input("Expiry", placeholder="MM/YY", max_chars=5)
            c1.text_input("Name on Card", placeholder="RAHUL SHARMA")
            c2.text_input("CVV", placeholder="•••", max_chars=3, type="password")

    with col2:
        st.markdown(f"""
        <div class="summary-card">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:#f0f0ff;letter-spacing:2px;margin-bottom:0.8rem">ORDER SUMMARY</div>
          <div class="summary-row"><span class="summary-label">🎬 Movie</span><span class="summary-value">{m['title']}</span></div>
          <div class="summary-row"><span class="summary-label">📍 Theatre</span><span class="summary-value" style="font-size:0.8rem">{st.session_state.selected_theatre.split('–')[0].strip()}</span></div>
          <div class="summary-row"><span class="summary-label">🖥️ Screen</span><span class="summary-value">{st.session_state.selected_screen}</span></div>
          <div class="summary-row"><span class="summary-label">📅 Date</span><span class="summary-value">{st.session_state.selected_date}</span></div>
          <div class="summary-row"><span class="summary-label">⏰ Show</span><span class="summary-value">{st.session_state.selected_showtime}</span></div>
          <div class="summary-row"><span class="summary-label">💺 Seats</span><span class="summary-value">{', '.join(selected)}</span></div>
          <div class="summary-row" style="border:none;margin-top:0.5rem"><span class="summary-label summary-total">TOTAL</span><span class="summary-value summary-total">₹{total:.0f}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("◀ Back"):
            go_to(3)
    with c2:
        if st.button("💳 Confirm & Pay ▶"):
            if not name.strip():
                st.error("Please enter your full name.")
            elif not phone.strip():
                st.error("Please enter your phone number.")
            elif not email.strip():
                st.error("Please enter your email address.")
            else:
                # Mark seats as booked
                key = seat_key()
                existing = st.session_state.booked_seats.get(key, [])
                st.session_state.booked_seats[key] = existing + selected
                st.session_state.booking_id = generate_booking_id()
                st.session_state.booking_confirmed = True
                go_to(5)

# ════════════════════════════════════════════════════
# STEP 5 – Confirmation
# ════════════════════════════════════════════════════
elif step == 5:
    m        = st.session_state.selected_movie
    selected = st.session_state.selected_seats
    total    = sum(m["price"] * PRICES[s[0]] for s in selected)

    st.markdown("""
    <div style="text-align:center;padding:2rem 0 1rem">
      <div style="font-size:4rem">🎉</div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;color:#2a9d8f;letter-spacing:3px">BOOKING CONFIRMED!</div>
      <div style="color:#6b6b8a;margin-top:0.3rem">Your tickets are ready. Enjoy the show!</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ticket-card">
      <div style="font-size:2.5rem">{m['emoji']}</div>
      <div class="ticket-id">{st.session_state.booking_id}</div>
      <div style="color:#6b6b8a;font-size:0.78rem;letter-spacing:2px;margin-bottom:1rem">BOOKING ID</div>
      <hr class="ticket-divider">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:#f0f0ff;letter-spacing:2px;margin-bottom:0.5rem">{m['title']}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;text-align:left;margin:1rem 0">
        <div><div style="color:#6b6b8a;font-size:0.75rem;text-transform:uppercase">Theatre</div><div style="color:#f0f0ff;font-size:0.88rem;font-weight:500">{st.session_state.selected_theatre.split('–')[0].strip()}</div></div>
        <div><div style="color:#6b6b8a;font-size:0.75rem;text-transform:uppercase">Screen</div><div style="color:#f0f0ff;font-size:0.88rem;font-weight:500">{st.session_state.selected_screen}</div></div>
        <div><div style="color:#6b6b8a;font-size:0.75rem;text-transform:uppercase">Date</div><div style="color:#f0f0ff;font-size:0.88rem;font-weight:500">{st.session_state.selected_date}</div></div>
        <div><div style="color:#6b6b8a;font-size:0.75rem;text-transform:uppercase">Showtime</div><div style="color:#f0f0ff;font-size:0.88rem;font-weight:500">{st.session_state.selected_showtime}</div></div>
        <div><div style="color:#6b6b8a;font-size:0.75rem;text-transform:uppercase">Seats</div><div style="color:#e63946;font-size:0.88rem;font-weight:600">{', '.join(selected)}</div></div>
        <div><div style="color:#6b6b8a;font-size:0.75rem;text-transform:uppercase">Total Paid</div><div style="color:#f4a261;font-size:0.88rem;font-weight:600">₹{total:.0f}</div></div>
      </div>
      <hr class="ticket-divider">
      <div style="color:#6b6b8a;font-size:0.78rem">Booked for &nbsp;<strong style="color:#f0f0ff">{st.session_state.booking_name}</strong></div>
      <div style="color:#6b6b8a;font-size:0.78rem;margin-top:2px">{st.session_state.booking_email} &nbsp;|&nbsp; {st.session_state.booking_phone}</div>
      <div style="margin-top:1rem;background:rgba(42,157,143,0.1);border:1px solid rgba(42,157,143,0.3);
                  border-radius:8px;padding:0.5rem;color:#2a9d8f;font-size:0.82rem">
        ✅ Confirmation sent to your email
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎬 Book Another Movie"):
            for key in ["step","selected_movie","selected_theatre","selected_screen",
                        "selected_date","selected_showtime","selected_seats",
                        "booking_name","booking_phone","booking_email",
                        "booking_confirmed","booking_id"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#2a2a3e;font-size:0.78rem;padding:3rem 0 1rem;
            border-top:1px solid #1a1a2e;margin-top:3rem">
  🎬 CineBook &nbsp;|&nbsp; Made with ❤️ using Streamlit &nbsp;|&nbsp; © 2025
</div>
""", unsafe_allow_html=True)
