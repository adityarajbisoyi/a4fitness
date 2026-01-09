import sqlite3
from datetime import datetime

DB_NAME = "fitness_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_name TEXT NOT NULL,
            reps INTEGER NOT NULL,
            calories REAL DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Simple migration: try to add column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE sessions ADD COLUMN calories REAL DEFAULT 0")
    except sqlite3.OperationalError:
        pass # Column likely exists

    # Create Settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    # Create Users table (Simple single user for now, expandable later)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT DEFAULT 'User',
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            total_reps INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            last_active DATE
        )
    ''')
    
    # Create Quests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE DEFAULT CURRENT_DATE,
            description TEXT,
            target INTEGER,
            current INTEGER DEFAULT 0,
            completed BOOLEAN DEFAULT 0,
            reward_xp INTEGER
        )
    ''')
    
    # Initialize default user if not exists
    cursor.execute('SELECT count(*) FROM users')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (name, xp, level, total_reps, streak, last_active) VALUES ('User', 0, 1, 0, 0, CURRENT_DATE)")

    conn.commit()
    conn.close()


XP_RATES = {
    "Pushups": 10,
    "Squats": 8,
    "Jumping Jacks": 5,
    "Bicep Curls": 8,
    "Lunges": 9,
    "Shoulder Press": 9,
    "Plank (Secs)": 2, 
    "High Knees": 5,
    "Crunches": 8
}

def save_session(exercise_name, reps, calories=0):
    if reps <= 0:
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sessions (exercise_name, reps, calories) VALUES (?, ?, ?)', (exercise_name, reps, calories))
    
    # --- Gamification Update ---
    # Calculate XP
    rate = XP_RATES.get(exercise_name, 5)
    xp_gain = int(reps * rate)
    
    # Update User Stats
    cursor.execute('SELECT xp, level, total_reps, streak, last_active FROM users WHERE id=1')
    row = cursor.fetchone()
    if row:
        current_xp, current_level, current_reps, current_streak, last_active = row
        new_xp = current_xp + xp_gain
        new_reps = current_reps + reps
        new_level = int(1 + (new_xp / 500))
        
        # Streak: Check if last_active is not today
        # For simplicity, we just increment if it's a new day
        # In a real app, we'd check if last_active == yesterday
        cursor.execute("SELECT date('now')")
        today = cursor.fetchone()[0]
        
        new_streak = current_streak
        if last_active != today:
             new_streak += 1
             
        cursor.execute('UPDATE users SET xp=?, level=?, total_reps=?, streak=?, last_active=CURRENT_DATE WHERE id=1', 
                       (new_xp, new_level, new_reps, new_streak))

    conn.commit()
    conn.close()
    
    # Check Quests
    update_quest_progress(exercise_name, reps)
    
    print(f"Saved session: {exercise_name} - {reps} reps - {calories:.2f} kcal - {xp_gain} XP")

def get_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT exercise_name, reps, calories, timestamp FROM sessions ORDER BY timestamp DESC LIMIT 20')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_daily_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Group by date
    cursor.execute('''
        SELECT date(timestamp), SUM(reps), SUM(calories) 
        FROM sessions 
        GROUP BY date(timestamp) 
        ORDER BY date(timestamp) ASC LIMIT 7
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_setting(key, default=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default

def set_setting(key, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, str(value)))
    conn.commit()
    conn.close()

def get_user_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT xp, level, total_reps, streak FROM users WHERE id=1')
    row = cursor.fetchone()
    conn.close()
    return row if row else (0, 1, 0, 0)

def update_user_stats(xp_gain, reps_gain):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get current stats
    cursor.execute('SELECT xp, level, total_reps, streak, last_active FROM users WHERE id=1')
    row = cursor.fetchone()
    if not row:
        return
    
    current_xp, current_level, current_reps, current_streak, last_active = row
    
    # Update logic
    new_xp = current_xp + xp_gain
    new_reps = current_reps + reps_gain
    
    # Simple Level Up Logic: Level = 1 + sqrt(XP / 100)
    # Or static thresholds: Level N requires N*100 XP
    new_level = int(1 + (new_xp / 500)) # Every 500 XP = 1 Level Up
    
    # Streak Logic (check if last_active was yesterday)
    # For now, just simple update
    
    cursor.execute('UPDATE users SET xp=?, level=?, total_reps=?, last_active=CURRENT_DATE WHERE id=1', (new_xp, new_level, new_reps))
    conn.commit()
    conn.close()

def get_active_quests():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, target, current, completed, reward_xp FROM quests WHERE date = CURRENT_DATE")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_quest(description, target, reward_xp):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO quests (description, target, reward_xp) VALUES (?, ?, ?)", (description, target, reward_xp))
    conn.commit()
    conn.close()

def update_quest_progress(exercise_name, reps_added):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Find active quests matching this exercise
    # Using simple string matching for now
    cursor.execute("SELECT id, description, target, current, completed, reward_xp FROM quests WHERE date = CURRENT_DATE AND completed = 0")
    active_quests = cursor.fetchall()
    
    completed_any = False
    
    for q in active_quests:
        qid, desc, target, current, completed, reward = q
        
        # Check if exercise matches quest description (e.g. "Do 20 Pushups" contains "Pushups")
        if exercise_name in desc:
            new_current = min(target, current + reps_added)
            new_completed = 1 if new_current >= target else 0
            
            cursor.execute("UPDATE quests SET current=?, completed=? WHERE id=?", (new_current, new_completed, qid))
            
            if new_completed and not completed:
                # Grant Bonus XP
                cursor.execute("UPDATE users SET xp = xp + ? WHERE id=1", (reward,))
                print(f"Quest Completed! +{reward} XP")
                completed_any = True
                
    conn.commit()
    conn.close()
    return completed_any

# Initialize DB on import
init_db()
