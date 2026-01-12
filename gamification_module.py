import database
import math
import random

QUEST_TEMPLATES = [
    ("Do {N} Pushups", "Pushups", 10, 50, 200), # Desc, Key, Min, Max, XP
    ("Do {N} Squats", "Squats", 10, 50, 150),
    ("Do {N} Jumping Jacks", "Jumping Jacks", 20, 100, 100),
    ("Do {N} Bicep Curls", "Bicep Curls", 10, 40, 120),
    ("Do {N} Lunges", "Lunges", 10, 30, 150),
    ("Do {N} Crunches", "Crunches", 10, 50, 100)
]

XP_RATES = {
    "Pushups": 10,
    "Squats": 8,
    "Jumping Jacks": 5,
    "Bicep Curls": 8,
    "Lunges": 9,
    "Shoulder Press": 9,
    "Plank (Secs)": 2, # per second
    "High Knees": 5,
    "Crunches": 8
}

BADGES = [
    {"name": "First Steps", "desc": "Do your first 10 reps", "condition": lambda reps: reps >= 10},
    {"name": "Century Club", "desc": "Reach 100 total reps", "condition": lambda reps: reps >= 100},
    {"name": "Spartan", "desc": "Reach 300 total reps", "condition": lambda reps: reps >= 300},
    {"name": "Master", "desc": "Reach 1000 total reps", "condition": lambda reps: reps >= 1000}
]

def calculate_xp(exercise_name, count):
    """ Calculate XP for a session """
    rate = XP_RATES.get(exercise_name, 5)
    return int(count * rate)

def check_level_up(old_level, new_level):
    if new_level > old_level:
        return True, new_level
    return False, old_level

def get_badges(total_reps):
    """ Return list of earned badge names """
    earned = []
    for badge in BADGES:
        if badge["condition"](total_reps):
            earned.append(badge)
    return earned

def refresh_daily_quests():
    """Generates 3 new quests if none exist for today"""
    current_quests = database.get_active_quests()
    if not current_quests:
        # Generate 3 random quests
        templates = random.sample(QUEST_TEMPLATES, 3)
        for tmpl in templates:
            desc_fmt, key, min_n, max_n, xp = tmpl
            target = random.randrange(min_n, max_n, 5) # Random target multiple of 5
            desc = desc_fmt.format(N=target)
            
            database.add_quest(desc, target, xp)
        return True
    return False

def refresh_daily_quests():
    """Generates 3 new quests if none exist for today"""
    current_quests = database.get_active_quests()
    if not current_quests:
        # Generate 3 random quests
        templates = random.sample(QUEST_TEMPLATES, 3)
        for tmpl in templates:
            desc_fmt, key, min_n, max_n, xp = tmpl
            target = random.randrange(min_n, max_n, 5) # Random target multiple of 5
            desc = desc_fmt.format(N=target)
            
            database.add_quest(desc, target, xp)
        return True
    return False
