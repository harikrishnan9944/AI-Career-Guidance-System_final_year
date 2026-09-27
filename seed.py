import json
from app import create_app
from models import db
from models.user import User
from models.profile import Profile, Skill, Interest
from models.career import Career

app = create_app()

def seed_database():
    with app.app_context():
        print("Re-creating database tables...")
        db.drop_all()
        db.create_all()

        print("Seeding Skills...")
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

        for s_name in tech_skills:
            db.session.add(Skill(name=s_name, category='technical'))
            
        for s_name in soft_skills:
            db.session.add(Skill(name=s_name, category='soft'))

        print("Seeding Interests...")
        interests = [
            'Software Development', 'Data Science', 'AI / ML', 'Cybersecurity', 
            'UI/UX', 'Cloud Computing', 'Networking', 'Business', 'Finance', 
            'Marketing', 'Teaching', 'Research'
        ]
        for i_name in interests:
            db.session.add(Interest(name=i_name))

        db.session.commit()

        print("Seeding Default Admin User...")
        admin = User(
            name='System Administrator',
            email='admin@careerpath.ai',
            role='ADMIN'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.flush()

        admin_profile = Profile(
            user_id=admin.id,
            qualification="Master of Science",
            degree="M.Sc Computer Science",
            field_of_study="Computer Science",
            profile_completion=100
        )
        db.session.add(admin_profile)
        db.session.commit()

        print("Seeding 20 Careers with real metadata and free learning resources...")

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
                ]
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
                    {"level": "Senior Level", "title": "Senior UI Engineer"},
                    {"level": "Lead / Manager", "title": "Frontend Architect / UX Lead"}
                ],
                "learning_resources": [
                    {"title": "MDN JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "type": "Documentation"},
                    {"title": "freeCodeCamp Front End Development Libraries", "url": "https://www.freecodecamp.org/learn/front-end-development-libraries/", "type": "Course"}
                ]
            },
            {
                "name": "Backend Developer",
                "category": "Software",
                "description": "Build high-performance server logic, design robust database architectures, and engineer RESTful APIs to power complex application workflows.",
                "required_education": ["B.Sc Computer Science", "B.Tech Computer Engineering"],
                "required_skills": ["Python", "Node.js", "SQL", "MongoDB", "REST APIs", "Git", "Docker"],
                "soft_skills": ["Problem Solving", "Critical Thinking", "Teamwork"],
                "interests": ["Software Development", "Cloud Computing"],
                "work_environment": ["Remote", "Hybrid", "Office", "MNC"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Junior Backend Developer"},
                    {"level": "Mid Level", "title": "Backend Engineer"},
                    {"level": "Senior Level", "title": "Senior Systems Engineer"},
                    {"level": "Lead / Manager", "title": "Backend Lead / Tech Director"}
                ],
                "learning_resources": [
                    {"title": "Python Official Documentation & Tutorial", "url": "https://docs.python.org/3/tutorial/", "type": "Official Documentation"},
                    {"title": "Node.js Developer Guides", "url": "https://nodejs.org/en/docs/guides/", "type": "Documentation"}
                ]
            },
            {
                "name": "Python Developer",
                "category": "Software",
                "description": "Develop scalable Python web backends, automation scripts, data pipelines, and specialized application software.",
                "required_education": ["B.Sc Computer Science", "B.Sc Data Science", "B.Tech IT"],
                "required_skills": ["Python", "SQL", "REST APIs", "Git", "Data Analysis"],
                "soft_skills": ["Problem Solving", "Adaptability", "Communication"],
                "interests": ["Software Development", "Data Science", "AI / ML"],
                "work_environment": ["Remote", "Hybrid", "MNC", "Startup"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Junior Python Developer"},
                    {"level": "Mid Level", "title": "Python Specialist"},
                    {"level": "Senior Level", "title": "Senior Python Engineer"},
                    {"level": "Lead / Manager", "title": "Python Technical Lead"}
                ],
                "learning_resources": [
                    {"title": "Python 3 Official Docs", "url": "https://docs.python.org/3/", "type": "Official Documentation"},
                    {"title": "Real Python Tutorials & Free Guides", "url": "https://realpython.com/", "type": "Tutorials"}
                ]
            },
            {
                "name": "Software Engineer",
                "category": "Software",
                "description": "Apply core computer science principles and algorithmic problem solving to design, test, build, and maintain large-scale software systems.",
                "required_education": ["B.Sc Computer Science", "B.Tech Computer Science", "B.E Software Engineering"],
                "required_skills": ["C++", "Java", "Python", "SQL", "Git", "REST APIs"],
                "soft_skills": ["Problem Solving", "Critical Thinking", "Teamwork", "Leadership"],
                "interests": ["Software Development", "Research"],
                "work_environment": ["Office", "Hybrid", "MNC", "Research"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Associate Software Engineer"},
                    {"level": "Mid Level", "title": "Software Engineer"},
                    {"level": "Senior Level", "title": "Senior Software Engineer"},
                    {"level": "Lead / Manager", "title": "Engineering Manager / VP Engineering"}
                ],
                "learning_resources": [
                    {"title": "GeeksforGeeks Data Structures & Algorithms", "url": "https://www.geeksforgeeks.org/", "type": "Free Reference"},
                    {"title": "MIT OpenCourseWare Computer Science", "url": "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/", "type": "Open University Course"}
                ]
            },
            {
                "name": "Data Analyst",
                "category": "Data",
                "description": "Transform complex quantitative datasets into actionable business insights, dashboards, and strategic recommendations.",
                "required_education": ["B.Sc Mathematics", "B.Sc Statistics", "B.Sc Computer Science", "B.Com Analytics"],
                "required_skills": ["SQL", "Data Analysis", "Python", "Tableau", "Power BI", "Statistics"],
                "soft_skills": ["Communication", "Critical Thinking", "Time Management"],
                "interests": ["Data Science", "Business", "Finance"],
                "work_environment": ["Hybrid", "Office", "Remote", "MNC", "Startup"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Junior Data Analyst"},
                    {"level": "Mid Level", "title": "Data Analyst"},
                    {"level": "Senior Level", "title": "Senior Business Data Analyst"},
                    {"level": "Lead / Manager", "title": "Analytics Lead / Head of Data"}
                ],
                "learning_resources": [
                    {"title": "Kaggle Learn Data Analysis Tutorials", "url": "https://www.kaggle.com/learn", "type": "Interactive Tutorials"},
                    {"title": "Microsoft Learn Data Analysis with Power BI", "url": "https://learn.microsoft.com/", "type": "Official Learning Paths"}
                ]
            },
            {
                "name": "Data Scientist",
                "category": "Data",
                "description": "Construct predictive models, machine learning algorithms, and deep statistical frameworks to extract value from structured and unstructured data.",
                "required_education": ["B.Sc Data Science", "M.Sc Statistics", "B.Tech Computer Science"],
                "required_skills": ["Python", "Statistics", "Machine Learning", "SQL", "Data Analysis"],
                "soft_skills": ["Problem Solving", "Critical Thinking", "Public Speaking"],
                "interests": ["Data Science", "AI / ML", "Research"],
                "work_environment": ["Remote", "Hybrid", "Research", "MNC"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Associate Data Scientist"},
                    {"level": "Mid Level", "title": "Data Scientist"},
                    {"level": "Senior Level", "title": "Senior Data Scientist"},
                    {"level": "Lead / Manager", "title": "Principal Data Scientist / Director of AI"}
                ],
                "learning_resources": [
                    {"title": "Scikit-Learn Official User Guide", "url": "https://scikit-learn.org/stable/user_guide.html", "type": "Documentation"},
                    {"title": "Kaggle Machine Learning Courses", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "type": "Interactive Course"}
                ]
            },
            {
                "name": "Machine Learning Engineer",
                "category": "AI & ML",
                "description": "Engineer, deploy, optimize, and maintain machine learning pipelines and artificial intelligence models in production environments.",
                "required_education": ["B.Sc Computer Science", "B.Tech AI & ML", "M.Sc Computer Science"],
                "required_skills": ["Python", "Machine Learning", "Deep Learning", "SQL", "Docker", "Git"],
                "soft_skills": ["Problem Solving", "Critical Thinking", "Adaptability"],
                "interests": ["AI / ML", "Data Science", "Research"],
                "work_environment": ["Remote", "Hybrid", "Startup", "MNC"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Junior ML Engineer"},
                    {"level": "Mid Level", "title": "Machine Learning Engineer"},
                    {"level": "Senior Level", "title": "Senior ML Infrastructure Engineer"},
                    {"level": "Lead / Manager", "title": "Head of Machine Learning"}
                ],
                "learning_resources": [
                    {"title": "Google Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "type": "Free Course"},
                    {"title": "PyTorch Official Tutorials", "url": "https://pytorch.org/tutorials/", "type": "Documentation"}
                ]
            },
            {
                "name": "AI Engineer",
                "category": "AI & ML",
                "description": "Architect artificial intelligence applications, integrate generative models, modern NLP systems, and intelligent multi-agent frameworks.",
                "required_education": ["B.Sc AI", "B.Tech Computer Science", "M.Sc Data Science"],
                "required_skills": ["Python", "Deep Learning", "Machine Learning", "REST APIs", "Git"],
                "soft_skills": ["Creativity", "Problem Solving", "Adaptability"],
                "interests": ["AI / ML", "Software Development", "Research"],
                "work_environment": ["Remote", "Hybrid", "Startup", "Research"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Junior AI Specialist"},
                    {"level": "Mid Level", "title": "AI Engineer"},
                    {"level": "Senior Level", "title": "Senior AI Systems Engineer"},
                    {"level": "Lead / Manager", "title": "Chief AI Architect"}
                ],
                "learning_resources": [
                    {"title": "Hugging Face Deep Learning Course", "url": "https://huggingface.co/course/chapter1/1", "type": "Free Interactive Course"},
                    {"title": "Fast.ai Practical Deep Learning for Coders", "url": "https://course.fast.ai/", "type": "Free Open Course"}
                ]
            },
            {
                "name": "Cybersecurity Analyst",
                "category": "Cybersecurity",
                "description": "Protect organizational networks, monitor threat intelligence, conduct vulnerability assessments, and respond to security incidents.",
                "required_education": ["B.Sc Cyber Security", "B.Sc Computer Science", "B.Tech IT"],
                "required_skills": ["Cyber Security", "Networking", "Python", "Git"],
                "soft_skills": ["Critical Thinking", "Problem Solving", "Communication", "Time Management"],
                "interests": ["Cybersecurity", "Networking", "Cloud Computing"],
                "work_environment": ["Office", "Hybrid", "Government", "MNC"],
                "career_growth": [
                    {"level": "Entry Level", "title": "SOC Analyst Tier 1"},
                    {"level": "Mid Level", "title": "Cybersecurity Engineer"},
                    {"level": "Senior Level", "title": "Senior Security Consultant"},
                    {"level": "Lead / Manager", "title": "Chief Information Security Officer (CISO)"}
                ],
                "learning_resources": [
                    {"title": "Cisco Networking Academy Cybersecurity Introduction", "url": "https://www.netacad.com/", "type": "Free Academy Course"},
                    {"title": "Cybrary Free Cybersecurity Fundamentals", "url": "https://www.cybrary.it/", "type": "Free Training"}
                ]
            },
            {
                "name": "Cloud Engineer",
                "category": "Cloud & Infrastructure",
                "description": "Deploy, configure, and maintain cloud infrastructure architectures across major platforms like AWS, Azure, and Google Cloud.",
                "required_education": ["B.Sc Computer Science", "B.Tech IT", "Diploma in Computer Hardware"],
                "required_skills": ["Cloud Computing", "Docker", "Kubernetes", "Networking", "Python", "Git"],
                "soft_skills": ["Problem Solving", "Adaptability", "Teamwork"],
                "interests": ["Cloud Computing", "Networking", "Software Development"],
                "work_environment": ["Remote", "Hybrid", "MNC", "Startup"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Associate Cloud Administrator"},
                    {"level": "Mid Level", "title": "Cloud Engineer"},
                    {"level": "Senior Level", "title": "Senior Cloud Solutions Engineer"},
                    {"level": "Lead / Manager", "title": "Principal Cloud Architect"}
                ],
                "learning_resources": [
                    {"title": "Microsoft Learn Azure Fundamentals", "url": "https://learn.microsoft.com/en-us/training/paths/az-900-describe-cloud-concepts/", "type": "Official Learning Path"},
                    {"title": "AWS Free Fundamentals Guides", "url": "https://aws.amazon.com/getting-started/", "type": "Official Guides"}
                ]
            },
            {
                "name": "DevOps Engineer",
                "category": "Cloud & Infrastructure",
                "description": "Bridge the gap between software development and IT operations by automating CI/CD deployment pipelines, containerization, and infrastructure as code.",
                "required_education": ["B.Sc Computer Science", "B.Tech IT"],
                "required_skills": ["Docker", "Kubernetes", "Git", "Python", "Cloud Computing", "Networking"],
                "soft_skills": ["Teamwork", "Problem Solving", "Communication", "Adaptability"],
                "interests": ["Cloud Computing", "Software Development"],
                "work_environment": ["Remote", "Hybrid", "MNC", "Startup"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Junior DevOps Engineer"},
                    {"level": "Mid Level", "title": "DevOps Specialist"},
                    {"level": "Senior Level", "title": "Senior SRE / DevOps Lead"},
                    {"level": "Lead / Manager", "title": "VP of Infrastructure Operations"}
                ],
                "learning_resources": [
                    {"title": "Kubernetes Official Documentation Tutorials", "url": "https://kubernetes.io/docs/tutorials/", "type": "Official Docs"},
                    {"title": "Docker Getting Started Guide", "url": "https://docs.docker.com/get-started/", "type": "Official Guide"}
                ]
            },
            {
                "name": "UI/UX Designer",
                "category": "Design & UI/UX",
                "description": "Craft intuitive user journeys, interactive wireframes, visual design systems, and seamless user experiences for modern applications.",
                "required_education": ["B.A Design", "B.Sc Computer Science", "B.Des Graphic Design"],
                "required_skills": ["Figma", "HTML", "CSS", "Creativity"],
                "soft_skills": ["Creativity", "Communication", "Adaptability", "Public Speaking"],
                "interests": ["UI/UX", "Software Development"],
                "work_environment": ["Remote", "Hybrid", "Startup", "Freelance"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Junior UI/UX Designer"},
                    {"level": "Mid Level", "title": "Product Designer"},
                    {"level": "Senior Level", "title": "Senior UX Researcher / Designer"},
                    {"level": "Lead / Manager", "title": "Head of Design / Creative Director"}
                ],
                "learning_resources": [
                    {"title": "Figma Official Learn & Tutorial Portal", "url": "https://help.figma.com/hc/en-us/categories/360002051613-Figma-design", "type": "Official Guides"},
                    {"title": "Interaction Design Foundation Free Articles", "url": "https://www.interaction-design.org/literature", "type": "Design Articles"}
                ]
            },
            {
                "name": "Database Administrator",
                "category": "Data",
                "description": "Manage database performance, ensure data integrity, implement robust backup strategies, and execute complex query optimizations.",
                "required_education": ["B.Sc Computer Science", "B.Tech IT"],
                "required_skills": ["SQL", "MongoDB", "Python", "Git"],
                "soft_skills": ["Critical Thinking", "Problem Solving", "Time Management"],
                "interests": ["Data Science", "Cloud Computing"],
                "work_environment": ["Office", "Hybrid", "MNC", "Government"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Junior Database Administrator"},
                    {"level": "Mid Level", "title": "Database Engineer"},
                    {"level": "Senior Level", "title": "Senior DBA Specialist"},
                    {"level": "Lead / Manager", "title": "Database Architecture Manager"}
                ],
                "learning_resources": [
                    {"title": "PostgreSQL Official Tutorial", "url": "https://www.postgresqltutorial.com/", "type": "Tutorials"},
                    {"title": "MongoDB University Free Fundamentals", "url": "https://learn.mongodb.com/", "type": "Free Courses"}
                ]
            },
            {
                "name": "Network Engineer",
                "category": "Networking",
                "description": "Design, configure, manage, and troubleshoot enterprise networking systems, routers, switches, firewalls, and WAN/LAN architectures.",
                "required_education": ["B.Sc Networking", "B.Tech IT", "Diploma in Computer Hardware"],
                "required_skills": ["Networking", "Cyber Security", "Cloud Computing"],
                "soft_skills": ["Problem Solving", "Communication", "Teamwork"],
                "interests": ["Networking", "Cybersecurity", "Cloud Computing"],
                "work_environment": ["Office", "Government", "MNC"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Network Support Specialist"},
                    {"level": "Mid Level", "title": "Network Engineer"},
                    {"level": "Senior Level", "title": "Senior Network Architect"},
                    {"level": "Lead / Manager", "title": "Director of Network Operations"}
                ],
                "learning_resources": [
                    {"title": "Cisco Networking Essentials", "url": "https://www.netacad.com/courses/networking/networking-essentials", "type": "Official Free Course"},
                    {"title": "NetworkChuck Networking Tutorials", "url": "https://www.youtube.com/@NetworkChuck", "type": "Video Tutorials"}
                ]
            },
            {
                "name": "Business Analyst",
                "category": "Business & Strategy",
                "description": "Evaluate organizational workflows, gather business requirements, and bridge the gap between IT solutions and enterprise goals.",
                "required_education": ["B.B.A", "B.Sc Computer Science", "M.B.A"],
                "required_skills": ["Data Analysis", "SQL", "Financial Modeling", "Technical Writing"],
                "soft_skills": ["Communication", "Leadership", "Negotiation", "Public Speaking"],
                "interests": ["Business", "Finance"],
                "work_environment": ["Office", "Hybrid", "MNC"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Associate Business Analyst"},
                    {"level": "Mid Level", "title": "Business Systems Analyst"},
                    {"level": "Senior Level", "title": "Senior Business Consultant"},
                    {"level": "Lead / Manager", "title": "Director of Business Strategy"}
                ],
                "learning_resources": [
                    {"title": "IIBA Free Business Analysis Resources", "url": "https://www.iiba.org/standards-and-resources/", "type": "Industry Standards"},
                    {"title": "Microsoft Learn Excel & Analytics", "url": "https://learn.microsoft.com/", "type": "Documentation"}
                ]
            },
            {
                "name": "Digital Marketing Specialist",
                "category": "Digital Marketing",
                "description": "Formulate data-driven online campaigns, optimize search engine visibility (SEO), run social media marketing, and track conversion analytics.",
                "required_education": ["B.A Communications", "B.B.A Marketing", "Diploma in Marketing"],
                "required_skills": ["Digital Marketing", "SEO", "Data Analysis"],
                "soft_skills": ["Creativity", "Communication", "Public Speaking", "Adaptability"],
                "interests": ["Marketing", "Business"],
                "work_environment": ["Remote", "Hybrid", "Startup", "Freelance"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Junior Digital Marketer"},
                    {"level": "Mid Level", "title": "Digital Marketing Specialist"},
                    {"level": "Senior Level", "title": "Growth Marketing Manager"},
                    {"level": "Lead / Manager", "title": "Chief Marketing Officer (CMO)"}
                ],
                "learning_resources": [
                    {"title": "Google Digital Garage Fundamentals of Digital Marketing", "url": "https://skillshop.exceedlms.com/student/catalog/browse", "type": "Free Certification"},
                    {"title": "HubSpot Academy Inbound Marketing", "url": "https://academy.hubspot.com/", "type": "Free Course"}
                ]
            },
            {
                "name": "Product Manager",
                "category": "Business & Strategy",
                "description": "Drive product vision, define roadmaps, align cross-functional tech & design teams, and manage key performance indicators for tech products.",
                "required_education": ["B.Sc Computer Science", "M.B.A", "B.Tech IT"],
                "required_skills": ["Data Analysis", "SQL", "Figma", "Technical Writing"],
                "soft_skills": ["Leadership", "Communication", "Negotiation", "Problem Solving", "Critical Thinking"],
                "interests": ["Business", "Software Development", "UI/UX"],
                "work_environment": ["Hybrid", "Office", "Startup", "MNC"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Associate Product Manager (APM)"},
                    {"level": "Mid Level", "title": "Product Manager"},
                    {"level": "Senior Level", "title": "Senior Product Manager"},
                    {"level": "Lead / Manager", "title": "VP of Product"}
                ],
                "learning_resources": [
                    {"title": "Product School Free PM Resources", "url": "https://productschool.com/free-resources", "type": "Free Guides"},
                    {"title": "Mixpanel Product Analytics Guide", "url": "https://mixpanel.com/blog/", "type": "Articles"}
                ]
            },
            {
                "name": "Technical Writer",
                "category": "Education & Research",
                "description": "Translate complex software code, API specifications, and architecture into clear documentation, user manuals, and developer guides.",
                "required_education": ["B.A English", "B.Sc Computer Science", "B.Tech IT"],
                "required_skills": ["Technical Writing", "Git", "HTML", "Markdown"],
                "soft_skills": ["Communication", "Critical Thinking", "Time Management"],
                "interests": ["Research", "Teaching", "Software Development"],
                "work_environment": ["Remote", "Hybrid", "MNC", "Freelance"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Junior Technical Writer"},
                    {"level": "Mid Level", "title": "Technical Content Specialist"},
                    {"level": "Senior Level", "title": "Senior Documentation Engineer"},
                    {"level": "Lead / Manager", "title": "Documentation Team Lead"}
                ],
                "learning_resources": [
                    {"title": "Google Technical Writing Course for Developers", "url": "https://developers.google.com/tech-writing", "type": "Free Course"},
                    {"title": "Write the Docs Community Guides", "url": "https://www.writethedocs.org/guide/", "type": "Community Docs"}
                ]
            },
            {
                "name": "Research Assistant",
                "category": "Education & Research",
                "description": "Conduct experimental academic research, analyze scientific literature, perform statistical computations, and assist in publication drafts.",
                "required_education": ["B.Sc Computer Science", "M.Sc Mathematics", "B.Tech Engineering"],
                "required_skills": ["Python", "Statistics", "Data Analysis", "Technical Writing"],
                "soft_skills": ["Critical Thinking", "Problem Solving", "Time Management"],
                "interests": ["Research", "Teaching", "AI / ML"],
                "work_environment": ["Research", "Office", "Government"],
                "career_growth": [
                    {"level": "Entry Level", "title": "Graduate Research Assistant"},
                    {"level": "Mid Level", "title": "Associate Researcher"},
                    {"level": "Senior Level", "title": "Senior Research Scientist"},
                    {"level": "Lead / Manager", "title": "Principal Investigator (PI)"}
                ],
                "learning_resources": [
                    {"title": "ArXiv Open Access Computer Science Papers", "url": "https://arxiv.org/list/cs/recent", "type": "Research Repository"},
                    {"title": "Google Scholar Learning Guides", "url": "https://scholar.google.com/", "type": "Academic Search"}
                ]
            }
        ]

        for item in careers_data:
            c = Career(
                name=item["name"],
                category=item["category"],
                description=item["description"],
                is_active=True
            )
            c.required_education = item["required_education"]
            c.required_skills = item["required_skills"]
            c.soft_skills = item["soft_skills"]
            c.interests = item["interests"]
            c.work_environment = item["work_environment"]
            c.career_growth = item["career_growth"]
            c.learning_resources = item["learning_resources"]
            db.session.add(c)

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
