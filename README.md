# 🎬 CineBook – Movie Ticket Booking App

A beautiful, fully functional movie ticket booking web app built with **Streamlit**.

## Features
- 🎬 Browse Now Showing movies
- 🏛️ Choose theatre, screen format, date & showtime
- 💺 Interactive seat selection grid (with booked/available/premium seats)
- 👤 Booking details + payment method selection
- 🎉 Booking confirmation with ticket ID

---

## 🚀 Deployment Guide

### Option A: Run on Google Colab (Quick Test)

1. Open a new Google Colab notebook
2. Paste and run these cells:

```python
# Cell 1 – Install dependencies
!pip install streamlit -q
!npm install -g localtunnel -q
```

```python
# Cell 2 – Write app.py  (upload app.py to Colab first OR paste code directly)
# If you uploaded app.py, skip this cell
```

```python
# Cell 3 – Run the app
import subprocess, threading, time

def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py",
                    "--server.port", "8501",
                    "--server.headless", "true"])

t = threading.Thread(target=run_streamlit, daemon=True)
t.start()
time.sleep(5)

# Get public URL via localtunnel
!npx localtunnel --port 8501
```

> 🔑 When localtunnel asks for a password, go to https://ipv4.icanhazip.com to get your IP.

---

### Option B: Deploy to Streamlit Cloud (Permanent + Free) ✅ RECOMMENDED

#### Step 1 – Push to GitHub

```bash
# On your local machine or Colab terminal:
git init
git add .
git commit -m "Initial commit – CineBook app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cinebook.git
git push -u origin main
```

**Or use Colab to push:**
```python
import os
os.chdir('/content')

# Clone or init repo
!git config --global user.email "you@example.com"
!git config --global user.name "Your Name"
!git init cinebook
!cp app.py cinebook/
!cp requirements.txt cinebook/
os.chdir('cinebook')
!git add .
!git commit -m "CineBook app"

# Push to GitHub (use personal access token as password)
!git remote add origin https://github.com/YOUR_USERNAME/cinebook.git
!git push -u origin main
```

#### Step 2 – Deploy on Streamlit Cloud

1. Go to **https://share.streamlit.io**
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository: `YOUR_USERNAME/cinebook`
5. Branch: `main`
6. Main file path: `app.py`
7. Click **"Deploy!"**

✅ Your app will be live at:
`https://YOUR_USERNAME-cinebook-app-xxxx.streamlit.app`

---

### Option C: Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/cinebook.git
cd cinebook
pip install -r requirements.txt
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📁 File Structure

```
cinebook/
├── app.py            ← Main Streamlit app (all-in-one)
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

## 🛠️ Customisation Tips

| What to change | Where in app.py |
|---|---|
| Add/edit movies | `MOVIES` list (~line 50) |
| Add theatres | `THEATRES` dict (~line 65) |
| Change showtimes | `SHOWTIMES` list (~line 70) |
| Adjust seat prices | `PRICES` dict (~line 75) |
| Change ticket price | `"price"` key in each movie |

---

Made with ❤️ using [Streamlit](https://streamlit.io)
