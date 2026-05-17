# 🚦 DriveLegal — AI-Powered Traffic Law Assistant

> Road Safety Hackathon 2026 | Centre of Excellence for Road Safety (CoERS) | IIT Madras

DriveLegal is an AI-powered platform that provides location-specific traffic laws, violation details, fine schedules, and an intelligent chatbot to help citizens understand and comply with road safety rules.

---

## 👥 Team — Simple Engineers

| Name | Role |
|---|---|
| Rahul Das | Frontend Developer |
| Ayoshree Dutta | Frontend Developer |
| Nabarka Mazumdar | Data & Rules Engine |
| Subhadip Bhunia  | UI Designer        |
| Riddhismita Nath | Backend Developer  |
| Souradeep Tarafdar | Backend Developer  |

---

## 🗂️ Project Structure

```
Drive_Legal/
├── backend/
│ ├── app.py
│ ├── db.py
│ ├── seed_admins.py
│ ├── requirements.txt
│ ├── .env
│ ├── middleware/
│ │ └── auth.py
│ ├── models/
│ │ ├── user_model.py
│ │ ├── fine_model.py
│ │ └── history_model.py
│ ├── routes/
│ │ ├── auth_routes.py
│ │ ├── fine_routes.py
│ │ ├── rules_routes.py
│ │ ├── location_routes.py
│ │ ├── history_routes.py
│ │ └── chatbot_routes.py
│ └── services/
│ ├── auth_service.py
│ ├── jwt_service.py
│ ├── location_service.py
│ ├── rule_engine.py
│ ├── fine_calculator.py
│ └── chatbot_service.py
├── frontend/
│ ├── pages/
│ │ ├── index.html
│ │ ├── login.html
│ │ ├── signup.html
│ │ ├── adminlogin.html
│ │ ├── admin.html
│ │ ├── mainpage.html
│ │ ├── RulesPage.html
│ │ ├── ViewFines.html
│ │ ├── EmergencyContact.html
│ │ ├── About.html
│ │ ├── chatpage.html
│ │ └── ReceiptPage.html
│ ├── css/
│ │ ├── style.css
│ │ ├── stylelogin.css
│ │ ├── stylesignup.css
│ │ ├── stylemain.css
│ │ ├── admin.css
│ │ ├── stylerules.css
│ │ ├── viewfines.css
│ │ ├── styleemergency.css
│ │ ├── styleabout.css
│ │ └── chatpage.css
│ ├── js/
│ │ ├── api.js
│ │ ├── login.js
│ │ ├── signup.js
│ │ ├── adminlogin.js
│ │ ├── mainpage.js
│ │ ├── admin.js
│ │ ├── rules.js
│ │ ├── viewfines.js
│ │ ├── receipt.js
│ │ └── chatbot.js
│ └── assets/
│ ├── main_image.jpg
│ ├── main_image_mobile.jpg
│ ├── main_mobile_bg.png
│ └── main_pagebg.png
├── data/
│ └── state_rules/
│ ├── west_bengal.json
│ ├── delhi.json
│ └── tamil_nadu.json
├── run_chatbot.py
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Chatbot | FastAPI, Groq (LLaMA 3 70B) |
| Database | MongoDB Atlas |
| Auth | JWT (PyJWT) |
| PDF | ReportLab |
| Location | Geopy (Nominatim) |
| Password | Werkzeug Security |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- MongoDB Atlas account
- Groq API key (free at https://console.groq.com)

### Installation

**Step 1 — Clone the repository:**
```bash
git clone https://github.com/SOURAT/Ro_Safe.git
cd Drive_Legal
```

**Step 2 — Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
```

**Step 3 — Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**Step 4 — Set up environment variables:**
```bash
cd backend
cp .env.example .env
```

Fill in your `.env`:
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=drivelegal
JWT_SECRET=your_secret_key_here
JWT_EXPIRE_MIN=60
FLASK_ENV=development
GROQ_API_KEY=gsk_your_groq_api_key

Get your free GROQ API KEY here : https://console.groq.com

```

**Step 5 — Seed admin users:**
```bash
cd backend
python seed_admins.py
```

**Step 6 — Run Flask backend:**
```bash
cd backend
python app.py
```

**Step 7 — Run Chatbot server (new terminal):**
```bash
cd Drive_Legal
python run_chatbot.py
```

---

## 🌐 API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | /auth/signup | Register new user | ❌ |
| POST | /auth/user-login | User login | ❌ |
| POST | /auth/admin-login | Admin login | ❌ |

### Rules
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | /rules/?state=&city= | Get traffic rules by location | ✅ |

### Fine
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | /fine/calculate-fine | Calculate challan fine | ✅ Admin |
| POST | /fine/generate-receipt | Generate PDF receipt | ✅ |

### Location
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | /location/ | Detect location from GPS | ✅ |

### History
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | /history/fine-history | Get history by vehicle (admin) | ✅ Admin |
| GET | /history/my-history | Get user's own fines | ✅ User |

### Chatbot
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | /chat | Send message to DriveBot | ❌ |
| GET | /health | Health check | ❌ |

---

## 👤 Admin Credentials

| Key | Password |
|---|---|
| Rahul_Das | das123 |
| Ayoshree_Dutta | dutta123 |
| Nabarka_Mazumdar | nba123 |
| Subhadip_Bhunia | bhu123 |
| Riddhismita_Nath | smita123 |
| Souradeep_Tarafdar | soura123 |

---

## ✨ Features

- 📍 **Geo-fenced Rules** — Location-specific traffic laws using GPS
- 💰 **Challan Calculator** — Calculate fines based on violation and state
- 📄 **PDF Receipt** — Downloadable challan receipts
- 🤖 **AI Chatbot** — DriveBot powered by LLaMA 3 70B via Groq
- 🔐 **JWT Auth** — Secure login for users and admins
- 📋 **Fine History** — Track violation history by vehicle number
- 🌍 **Global Support** — Rules for multiple states and countries

---

## 📋 Evaluation Criteria Coverage

| Criteria | Implementation |
|---|---|
| Legal accuracy | Motor Vehicles Act 1988 & 2019 Amendment |
| Challan calculator | `/fine/calculate-fine` with repeated offence detection |
| Information integration | State-wise JSON + national rules in chatbot |
| User interface | Responsive dark theme UI |
| Geo-fenced lookup | Geopy + Nominatim GPS detection |
| Offline functionality | Cached rules in localStorage |
| Global applicability | International rules support |

---

## 📝 License

MIT License — © 2026 Simple Engineers
```

