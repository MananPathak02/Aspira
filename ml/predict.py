# ml/predict.py
import datetime

# Small sample college dataset — expand later
COLLEGES = [
    {"college": "IIT Delhi", "course": "B.Tech CSE", "required_percentage": 92, "rank_cutoff": 600},
    {"college": "IIT Bombay", "course": "B.Tech CSE", "required_percentage": 92, "rank_cutoff": 800},
    {"college": "NIT Trichy", "course": "B.Tech CSE", "required_percentage": 85, "rank_cutoff": 10000},
    {"college": "VIT Vellore", "course": "B.Tech CSE", "required_percentage": 75, "rank_cutoff": None},

    {"college": "St. X College", "course": "B.Com", "required_percentage": 70, "rank_cutoff": None},

    {"college": "AIIMS Delhi", "course": "MBBS", "required_percentage": 95, "rank_cutoff": 50},
    {"college": "State Medical College", "course": "MBBS", "required_percentage": 85, "rank_cutoff": 1000},

    {"college": "Top Design College", "course": "B.Des", "required_percentage": 75, "rank_cutoff": None},
    {"college": "Local University - BSc", "course": "B.Sc", "required_percentage": 60, "rank_cutoff": None}
]

# Roadmaps
ROADMAPS = {
    "B.Tech CSE": [
        "1st year: Strengthen programming fundamentals (C/Python), discrete math",
        "2nd year: Data Structures & Algorithms, OOP, mini projects",
        "3rd year: Internships, systems design, electives (AI/ML/Web)",
        "4th year: Major projects, placements / higher studies preparations"
    ],
    "MBBS": [
        "Complete MBBS curriculum and internships",
        "Choose specialization during residency",
        "Prepare for NEET-PG / post-grad exams",
        "Clinical practice / research"
    ],
    "B.Com": [
        "Learn accounting basics, Excel, and business fundamentals",
        "Internships in finance/accounts",
        "Optional: pursue CA/CMA/CS or MBA"
    ],
    "B.Des": [
        "Build design fundamentals and portfolio",
        "Learn Figma / Adobe tools",
        "Work on mini projects and internships"
    ],
    "B.Sc": [
        "Strengthen fundamentals in chosen subject",
        "Lab work + small projects",
        "Prepare for M.Sc or industry-focused certifications"
    ],
    "Default": [
        "Explore foundational courses",
        "Build early portfolio projects",
        "Take online certifications"
    ]
}

def normalize_text(s):
    return (s or "").strip().lower()

def infer_course(marks12, subjects_text, interests_text, exams):
    subj = normalize_text(subjects_text)
    interests = normalize_text(interests_text)
    exams_text = normalize_text(exams)

    if "neet" in exams_text:
        return "MBBS"
    if "jee" in exams_text:
        if any(k in interests for k in ["coding", "computer", "ai", "ml", "programming"]):
            return "B.Tech CSE"
        return "B.Tech"

    if any(k in interests for k in ["coding", "computer", "ai", "ml", "data"]):
        return "B.Tech CSE" if float(marks12 or 0) >= 60 else "B.Sc"

    if any(k in interests for k in ["business", "finance", "management"]):
        return "B.Com"

    if any(k in interests for k in ["design", "graphic", "ux", "ui"]):
        return "B.Des"

    if "pcm" in subj or "math" in subj:
        return "B.Tech CSE"

    if "pcb" in subj or "bio" in subj:
        return "MBBS" if float(marks12 or 0) >= 85 else "B.Sc"

    if "commerce" in subj:
        return "B.Com"

    return "B.Sc" if float(marks12 or 0) >= 60 else "Diploma"

def match_colleges(course, marks12, rank):
    marks = float(marks12 or 0)

    try:
        rk = int(rank) if rank not in ("", None, "null") else None
    except:
        rk = None

    matches = []
    for c in COLLEGES:
        if c["course"].lower() == course.lower():
            if marks >= c["required_percentage"]:
                cutoff = c.get("rank_cutoff")
                if cutoff is None or (rk is not None and rk <= cutoff):
                    matches.append(c)

    if not matches:
        for c in COLLEGES:
            if course.split()[0].lower() in c["course"].lower():
                matches.append(c)

    return matches[:5]

def generate_roadmap_for(course):
    return ROADMAPS.get(course, ROADMAPS["Default"])

# NEW → Tech skills, soft skills, careers, salaries, projects, companies, resources
EXTRA_DATA = {
    "B.Tech CSE": {
        "course_badge": "Engineering • CS",
        "course_description": "Computer Science Engineering focuses on algorithms, software, systems, and AI.",
        "technical_skills": ["Python", "DSA", "Databases", "Web Dev", "Machine Learning"],
        "soft_skills": ["Communication", "Teamwork", "Problem Solving"],
        "career_opportunities": ["Software Engineer", "Data Scientist", "Backend Engineer", "ML Engineer"],
        "salary_india": "6–22 LPA",
        "salary_global": "50k–200k USD",
        "projects": ["REST API project", "ML model", "Portfolio website", "Data pipeline"],
        "companies": ["Google", "Microsoft", "Amazon", "TCS", "Infosys"],
        "resources": ["Coursera – Python", "NPTEL – DSA", "YouTube – Web Dev Bootcamp"]
    },
    "MBBS": {
        "course_badge": "Medical",
        "course_description": "Bachelor of Medicine & Surgery prepares students for clinical practice.",
        "technical_skills": ["Anatomy", "Clinical Skills", "Biochemistry"],
        "soft_skills": ["Empathy", "Teamwork", "Observation"],
        "career_opportunities": ["Doctor", "Surgeon", "Clinical Researcher"],
        "salary_india": "4–18 LPA",
        "salary_global": "60k–250k USD",
        "projects": ["Case study", "Medical research summary"],
        "companies": ["AIIMS", "Apollo", "Fortis"],
        "resources": ["NPTEL Medical Basics", "YouTube – Anatomy lectures"]
    },
    "B.Com": {
        "course_badge": "Commerce",
        "course_description": "Commerce focuses on finance, accounting, and business fundamentals.",
        "technical_skills": ["Accounting", "Excel", "Finance Basics"],
        "soft_skills": ["Communication", "Analytical Thinking"],
        "career_opportunities": ["Accountant", "Investment Analyst"],
        "salary_india": "3–8 LPA",
        "salary_global": "40k–120k USD",
        "projects": ["Finance dashboard", "Business analysis project"],
        "companies": ["Deloitte", "EY", "KPMG"],
        "resources": ["Coursera – Finance", "YouTube – Accounting Basics"]
    },
    "B.Des": {
        "course_badge": "Design",
        "course_description": "Design program covering UI/UX, product design, and creative tools.",
        "technical_skills": ["Figma", "Adobe XD", "UI Design"],
        "soft_skills": ["Creativity", "Storytelling"],
        "career_opportunities": ["UI Designer", "UX Designer", "Product Designer"],
        "salary_india": "4–12 LPA",
        "salary_global": "50k–150k USD",
        "projects": ["App UI redesign", "Portfolio website"],
        "companies": ["Swiggy Design", "Zomato Design", "Adobe"],
        "resources": ["Figma Crash Course", "DesignLab"]
    },
    "B.Sc": {
        "course_badge": "Science",
        "course_description": "Science degree focusing on fundamental and applied sciences.",
        "technical_skills": ["Lab Skills", "Research", "Data Analysis"],
        "soft_skills": ["Critical Thinking"],
        "career_opportunities": ["Research Assistant", "Lab Technician"],
        "salary_india": "2–6 LPA",
        "salary_global": "30k–80k USD",
        "projects": ["Research project", "Lab analysis"],
        "companies": ["Research labs", "Universities"],
        "resources": ["NPTEL Science Basics"]
    }
}

def predict_profile(payload):
    marks12 = payload.get("marks12")
    subjects12 = payload.get("subjects12", "")
    interests = payload.get("interests", "")
    exams = payload.get("exams", "")
    rank = payload.get("rank")

    predicted_course = infer_course(marks12, subjects12, interests, exams)
    colleges = match_colleges(predicted_course, marks12, rank)
    roadmap = generate_roadmap_for(predicted_course)

    # load all extra data
    extras = EXTRA_DATA.get(predicted_course, EXTRA_DATA["B.Sc"])

    response = {
        "predicted_course": predicted_course,
        "recommended_colleges": colleges,
        "roadmap": roadmap,
        **extras,  # add salaries + skills + career + projects + resources
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z"
    }

    return response
