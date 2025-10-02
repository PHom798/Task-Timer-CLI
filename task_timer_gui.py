#!/usr/bin/env python3
"""
Task Timer GUI - A simple pomodoro timer and task tracker
GUI version using tkinter.
"""

from logging import root
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
from task_timer import TaskManager, play_notification_sound, DEFAULT_BREAK_DURATION
import csv
from pathlib import Path

class TaskTimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Timer")
        self.geometry("600x400")

        self.task_manager = TaskManager()
        self.timer_id = None

        # --- UI Components ---
        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        # Frame for task list
        list_frame = ttk.Frame(self, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(list_frame, text="Tasks", font=("Helvetica", 14, "bold")).pack(anchor="w")

        self.task_listbox = tk.Listbox(list_frame, height=10, selectmode=tk.SINGLE)
        self.task_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.task_listbox.bind("<Double-1>", self.start_selected_task)

        # Frame for buttons
        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill=tk.X)

        self.add_button = ttk.Button(button_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.start_button = ttk.Button(button_frame, text="Start Selected", command=self.start_selected_task)
        self.start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_timer)
        self.pause_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected_task)
        self.delete_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.reset_button = ttk.Button(button_frame, text="Reset Timer", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.export_button = ttk.Button(button_frame, text="Export CSV", command=self.export_to_csv)
        self.export_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Frame for timer display
        timer_frame = ttk.Frame(self, padding="10")
        timer_frame.pack(fill=tk.X)

        self.timer_label = ttk.Label(timer_frame, text="Select a task to start", font=("Courier", 16))
        self.timer_label.pack()

        self.status_label = ttk.Label(timer_frame, text="", font=("Helvetica", 10))
        self.status_label.pack(pady=5)

        #paused
        global paused
        paused=0

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        self.task_manager.tasks = self.task_manager._load() # Reload tasks
        for task in self.task_manager.tasks:
            status = "✓" if task["completed"] else "○"
            self.task_listbox.insert(tk.END, f"{status} [{task['id']}] {task['name']} ({task['duration']} min)")

    def add_task(self):
        name = simpledialog.askstring("Add Task", "Enter task name:")
        if not name:
            return

        duration_str = simpledialog.askstring("Task Duration", "Enter duration in minutes (default 25):", initialvalue="25")
        try:
            duration = int(duration_str) if duration_str else 25
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid duration. Please enter a number.")
            return

        self.task_manager.add(name, duration)
        self.refresh_task_list()
        self.status_label.config(text=f"Added task: {name}")

    def get_selected_task_id(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a task from the list.")
            return None
        
        selected_text = self.task_listbox.get(selection[0])
        # Extracts ID from string like "○ [1] Task Name (25 min)"
        try:
            task_id = int(selected_text.split('[')[1].split(']')[0])
            return task_id
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Could not identify the selected task.")
            return None

    def start_selected_task(self, event=None):
        global task_id
        task_id= self.get_selected_task_id()
        if task_id is None:
            return
        try:
            if paused==1:
                return

        except:
            print("Error")
            return
        global task
        task = self.task_manager.get_task(task_id)
        if task['completed']:
            messagebox.showinfo("Task Completed", "This task has already been completed.")
            return

        self.run_timer(task['duration'], task['name'], task_id)


    def delete_selected_task(self):
        task_id = self.get_selected_task_id()
        if task_id is None:
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete task {task_id}?"):
            if self.task_manager.delete(task_id):
                self.refresh_task_list()
                self.status_label.config(text=f"Deleted task {task_id}")
            else:
                messagebox.showerror("Error", "Failed to delete the task.")

    def run_timer(self, duration_minutes, label, task_id=None, is_break=False):
        self.disable_buttons()
        self.status_label.config(text=f"Timer running for: {label}")
        
        


        
        end_time = time.time() + duration_minutes * 60 

        def update_display():
            global remaining
            remaining = end_time - time.time()
            if remaining > 0:
                mins, secs = divmod(int(remaining), 60)
                self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
                self.timer_id = self.after(1000, update_display)
            else:
                self.timer_label.config(text="00:00")
                play_notification_sound()
                self.enable_buttons()

                if not is_break and task_id:
                    self.task_manager.complete_task(task_id)
                    self.refresh_task_list()
                    messagebox.showinfo("Time's Up!", f"Great work on '{label}'!")
                    self.prompt_for_break(label)
                elif is_break:
                    messagebox.showinfo("Break Over", "Break time is over. Back to work!")
                    self.status_label.config(text="Break finished.")

        update_display()
    def pause_timer(self):
        global paused
        paused=0
        task = self.task_manager.get_task(task_id)


        if not task['completed']:
            if (paused==1):
                pass
            else:
                self.after_cancel(self.timer_id)
                self.status_label.config(text="Timer paused.")
                self.pause_button.config(text="Resume", command=self.resume_timer)
                self.pause_button.config(state=tk.NORMAL)
                paused=1
                self.enable_buttons()
    def resume_timer(self):
        paused=0

        self.run_timer(remaining/60, task['name'], task_id)
        self.pause_button.config(text="Pause", command=self.pause_timer)
        self.pause_button.config(state=tk.NORMAL)
    
    def reset_timer(self):
        
        global paused, remaining
        paused = 0
        remaining = 0
        
        if self.timer_id:
            self.after_cancel(self.timer_id)  # Stop any running countdown

        # Reset labels
        self.timer_label.config(text="00:00")
        self.status_label.config(text="Timer reset.")

        # Restore pause button state
        self.pause_button.config(text="Pause", command=self.pause_timer)

        # Re-enable all buttons
        self.enable_buttons()

    def export_to_csv(self):
        tasks = self.task_manager.tasks
        if not tasks:
            messagebox.showinfo("Export", "No tasks to export.")
            return

        csv_file = Path.cwd() / "task_timer_export.csv"
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["ID", "Name", "Duration (minutes)", "Completed", "Created At", "Completed At"])
                writer.writeheader()
                for task in tasks:
                    writer.writerow({
                        "ID": task.get("id"),
                        "Name": task.get("name"),
                        "Duration (minutes)": task.get("duration"),
                        "Completed": task.get("completed"),
                        "Created At": task.get("created_at"),
                        "Completed At": task.get("completed_at", "")
                    })
            messagebox.showinfo("Export", f"Tasks exported to {csv_file}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export tasks:\n{e}")

    def prompt_for_break(self, task_name):
        if messagebox.askyesno("Break Time?", f"Start a {DEFAULT_BREAK_DURATION}-minute break?"):
            self.run_timer(DEFAULT_BREAK_DURATION, f"Break after {task_name}", is_break=True)

    def disable_buttons(self):
        self.add_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)
        self.delete_button.config(state=tk.DISABLED)
        self.task_listbox.config(state=tk.DISABLED)
        


    def enable_buttons(self):
        self.add_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        self.delete_button.config(state=tk.NORMAL)
        self.task_listbox.config(state=tk.NORMAL)
        
        
        if (paused==1):
            # self.timer_label.config(text="Timer paused")
            pass
            
        else:


            self.timer_label.config(text="Select a task to start")

            self.status_label.config(text="Timer finished.")


if __name__ == "__main__":
    # Exit entire app on 'q' or 'Q'
    app = TaskTimerApp()
    app.mainloop()


# ideas for improvement
#must

# - Add keyboard shortcuts for buttons (e.g., Start, Pause, Reset)
# - there was a problem with sound soo
# - break duration option (i couldnt find a good place to add it in gui)

# good to have
# - better styling (i am bad at design)
# - add a progress bar for the timer


# - contact me on discord if u want to discuss about it : "ayowhatthef_"
