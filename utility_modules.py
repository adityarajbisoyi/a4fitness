import database
import customtkinter as ctk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from datetime import datetime
import threading
import time
import winsound

class UtilityManager:
    def __init__(self, parent_app):
        self.app = parent_app

    def show_bmi_calculator(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("BMI Calculator")
        dialog.geometry("300x350")
        dialog.attributes("-topmost", True)
        
        ctk.CTkLabel(dialog, text="Height (cm):").pack(pady=5)
        height_entry = ctk.CTkEntry(dialog)
        height_entry.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="Weight (kg):").pack(pady=5)
        weight_entry = ctk.CTkEntry(dialog)
        weight_entry.pack(pady=5)
        
        result_label = ctk.CTkLabel(dialog, text="", font=ctk.CTkFont(size=14, weight="bold"))
        result_label.pack(pady=20)
        
        def calculate():
            try:
                h = float(height_entry.get()) / 100
                w = float(weight_entry.get())
                bmi = w / (h*h)
                
                category = ""
                if bmi < 18.5: category = "Underweight"
                elif bmi < 24.9: category = "Normal"
                elif bmi < 29.9: category = "Overweight"
                else: category = "Obese"
                
                result_label.configure(text=f"BMI: {bmi:.1f}\n{category}")
                
            except ValueError:
                result_label.configure(text="Invalid Input")
        
        ctk.CTkButton(dialog, text="Calculate", command=calculate).pack(pady=10)

    def export_report(self):
        filename = f"Fitness_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
        c = canvas.Canvas(filename)
        c.drawString(100, 800, "Fitness AI Report")
        c.drawString(100, 780, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        
        xp, level, reps, streak = database.get_user_stats()
        c.drawString(100, 750, f"User Level: {level}")
        c.drawString(100, 730, f"Total XP: {xp}")
        c.drawString(100, 710, f"Total Reps: {reps}")
        c.drawString(100, 690, f"Current Streak: {streak} days")
        
        c.line(100, 670, 500, 670)
        c.drawString(100, 650, "Recent Sessions:")
        
        history = database.get_history()
        y = 630
        for row in history[:10]:
            exercise, r, cal, time = row
            c.drawString(100, y, f"{time}: {exercise} - {r} reps")
            y -= 20
            if y < 50:
                c.showPage()
                y = 800
                
        c.save()
        messagebox.showinfo("Export", f"Report saved as {filename}")

    def start_water_reminder(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Water Reminder")
        dialog.geometry("300x200")
        dialog.attributes("-topmost", True)
        
        ctk.CTkLabel(dialog, text="Remind me every (mins):").pack(pady=10)
        entry = ctk.CTkEntry(dialog)
        entry.insert(0, "30")
        entry.pack(pady=5)
        
        def start():
            try:
                mins = int(entry.get())
                self.app.after(mins * 60 * 1000, self._show_water_popup, mins)
                dialog.destroy()
                messagebox.showinfo("Started", f"Reminder set for every {mins} mins.")
            except ValueError:
                pass
                
        ctk.CTkButton(dialog, text="Start Trigger", command=start).pack(pady=10)

    def _show_water_popup(self, interval):
        winsound.Beep(1000, 500)
        messagebox.showinfo("Hydrate!", "Time to drink water! 💧")
        # Schedule next
        self.app.after(interval * 60 * 1000, self._show_water_popup, interval)

    def show_rest_timer(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Rest Timer")
        dialog.geometry("300x200")
        dialog.attributes("-topmost", True)
        
        ctk.CTkLabel(dialog, text="Rest Duration (secs):").pack(pady=10)
        entry = ctk.CTkEntry(dialog)
        entry.insert(0, "60")
        entry.pack(pady=5)
        
        lbl = ctk.CTkLabel(dialog, text="00:00", font=ctk.CTkFont(size=30, weight="bold"))
        lbl.pack(pady=10)
        
        def start_timer():
            try:
                secs = int(entry.get())
                for i in range(secs, -1, -1):
                    lbl.configure(text=f"{i//60:02d}:{i%60:02d}")
                    dialog.update()
                    time.sleep(1)
                winsound.Beep(1500, 1000)
                dialog.destroy()
            except ValueError:
                pass
        
        ctk.CTkButton(dialog, text="Start Rest", command=start_timer).pack(pady=5)
