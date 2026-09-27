def analyze_skill_gap(user, career):
    """
    Analyzes the skill gap between user's current skills and career's required skills.
    Returns:
    - skill_match_percentage (float 0-100)
    - acquired_skills (list of str)
    - missing_skills (list of str with priority ranking)
    - soft_skills_match (dict with possessed and missing)
    """
    user_skills_set = {
        s.skill.name.lower().strip() for s in user.skills if s.skill and s.skill.category == 'technical'
    }
    user_soft_set = {
        s.skill.name.lower().strip() for s in user.skills if s.skill and s.skill.category == 'soft'
    }

    req_tech = career.required_skills
    req_soft = career.soft_skills

    acquired_tech = []
    missing_tech = []

    for skill in req_tech:
        s_clean = skill.strip()
        if s_clean.lower() in user_skills_set:
            acquired_tech.append(s_clean)
        else:
            missing_tech.append(s_clean)

    if req_tech:
        skill_match_pct = round((len(acquired_tech) / len(req_tech)) * 100, 1)
    else:
        skill_match_pct = 100.0

    acquired_soft = []
    missing_soft = []
    for s in req_soft:
        s_clean = s.strip()
        if s_clean.lower() in user_soft_set:
            acquired_soft.append(s_clean)
        else:
            missing_soft.append(s_clean)

    # Priority ranking for missing technical skills
    priority_missing = []
    for idx, skill in enumerate(missing_tech, start=1):
        priority_missing.append({
            'rank': idx,
            'skill': skill,
            'importance': 'High' if idx <= 2 else ('Medium' if idx <= 4 else 'Normal'),
            'badge_color': 'danger' if idx <= 2 else ('warning' if idx <= 4 else 'secondary')
        })

    return {
        'skill_match_pct': skill_match_pct,
        'acquired_tech': acquired_tech,
        'missing_tech': missing_tech,
        'priority_missing': priority_missing,
        'acquired_soft': acquired_soft,
        'missing_soft': missing_soft,
        'total_required': len(req_tech)
    }
