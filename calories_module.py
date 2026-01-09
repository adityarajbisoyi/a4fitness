# Calorie Estimation Module
# Estimates are approximate values per repetition or per second

MET_VALUES = {
    "Pushups": 0.5,       # kcal per rep
    "Squats": 0.6,        # kcal per rep
    "Jumping Jacks": 0.2, # kcal per jumping jack
    "Bicep Curls": 0.3,   # kcal per rep (per arm approx)
    "Lunges": 0.4,        # kcal per lunge
    "Shoulder Press": 0.4,# kcal per rep
    "Plank (Secs)": 0.1,  # kcal per second (approx)
    "High Knees": 0.3,    # kcal per step
    "Crunches": 0.25      # kcal per crunch
}

def calculate_calories(exercise_name, count):
    """
    Calculate total calories burnt based on exercise and count (reps or seconds).
    """
    burn_rate = MET_VALUES.get(exercise_name, 0)
    return float(count) * burn_rate
