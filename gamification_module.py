import database
import math

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
