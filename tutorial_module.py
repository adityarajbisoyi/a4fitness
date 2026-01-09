import customtkinter as ctk
import utils
import database

def show_tutorial(parent, exercise_name):
    """
    Shows a tutorial dialog if not seen before.
    Blocks execution until dialog is closed.
    """
    key = f"tutorial_{exercise_name}"
    if database.get_setting(key) == "seen":
        return

    dialog = ctk.CTkToplevel(parent)
    dialog.title(f"{exercise_name} Tutorial")
    dialog.geometry("400x350")
    dialog.resizable(False, False)
    
    # Bring to front
    dialog.attributes("-topmost", True)
    
    label = ctk.CTkLabel(dialog, text=f"Welcome to {exercise_name}!", font=ctk.CTkFont(size=20, weight="bold"))
    label.pack(pady=20)
    
    instructions = f"AI will track your reps for {exercise_name}.\n\nEnsure your full body is visible.\nFollow the voice commands."
    desc = ctk.CTkLabel(dialog, text=instructions, font=ctk.CTkFont(size=14))
    desc.pack(pady=20, padx=20)
    
    def close():
        database.set_setting(key, "seen")
        dialog.destroy()
        
    btn = ctk.CTkButton(dialog, text="Start Exercise", command=close)
    btn.pack(pady=20)
    
    # Speak welcome
    utils.speak("Welcome")
    
    dialog.wait_window()
