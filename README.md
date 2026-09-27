# AI Career Guidance System (CareerPath AI)

A complete, professional, 100% free, offline-capable final-year academic web application designed to help students and job seekers discover ideal career paths through transparent algorithm-based compatibility scoring, skill gap analysis, interactive career roadmaps, and free learning resources.

---

## 🌟 Key Project Highlights

- **100% Free & Offline-Capable**: Operates locally with **zero paid API dependencies** (No OpenAI, Gemini, Claude, Firebase, AWS, or paid database costs required).
- **Transparent Multi-Factor Scoring Engine**: Explores education, technical skills, soft skills, interests, work preferences, and assessment inputs to generate explainable compatibility match scores (0–100%).
- **Deep Skill Gap Analysis**: Compares user profile skills against career requirements to present acquired vs missing skills with priority ranking.
- **Interactive Career Roadmaps & Free Learning Resources**: Offers step-by-step career progression roadmaps alongside curated 100% free learning resource documentation (MDN, Python Docs, freeCodeCamp, Microsoft Learn, Kaggle, etc.).
- **Career Comparison Engine**: Allows side-by-side comparison of up to 3 careers (skills, growth, match scores).
- **Admin Management & Live Analytics**: Complete administrative dashboard featuring user management, career profile management (Add/Edit/Deactivate), and real-time interactive charts powered by Chart.js.

---

## 🛠️ Technology Stack

### Backend
- **Python 3**
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Object-Relational Mapping (ORM)
- **SQLite**: Local relational database
- **Werkzeug**: Password hashing (`generate_password_hash`, `check_password_hash`) and secure sessions

### Frontend
- **HTML5 & CSS3**
- **Bootstrap 5**: Modern responsive framework
- **Bootstrap Icons**: Vector icon library
- **Vanilla JavaScript**: Form wizard, alert handlers, and UI logic
- **Chart.js**: Interactive analytics charts

### Scoring Engine & Data Analysis
- **Python-based transparent multi-factor weighting engine** (utilizing `pandas`, `numpy`, and `scikit-learn` libraries where required).

## ☁️ Vercel & MongoDB Atlas Hosting Guide

You can easily host this application for FREE on **Vercel** with **MongoDB Atlas** database!

### 1. Set up MongoDB Atlas (Free Cloud Database)
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and create a free account.
2. Create a **Shared Free Cluster (M0)**.
3. Under **Database Access**, create a user (e.g. username: `admin`, password: `yourpassword`).
4. Under **Network Access**, click **Add IP Address** -> Select **Allow Access from Anywhere (`0.0.0.0/0`)**.
5. Click **Connect** -> Choose **Drivers (Python)** -> Copy your Connection String (`mongodb+srv://admin:yourpassword@cluster0.xxx.mongodb.net/career_guidance?retryWrites=true&w=majority`).

### 2. Seed Data into MongoDB Atlas
Run the MongoDB seed script on your local machine:
```bash
# Set your MongoDB Atlas URI
set MONGO_URI="mongodb+srv://admin:yourpassword@cluster0.xxx.mongodb.net/career_guidance?retryWrites=true&w=majority"

# Run the seeding script
python seed_mongo.py
```

### 3. Deploy to Vercel (3 Simple Steps)
1. Push your project to **GitHub**.
2. Go to [Vercel](https://vercel.com) and click **Add New Project** -> Import your GitHub Repository.
3. In the Vercel project configuration, add the **Environment Variables**:
   - `SECRET_KEY`: `careerpath-ai-secret-key-production`
   - `MONGO_URI`: `mongodb+srv://admin:yourpassword@cluster0.xxx.mongodb.net/career_guidance?retryWrites=true&w=majority`
4. Click **Deploy**! Vercel will build and host your site with a free `https://your-app.vercel.app` live URL! 🚀

---

## 📋 System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python Version**: Python 3.8+ (Python 3.14 compatible)
- **Web Browser**: Any modern web browser (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari)

---

## 🚀 Quick Setup & Installation Guide

### Step 1: Open Terminal / Command Prompt
Navigate to the project root directory:
```bash
cd "d:\fial_year_project\AI Career Guidance System"
```

### Step 2: Create & Activate Virtual Environment
On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup & Seed Initial Data
Run the seeding script to initialize the SQLite database and populate 20+ realistic career profiles, preset skills, interests, and the administrator account:
```bash
python seed.py
```

### Step 5: Start the Flask Application
```bash
python app.py
```
The application will launch locally at:
**`http://127.0.0.1:5000`**

---

## 🔑 Default Credentials

### Administrator Account
- **Email**: `admin@careerpath.ai`
- **Password**: `admin123`
- **Role**: ADMIN (Access to `/admin` dashboard, career management, user management, and analytics)

### User Account
Create any new user account via the Registration page (`/register`) to start as a standard job seeker / student user.

---

## 🧮 Recommendation Scoring Algorithm

The scoring engine (`services/recommendation_engine.py`) calculates transparent compatibility scores (0–100%) using weighted dimensions:

| Dimension | Weight | Description |
| :--- | :---: | :--- |
| **Technical Skills** | **30%** | Overlap ratio between user skills and career required technical skills. |
| **Education** | **20%** | Qualification, degree, and field of study alignment with career requirements. |
| **Interests** | **20%** | Match between user domain interests and career classification. |
| **Soft Skills** | **10%** | Presence of key soft skill competencies. |
| **Work Environment** | **10%** | Preference alignment with available role work styles (Remote, Hybrid, MNC, Startup). |
| **Personality & Assessment** | **10%** | Work style preference survey and primary career goal alignment. |

### Compatibility Scoring Tiers
- **90% – 100%**: Excellent Match
- **80% – 89%**: Strong Match
- **70% – 79%**: Good Match
- **50% – 69%**: Moderate Match
- **Below 50%**: Low Match

---

## 📁 Project Structure

```
ai_career_guidance/
│
├── app.py                      # Flask main entry point & blueprint registration
├── config.py                   # App configuration & database URI
├── requirements.txt            # Python dependencies
├── seed.py                     # Database initialization & seed script
├── .env.example                # Environment variables template
│
├── database/
│   └── career_guidance.db      # SQLite database file
│
├── models/
│   ├── __init__.py             # SQLAlchemy instance initialization
│   ├── user.py                 # User model & Werkzeug hashing
│   ├── profile.py              # Profile, Skill, UserSkill, Interest, UserInterest models
│   ├── career.py               # Career & SavedCareer models
│   └── recommendation.py       # Recommendation model & score tiers
│
├── routes/
│   ├── __init__.py             # Login & Admin auth decorators
│   ├── auth.py                 # Register, Login, Logout routes
│   ├── profile.py              # 7-Step Onboarding profile form routes
│   ├── career.py               # Dashboard, Recommendations, Skill Gap, Roadmap, Compare routes
│   └── admin.py                # Admin dashboard, Career CRUD, User list, Analytics routes
│
├── services/
│   ├── __init__.py
│   ├── recommendation_engine.py# Multi-factor scoring logic & reason generation
│   ├── skill_analysis.py       # Skill gap analysis & priority ranking
│   └── career_data.py          # Category helpers & admin analytics query service
│
├── templates/
│   ├── base.html               # Main base layout with navbar & footer disclaimer
│   ├── index.html              # Landing page
│   ├── login.html              # Authentication login page
│   ├── register.html           # User registration page
│   ├── onboarding.html         # 7-Step multi-step questionnaire wizard
│   ├── dashboard.html          # User overview dashboard
│   ├── recommendations.html    # Ranked career match recommendations
│   ├── career_details.html     # Role overview, skills, and growth timeline
│   ├── skill_gap.html          # Skill gap analysis & acquired vs missing matrix
│   ├── learning_path.html      # Step-by-step roadmap & free learning resources
│   ├── explore.html            # Searchable career directory with category filters
│   ├── saved_careers.html      # Bookmarked careers page
│   ├── compare.html            # Side-by-side career comparison matrix
│   ├── 404.html                # 404 Page Not Found error handler
│   ├── 500.html                # 500 Internal Error handler
│   └── admin/
│       ├── dashboard.html      # Admin portal dashboard
│       ├── careers.html        # Career management table
│       ├── career_form.html    # Add / Edit career form
│       ├── users.html          # User account management table
│       └── analytics.html      # Chart.js system analytics dashboard
│
└── static/
    ├── css/
    │   └── style.css           # Custom CSS stylesheet with modern indigo theme
    └── js/
        └── app.js              # Onboarding form wizard & Chart.js helpers
```

---

## 🔮 Future Enhancements

- Integration of downloadable PDF career report summaries.
- Peer mentorship matching based on common career targets.
- Live job market API integration for regional salary benchmarks.

---

## 📜 Disclaimer

*This system provides educational career guidance based on the information provided by the user. Recommendations are intended as decision-support information and should not be considered professional career, employment, financial, or psychological advice.*
