import os
import sys
import json
from datetime import datetime
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.environ.get('MONGO_URI') or os.environ.get('MONGODB_URI')
if not mongo_uri:
    print("❌ Error: MONGO_URI environment variable is not set!")
    print("Please set MONGO_URI in your environment or .env file before running seed_mongo.py.")
    sys.exit(1)

try:
    from pymongo import MongoClient
    client = MongoClient(mongo_uri)
    db = client.get_default_database(default='career_guidance')
    print("✅ Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB Atlas: {e}")
    sys.exit(1)

def seed_mongo():
    print("Clearing existing collections in MongoDB...")
    db.users.drop()
    db.profiles.drop()
    db.skills.drop()
    db.interests.drop()
    db.careers.drop()

    print("Seeding Skills into MongoDB...")
    tech_skills = [
        'Python', 'Java', 'JavaScript', 'React', 'HTML', 'CSS', 'SQL', 'C', 'C++', 
        'Data Analysis', 'Machine Learning', 'Cloud Computing', 'Networking', 
        'Node.js', 'MongoDB', 'REST APIs', 'Git', 'Docker', 'Kubernetes', 
        'Cyber Security', 'Figma', 'Statistics', 'Digital Marketing', 'SEO', 
        'Financial Modeling', 'Technical Writing', 'Deep Learning', 'Tableau', 'Power BI'
    ]
    soft_skills = [
        'Communication', 'Leadership', 'Problem Solving', 'Teamwork', 'Creativity', 
        'Time Management', 'Critical Thinking', 'Adaptability', 'Negotiation', 'Public Speaking'
    ]

    skill_docs = [{'name': s, 'category': 'technical'} for s in tech_skills] + \
                 [{'name': s, 'category': 'soft'} for s in soft_skills]
    db.skills.insert_many(skill_docs)

    print("Seeding Interests into MongoDB...")
    interests = [
        'Software Development', 'Data Science', 'AI / ML', 'Cybersecurity', 
        'UI/UX', 'Cloud Computing', 'Networking', 'Business', 'Finance', 
        'Marketing', 'Teaching', 'Research'
    ]
    db.interests.insert_many([{'name': i} for i in interests])

    print("Seeding Admin User into MongoDB...")
    admin_id = db.users.insert_one({
        'name': 'System Administrator',
        'email': 'admin@careerpath.ai',
        'password_hash': generate_password_hash('admin123'),
        'role': 'ADMIN',
        'created_at': datetime.utcnow()
    }).inserted_id

    db.profiles.insert_one({
        'user_id': admin_id,
        'qualification': 'Master of Science',
        'degree': 'M.Sc Computer Science',
        'field_of_study': 'Computer Science',
        'profile_completion': 100,
        'created_at': datetime.utcnow()
    })

    print("Seeding Careers into MongoDB...")
    careers_data = [
        {
            "name": "Full Stack Developer",
            "category": "Software",
            "description": "Design and construct complete end-to-end web applications, managing both front-end client user interfaces and back-end database systems.",
            "required_education": ["B.Sc Computer Science", "B.Tech IT", "Software Engineering"],
            "required_skills": ["JavaScript", "HTML", "CSS", "React", "Node.js", "SQL", "REST APIs", "Git"],
            "soft_skills": ["Problem Solving", "Communication", "Teamwork", "Adaptability"],
            "interests": ["Software Development", "UI/UX", "Cloud Computing"],
            "work_environment": ["Remote", "Hybrid", "Office", "Startup", "MNC"],
            "career_growth": [
                {"level": "Entry Level", "title": "Junior Full Stack Developer"},
                {"level": "Mid Level", "title": "Full Stack Engineer"},
                {"level": "Senior Level", "title": "Senior Full Stack Engineer"},
                {"level": "Lead / Manager", "title": "Lead Software Architect"}
            ],
            "learning_resources": [
                {"title": "freeCodeCamp Responsive Web Design & JS", "url": "https://www.freecodecamp.org/learn/", "type": "Interactive Course"},
                {"title": "MDN Web Docs (HTML/CSS/JavaScript)", "url": "https://developer.mozilla.org/", "type": "Official Documentation"},
                {"title": "React Official Documentation & Tutorials", "url": "https://react.dev/learn", "type": "Official Guide"}
            ],
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Frontend Developer",
            "category": "Software",
            "description": "Specialize in crafting interactive, highly responsive, visually rich user interfaces and web clients using modern front-end technologies.",
            "required_education": ["B.Sc Computer Science", "B.A Design", "Diploma in IT"],
            "required_skills": ["HTML", "CSS", "JavaScript", "React", "Figma", "Git"],
            "soft_skills": ["Creativity", "Communication", "Teamwork", "Time Management"],
            "interests": ["Software Development", "UI/UX"],
            "work_environment": ["Remote", "Hybrid", "Startup", "MNC", "Freelance"],
            "career_growth": [
                {"level": "Entry Level", "title": "Junior Frontend Developer"},
                {"level": "Mid Level", "title": "Frontend Engineer"},
                {"level": "Senior Level", "title": "Senior UI/Frontend Engineer"},
                {"level": "Lead / Manager", "title": "UI Technical Lead"}
            ],
            "learning_resources": [
                {"title": "MDN Web Docs - Front End Web Developer", "url": "https://developer.mozilla.org/en-US/docs/Learn", "type": "Guide"},
                {"title": "W3Schools HTML & CSS Tutorials", "url": "https://www.w3schools.com/html/", "type": "Interactive Tutorial"}
            ],
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Data Scientist",
            "category": "Data",
            "description": "Analyze complex sets of raw quantitative data to extract actionable insights, build predictive models, and optimize business decisions.",
            "required_education": ["B.Sc Data Science", "B.Tech Computer Science", "B.Sc Statistics", "M.Sc Mathematics"],
            "required_skills": ["Python", "SQL", "Statistics", "Machine Learning", "Data Analysis", "Tableau", "Power BI"],
            "soft_skills": ["Critical Thinking", "Problem Solving", "Communication", "Public Speaking"],
            "interests": ["Data Science", "AI / ML", "Research", "Business"],
            "work_environment": ["Remote", "Hybrid", "Office", "MNC", "Startup"],
            "career_growth": [
                {"level": "Entry Level", "title": "Junior Data Analyst / Scientist"},
                {"level": "Mid Level", "title": "Data Scientist"},
                {"level": "Senior Level", "title": "Senior Data Scientist"},
                {"level": "Lead / Manager", "title": "Head of Analytics & Data Science"}
            ],
            "learning_resources": [
                {"title": "Kaggle Learn Data Science & Python", "url": "https://www.kaggle.com/learn", "type": "Interactive Modules"},
                {"title": "Python Data Science Handbook", "url": "https://jakevdp.github.io/PythonDataScienceHandbook/", "type": "Free eBook"}
            ],
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "name": "AI / Machine Learning Engineer",
            "category": "AI",
            "description": "Research, design, build, and deploy intelligent algorithms and neural networks that learn from data and automate complex tasks.",
            "required_education": ["B.Tech Computer Science", "B.Tech AI & Data Science", "M.Tech AI"],
            "required_skills": ["Python", "Machine Learning", "Deep Learning", "Statistics", "C++", "Docker"],
            "soft_skills": ["Problem Solving", "Critical Thinking", "Adaptability", "Creativity"],
            "interests": ["AI / ML", "Data Science", "Research"],
            "work_environment": ["Remote", "Hybrid", "MNC", "Startup"],
            "career_growth": [
                {"level": "Entry Level", "title": "Junior ML Engineer"},
                {"level": "Mid Level", "title": "Machine Learning Engineer"},
                {"level": "Senior Level", "title": "Senior AI Architect"},
                {"level": "Lead / Manager", "title": "Director of AI Engineering"}
            ],
            "learning_resources": [
                {"title": "Google AI for Everyone & Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "type": "Interactive Course"},
                {"title": "Fast.ai Practical Deep Learning for Coders", "url": "https://course.fast.ai/", "type": "Video Course"}
            ],
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Cybersecurity Analyst",
            "category": "Cybersecurity",
            "description": "Protect organizational networks, systems, and data infrastructure against unauthorized access, cyber threats, vulnerabilities, and attacks.",
            "required_education": ["B.Sc Cyber Security", "B.Tech Computer Science", "Certified Information Systems Security Professional"],
            "required_skills": ["Cyber Security", "Networking", "Python", "Linux", "C"],
            "soft_skills": ["Critical Thinking", "Problem Solving", "Time Management", "Communication"],
            "interests": ["Cybersecurity", "Networking", "Software Development"],
            "work_environment": ["Office", "Hybrid", "MNC", "Govt Sector"],
            "career_growth": [
                {"level": "Entry Level", "title": "Junior Cybersecurity Analyst"},
                {"level": "Mid Level", "title": "Information Security Engineer"},
                {"level": "Senior Level", "title": "Senior Security Consultant"},
                {"level": "Lead / Manager", "title": "Chief Information Security Officer (CISO)"}
            ],
            "learning_resources": [
                {"title": "Cybrary Free Cybersecurity Courses", "url": "https://www.cybrary.it/", "type": "Online Courses"},
                {"title": "TryHackMe Hands-on Cyber Security Labs", "url": "https://tryhackme.com/", "type": "Hands-on Practice"}
            ],
            "is_active": True,
            "created_at": datetime.utcnow()
        }
    ]
    db.careers.insert_many(careers_data)

    print("🎉 MongoDB Atlas Database successfully seeded with careers, admin user, skills, and interests!")

if __name__ == '__main__':
    seed_mongo()
