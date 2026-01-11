import customtkinter as ctk
import os
import sys
import threading
from tkinter import messagebox
import pyttsx3
import database
import gamification_module
import tutorial_module
import utility_modules
import voice_control_module
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import ai_coach_module
import face_emotion_module
import face_emotion_module
import auto_detect_module
import bluetooth_module

class FitnessApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Fitness Tracker")
        self.geometry("800x600")
        
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")


        self.navigation_frame.grid_rowconfigure(9, weight=1) # Push empty space to bottom, keeping buttons at top

        # Home Button
        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=45, border_spacing=15, 
                                        text="🏠  Home",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        anchor="w", font=ctk.CTkFont(size=15, weight="bold"),
                                        command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        # History Button
        self.history_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=45, border_spacing=15, 
                                        text="📜  History",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        anchor="w", font=ctk.CTkFont(size=15, weight="bold"),
                                        command=self.history_button_event)
        self.history_button.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        # Analytics Button
        self.analytics_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=45, border_spacing=15, 
                                        text="📊  Analytics",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        anchor="w", font=ctk.CTkFont(size=15, weight="bold"),
                                        command=self.analytics_button_event)
        self.analytics_button.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        # Settings Button
        self.settings_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=45, border_spacing=15, 
                                        text="⚙️  Settings",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        anchor="w", font=ctk.CTkFont(size=15, weight="bold"),
                                        command=self.settings_button_event)
        self.settings_button.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
        
        # Health Profile (Injury Modifiers)
        self.health_btn = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=45, border_spacing=15, 
                                        text="🩺  Health Profile",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        anchor="w", font=ctk.CTkFont(size=15, weight="bold"),
                                        command=self.open_health_profile)
        self.health_btn.grid(row=5, column=0, sticky="ew", padx=10, pady=5)

        # Achievements Button
        self.achievements_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=45, border_spacing=15, 
                                        text="🏆  Achievements",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        anchor="w", font=ctk.CTkFont(size=15, weight="bold"),
                                        command=self.achievements_button_event)
        self.achievements_button.grid(row=6, column=0, sticky="ew", padx=10, pady=5)
        
        # Tools Button
        self.tools_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=45, border_spacing=15, 
                                        text="🛠️  Tools",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        anchor="w", font=ctk.CTkFont(size=15, weight="bold"),
                                        command=self.tools_button_event)
        self.tools_button.grid(row=7, column=0, sticky="ew", padx=10, pady=5)

        # Bluetooth Button (Sidebar)
        self.ble_button = ctk.CTkButton(self.navigation_frame, corner_radius=10, height=45, border_spacing=15, 
                                        text="📡  Connect Device",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        anchor="w", font=ctk.CTkFont(size=15, weight="bold"),
                                        command=self.open_bluetooth_scanner)
        self.ble_button.grid(row=8, column=0, sticky="ew", padx=10, pady=5)

        # Voice Control Status Indicator
        self.voice_status_label = ctk.CTkLabel(
            self.navigation_frame, 
            text="🎙️ Voice: Initializing...",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.voice_status_label.grid(row=9, column=0, sticky="ew", padx=10, pady=10)

        self.navigation_frame.grid_rowconfigure(10, weight=1) # Spacer


        # Create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=1)
        self.home_frame.grid_rowconfigure(2, weight=1)

        # Background Image
        try:
            self.bg_img = ctk.CTkImage(light_image=Image.open("assets/background.png"),
                                  dark_image=Image.open("assets/background.png"),
                                  size=(800, 600))
            self.bg_label = ctk.CTkLabel(self.home_frame, text="", image=self.bg_img)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()
        except Exception as e:
            print(f"Error loading background: {e}")

        # Stats Bar
        # Stats Labels (Directly on home_frame)
        self.level_label = ctk.CTkLabel(self.home_frame, text="Level: 1", font=ctk.CTkFont(size=16, weight="bold"))
        self.level_label.grid(row=0, column=0, sticky="w", padx=40, pady=10)
        
        self.xp_label = ctk.CTkLabel(self.home_frame, text="XP: 0", font=ctk.CTkFont(size=14))
        self.xp_label.grid(row=0, column=0, columnspan=2, pady=10) # Centered
        
        self.streak_label = ctk.CTkLabel(self.home_frame, text="Streak: 0 🔥", font=ctk.CTkFont(size=14))
        self.streak_label.grid(row=0, column=1, sticky="e", padx=40, pady=10)

        self.welcome_label = ctk.CTkLabel(self.home_frame, text="Select an Exercise", font=ctk.CTkFont(size=24, weight="bold"))
        self.welcome_label.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        # Scrollable Container for exercises (to allow many aesthetic cards)
        self.scroll_frame = ctk.CTkScrollableFrame(self.home_frame, fg_color="transparent")
        self.scroll_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        self.scroll_frame.grid_columnconfigure(1, weight=1)

        # Helper to create exercise cards
        def create_card(row, col, title, icon, command, color="transparent"):
            # Check for Injury Restrictions
            current_injuries = database.get_setting("injuries", "")
            
            # Map injuries to disabled exercises (title keywords)
            restrictions = {
                "knee": ["Squats", "Lunges", "High Knees", "Jumping Jacks"],
                "shoulder": ["Pushups", "Shoulder Press", "Plank"],
                "back": ["Squats", "Crunches", "Plank", "Lunge"],
                "wrist": ["Pushups", "Plank"]
            }
            
            is_disabled = False
            reason = ""
            for injury in current_injuries.split(','):
                if injury in restrictions and title in restrictions[injury]:
                    is_disabled = True
                    reason = f"Avoid due to {injury} injury"
                    break
            
            if is_disabled:
                 card = ctk.CTkButton(self.scroll_frame, text=f"{icon}\n\n{title}\n⚠️ {reason}", 
                                 font=ctk.CTkFont(size=14, weight="bold"),
                                 width=200, height=120,
                                 corner_radius=15,
                                 fg_color="gray30", hover_color="gray30", state="disabled", # Disabled Look
                                 border_width=2, border_color="gray20")
            else:
                card = ctk.CTkButton(self.scroll_frame, text=f"{icon}\n\n{title}", 
                                     font=ctk.CTkFont(size=16, weight="bold"),
                                     width=200, height=120,
                                     corner_radius=15,
                                     fg_color=color, hover_color=("gray70", "gray30"),
                                     border_width=2, border_color="gray50",
                                     command=command)
                                     
            card.grid(row=row, column=col, padx=15, pady=15, sticky="ew")
            return card

        # Row 0
        create_card(0, 0, "Auto Detect", "🤖", self.start_auto_mode, color="#7C4DFF")
        create_card(0, 1, "Pushups", "💪", self.start_pushup, color="#E57373")

        # Row 1
        create_card(1, 0, "Shoulder Press", "🏋️", self.start_shoulder_press, color="#64B5F6")
        create_card(1, 1, "Squats", "🦵", self.start_squat, color="#81C784")
        
        # Row 2
        create_card(2, 0, "Jumping Jacks", "🏃", self.start_jumping_jack, color="#FFD54F")
        create_card(2, 1, "Plank", "🧘", self.start_plank, color="#BA68C8")
        
        # Row 3
        create_card(3, 0, "High Knees", "🦵", self.start_high_knees, color="#4DB6AC")
        create_card(3, 1, "Bicep Curls", "💪", self.start_bicep_curl, color="#FF8A65")

        # Row 4
        create_card(4, 0, "Crunches", "🍫", self.start_crunches, color="#8D6E63")
        create_card(4, 1, "Lunges", "🚶", self.start_lunge, color="#7986CB")

        # Create History Frame
        self.history_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.history_frame.grid_columnconfigure(0, weight=1)
        self.history_frame.grid_rowconfigure(1, weight=1)

        self.history_label = ctk.CTkLabel(self.history_frame, text="Session History", font=ctk.CTkFont(size=24, weight="bold"))
        self.history_label.grid(row=0, column=0, padx=20, pady=10)

        self.history_textbox = ctk.CTkTextbox(self.history_frame, width=600)
        self.history_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.refresh_btn = ctk.CTkButton(self.history_frame, text="Refresh", command=self.update_history)
        self.refresh_btn.grid(row=2, column=0, padx=20, pady=10)

        # Create Analytics Frame
        self.analytics_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.analytics_frame.grid_columnconfigure(0, weight=1)
        self.analytics_frame.grid_rowconfigure(1, weight=1)

        self.analytics_label = ctk.CTkLabel(self.analytics_frame, text="Analytics Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.analytics_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.analytics_graph_frame = ctk.CTkFrame(self.analytics_frame, fg_color="transparent")
        self.analytics_graph_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.refresh_analytics_btn = ctk.CTkButton(self.analytics_frame, text="Refresh Graphs", command=self.update_analytics)
        self.refresh_analytics_btn.grid(row=2, column=0, padx=20, pady=10)

        # Create Achievements Frame
        self.achievements_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.achievements_frame.grid_columnconfigure(0, weight=1)
        
        self.achievements_label = ctk.CTkLabel(self.achievements_frame, text="Your Achievements", font=ctk.CTkFont(size=24, weight="bold"))
        self.achievements_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.badges_frame = ctk.CTkScrollableFrame(self.achievements_frame, width=500, height=400)
        self.badges_frame.grid(row=1, column=0, padx=20, pady=10)
        
        self.refresh_achievements_btn = ctk.CTkButton(self.achievements_frame, text="Refresh Badges", command=self.update_achievements)
        self.refresh_achievements_btn.grid(row=2, column=0, padx=20, pady=10)

        # Create Tools Frame
        self.tools_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.tools_frame.grid_columnconfigure(0, weight=1)
        
        self.tools_label = ctk.CTkLabel(self.tools_frame, text="Utility Tools", font=ctk.CTkFont(size=24, weight="bold"))
        self.tools_label.pack(pady=20)
        
        self.utils_manager = utility_modules.UtilityManager(self)
        
        self.bmi_btn = ctk.CTkButton(self.tools_frame, text="BMI Calculator", command=self.utils_manager.show_bmi_calculator)
        self.bmi_btn.pack(pady=10)
        
        self.export_btn = ctk.CTkButton(self.tools_frame, text="Export PDF Report", command=self.utils_manager.export_report)
        self.export_btn.pack(pady=10)

        self.water_btn = ctk.CTkButton(self.tools_frame, text="Set Water Reminder", command=self.utils_manager.start_water_reminder)
        self.water_btn.pack(pady=10)

        self.rest_btn = ctk.CTkButton(self.tools_frame, text="Rest Timer", command=self.utils_manager.show_rest_timer)
        self.rest_btn.pack(pady=10)


        # Select default frame
        self.select_frame_by_name("home")
        
        self.running_exercise = False
        
        # Update stats initially
        gamification_module.refresh_daily_quests()
        self.update_user_stats_display()
        self.update_quest_display()

        # Voice Control
        self.voice_controller = voice_control_module.VoiceController(self.process_voice_command)
        try:
            self.voice_controller.start_listening()
            self.voice_status_label.configure(text="🎙️ Voice: Ready", text_color="green")
        except Exception as e:
            print(f"Voice Control unavailable: {e}")
            self.voice_status_label.configure(text="🎙️ Voice: Unavailable", text_color="red")

    def process_voice_command(self, command):
        print(f"App received command: {command}")
        
        # Helper to run on main thread
        def _execute():
            if command == "home": self.home_button_event()
            elif command == "history": self.history_button_event()
            elif command == "analytics": self.analytics_button_event()
            elif command == "tools": self.tools_button_event()
            elif command == "stop": 
                if self.running_exercise:
                    # Stopping is handled by checks in loops usually, but we can try to force it
                    # For now just print, stopping threads is hard without a flag
                    pass 
            
            # Exercises
            elif command == "pushups": self.start_pushup()
            elif command == "squats": self.start_squat()
            elif command == "jumping_jacks": self.start_jumping_jack()
            elif command == "bicep_curls": self.start_bicep_curl()
            elif command == "lunges": self.start_lunge()
            elif command == "shoulder_press": self.start_shoulder_press()
            elif command == "plank": self.start_plank()
            elif command == "high_knees": self.start_high_knees()
            elif command == "crunches": self.start_crunches()

        self.after(0, _execute)

    def home_button_event(self):
        self.select_frame_by_name("home")

    def history_button_event(self):
        self.select_frame_by_name("history")

    def analytics_button_event(self):
        self.select_frame_by_name("analytics")

    def achievements_button_event(self):
        self.select_frame_by_name("achievements")

    def tools_button_event(self):
        self.select_frame_by_name("tools")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.history_button.configure(fg_color=("gray75", "gray25") if name == "history" else "transparent")
        self.analytics_button.configure(fg_color=("gray75", "gray25") if name == "analytics" else "transparent")
        self.achievements_button.configure(fg_color=("gray75", "gray25") if name == "achievements" else "transparent")
        self.tools_button.configure(fg_color=("gray75", "gray25") if name == "tools" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
            self.history_frame.grid_forget()
            self.analytics_frame.grid_forget()
            self.achievements_frame.grid_forget()
            self.tools_frame.grid_forget()
        elif name == "history":
            self.home_frame.grid_forget()
            self.history_frame.grid(row=0, column=1, sticky="nsew")
            self.analytics_frame.grid_forget()
            self.achievements_frame.grid_forget()
            self.tools_frame.grid_forget()
            self.update_history()
        elif name == "analytics":
            self.home_frame.grid_forget()
            self.history_frame.grid_forget()
            self.analytics_frame.grid(row=0, column=1, sticky="nsew")
            self.achievements_frame.grid_forget()
            self.tools_frame.grid_forget()
            self.update_analytics()
        elif name == "achievements":
            self.home_frame.grid_forget()
            self.history_frame.grid_forget()
            self.analytics_frame.grid_forget()
            self.achievements_frame.grid(row=0, column=1, sticky="nsew")
            self.tools_frame.grid_forget()
            self.update_achievements()
        elif name == "tools":
            self.home_frame.grid_forget()
            self.history_frame.grid_forget()
            self.analytics_frame.grid_forget()
            self.achievements_frame.grid_forget()
            self.tools_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
            self.history_frame.grid_forget()
            self.analytics_frame.grid_forget()
            self.achievements_frame.grid_forget()
            self.tools_frame.grid_forget()

    def update_history(self):
        self.history_textbox.configure(state="normal")
        self.history_textbox.delete("0.0", "end")
        
        data = database.get_history()
        if not data:
            self.history_textbox.insert("0.0", "No history found.")
        else:
            header = f"{'Exercise':<20} | {'Reps':<10} | {'Time'}\n"
            header += "-"*60 + "\n"
            self.history_textbox.insert("end", header)
            for row in data:
                # row is (exercise, reps, timestamp)
                line = f"{row[0]:<20} | {row[1]:<10} | {row[2]}\n"
                self.history_textbox.insert("end", line)
        
        self.history_textbox.configure(state="disabled")

    def update_analytics(self):
        # Clear previous graph
        for widget in self.analytics_graph_frame.winfo_children():
            widget.destroy()

        data = database.get_daily_stats()
        if not data:
            no_data_label = ctk.CTkLabel(self.analytics_graph_frame, text="No enough data to generate analytics.")
            no_data_label.pack(pady=20)
            return
            
        # Extract data
        dates = [row[0] for row in data]
        reps = [row[1] for row in data]
        calories = [row[2] for row in data]
        
        # Create Figure
        fig, ax1 = plt.subplots(figsize=(6, 4))
        
        # Plot Reps
        color = 'tab:blue'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Total Reps', color=color)
        ax1.bar(dates, reps, color=color, alpha=0.6)
        ax1.tick_params(axis='y', labelcolor=color)
        
        # Plot Calories
        ax2 = ax1.twinx()  
        color = 'tab:red'
        ax2.set_ylabel('Calories (kcal)', color=color)  
        ax2.plot(dates, calories, color=color, marker='o')
        ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title("Daily Activity")
        fig.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.analytics_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

    def update_user_stats_display(self):
        xp, level, total_reps, streak = database.get_user_stats()
        self.level_label.configure(text=f"Level: {level}")
        self.xp_label.configure(text=f"XP: {xp}")
        self.streak_label.configure(text=f"Streak: {streak} 🔥")

    def update_quest_display(self):
        # Quests UI removed by user request
        pass

    def update_achievements(self):
        for widget in self.badges_frame.winfo_children():
            widget.destroy()
            
        xp, level, total_reps, streak = database.get_user_stats()
        badges = gamification_module.get_badges(total_reps)
        
        if not badges:
            ctk.CTkLabel(self.badges_frame, text="No achievements yet. Start working out!").pack(pady=20)
        
        for badge in badges:
            frame = ctk.CTkFrame(self.badges_frame)
            frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(frame, text=f"🏆 {badge['name']}", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=5)
            ctk.CTkLabel(frame, text=badge['desc'], font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(0, 5))

    def run_exercise_thread(self, target_func):
        if self.running_exercise:
            messagebox.showwarning("Warning", "An exercise is already running!")
            return
        
        self.running_exercise = True
        
        # Run in a separate thread to keep GUI responsive
        t = threading.Thread(target=self._wrapper, args=(target_func,))
        t.daemon = True
        t.start()

    def _wrapper(self, func):
        """Wrapper to run exercise functions with proper error handling"""
        try:
            func()
        except Exception as e:
            error_msg = str(e)
            print(f"Exercise Error: {error_msg}")
            
            # Show error to user on main thread
            def show_error():
                messagebox.showerror(
                    "Exercise Error", 
                    f"An error occurred:\n\n{error_msg}\n\nPlease check:\n"
                    "• Camera is connected\n"
                    "• No other app is using the camera\n"
                    "• All dependencies are installed"
                )
            
            self.after(0, show_error)
        finally:
            self.running_exercise = False
            # Schedule GUI update on main thread
            self.after(100, self.update_user_stats_display)

    def start_pushup(self):
        tutorial_module.show_tutorial(self, "Pushups")
        try:
            import main_module
            self.run_exercise_thread(main_module.run_pushup)
        except ImportError:
             messagebox.showerror("Error", "Pushup module not found.")

    def start_squat(self):
        tutorial_module.show_tutorial(self, "Squats")
        try:
            import squat_module
            self.run_exercise_thread(squat_module.run_squat)
        except ImportError:
             messagebox.showerror("Error", "Squat module not found.")

    def start_jumping_jack(self):
        tutorial_module.show_tutorial(self, "Jumping Jacks")
        try:
            import jumping_jack_module
            self.run_exercise_thread(jumping_jack_module.run_jumping_jack)
        except ImportError:
             messagebox.showerror("Error", "Jumping Jack module not found.")

    def start_bicep_curl(self):
        tutorial_module.show_tutorial(self, "Bicep Curls")
        try:
            import bicep_curl_module
            self.run_exercise_thread(bicep_curl_module.run_bicep_curl)
        except ImportError:
             messagebox.showerror("Error", "Bicep Curl module not found.")

    def start_lunge(self):
        tutorial_module.show_tutorial(self, "Lunges")
        try:
            import lunge_module
            self.run_exercise_thread(lunge_module.run_lunge)
        except ImportError:
             messagebox.showerror("Error", "Lunge module not found.")

    def start_shoulder_press(self):
        tutorial_module.show_tutorial(self, "Shoulder Press")
        try:
            import shoulder_press_module
            self.run_exercise_thread(shoulder_press_module.run_shoulder_press)
        except ImportError:
             messagebox.showerror("Error", "Shoulder Press module not found.")

    def start_plank(self):
        tutorial_module.show_tutorial(self, "Plank (Secs)")
        try:
            import plank_module
            self.run_exercise_thread(plank_module.run_plank)
        except ImportError:
             messagebox.showerror("Error", "Plank module not found.")

    def start_high_knees(self):
        tutorial_module.show_tutorial(self, "High Knees")
        try:
            import high_knees_module
            self.run_exercise_thread(high_knees_module.run_high_knees)
        except ImportError:
             messagebox.showerror("Error", "High Knees module not found.")

    def start_crunches(self):
        tutorial_module.show_tutorial(self, "Crunches")
        try:
            import crunches_module
            self.run_exercise_thread(crunches_module.run_crunches)
        except ImportError:
             messagebox.showerror("Error", "Crunches module not found.")

    def start_auto_mode(self):
        tutorial_module.show_tutorial(self, "Auto Detect Mode")
        try:
            import auto_detect_module
            self.run_exercise_thread(auto_detect_module.run_auto_mode)
        except ImportError:
             messagebox.showerror("Error", "Auto Detect module not found.")

    def settings_button_event(self):
        self.open_language_dialog()

    def check_language(self):
        if not database.get_setting("language"):
            self.open_language_dialog()

    def open_health_profile(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Health Profile / Injury Modifiers")
        dialog.geometry("400x400")
        dialog.attributes("-topmost", True)
        
        ctk.CTkLabel(dialog, text="Select Active Injuries", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        ctk.CTkLabel(dialog, text="The AI will disable harmful exercises.", font=ctk.CTkFont(size=12)).pack(pady=5)
        
        current_injuries = database.get_setting("injuries", "")
        
        vars = {
            "knee": ctk.BooleanVar(value="knee" in current_injuries),
            "shoulder": ctk.BooleanVar(value="shoulder" in current_injuries),
            "back": ctk.BooleanVar(value="back" in current_injuries),
            "wrist": ctk.BooleanVar(value="wrist" in current_injuries)
        }
        
        for injury, var in vars.items():
            ctk.CTkCheckBox(dialog, text=f"{injury.capitalize()} Injury", variable=var).pack(pady=10, anchor="w", padx=50)
            
        def save():
            selected = [k for k, v in vars.items() if v.get()]
            database.set_setting("injuries", ",".join(selected))
            messagebox.showinfo("Saved", "Health Profile Updated! Restart app to apply restrictions.")
            dialog.destroy()
            
        ctk.CTkButton(dialog, text="Save Profile", command=save, fg_color="green").pack(pady=20)

    def open_bluetooth_scanner(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Bluetooth Scanner")
        dialog.geometry("400x500")
        dialog.attributes("-topmost", True)
        
        status_lbl = ctk.CTkLabel(dialog, text="Scanning for devices...", font=ctk.CTkFont(size=14))
        status_lbl.pack(pady=10)
        
        device_list = ctk.CTkScrollableFrame(dialog, height=300)
        device_list.pack(fill="both", expand=True, padx=10, pady=10)
        
        def on_scan_results(devices):
            def _update_ui():
                status_lbl.configure(text=f"Found {len(devices)} devices.")
                for widget in device_list.winfo_children(): widget.destroy()
                
                if not devices:
                    ctk.CTkLabel(device_list, text="No fitness devices found.").pack(pady=10)
                    return

                for dev in devices:
                    name = dev.name or dev.address
                    rssi = getattr(dev, 'rssi', "N/A")
                    btn = ctk.CTkButton(device_list, text=f"{name} ({rssi} dBm)", 
                                        anchor="w",
                                        command=lambda d=dev: connect(d))
                    btn.pack(fill="x", pady=2)
            
            self.after(0, _update_ui)
        
        def connect(device):
            self.after(0, lambda: status_lbl.configure(text=f"Connecting to {device.name}..."))
            
            def success():
                def _succ():
                    messagebox.showinfo("Success", f"Connected to {device.name}!")
                    status_lbl.configure(text=f"Connected: {device.name}")
                    dialog.destroy()
                self.after(0, _succ)
                
            def fail(err):
                def _fail():
                    messagebox.showerror("Error", f"Failed: {err}")
                    status_lbl.configure(text="Connection Failed")
                self.after(0, _fail)
                
            bluetooth_module.bt_manager.connect_device(device.address, success, fail)

        # Start Scan
        bluetooth_module.bt_manager.start_scan(on_scan_results)

    def open_language_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Choose Language / भाषा चुनें")
        dialog.geometry("300x200")
        dialog.attributes("-topmost", True)
        
        label = ctk.CTkLabel(dialog, text="Select your preferred language", font=ctk.CTkFont(size=16))
        label.pack(pady=20)
        
        def set_lang(lang):
            database.set_setting("language", lang)
            dialog.destroy()
            
        btn_en = ctk.CTkButton(dialog, text="English", command=lambda: set_lang("en"))
        btn_en.pack(pady=10)
        
        btn_hi = ctk.CTkButton(dialog, text="Hindi (हिंदी)", command=lambda: set_lang("hi"))
        btn_hi.pack(pady=10)
        
        dialog.wait_window()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.quit()
            self.destroy()
            sys.exit()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = FitnessApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    # Check language after mainloop starts, doing it before might be odd with CTk
    app.after(100, app.check_language)
    app.mainloop()
