#!/usr/bin/env python3
"""
Task Timer CLI - A simple pomodoro timer and task tracker
"""

import time
import json
import os
from datetime import datetime
from pathlib import Path

DATA_FILE = Path.home() / ".task_timer_data.json"

def load_tasks():
    """Load tasks from JSON file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(name, duration=25):
    """Add a new task"""
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "name": name,
        "duration": duration,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✓ Task added: {name} ({duration} minutes)")

def list_tasks():
    """List all tasks"""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found. Add one with 'add' command!")
        return
    
    print("\n📋 Your Tasks:")
    print("-" * 50)
    for task in tasks:
        status = "✓" if task["completed"] else "○"
        print(f"{status} [{task['id']}] {task['name']} - {task['duration']}min")
    print("-" * 50)

def start_timer(task_id):
    """Start a timer for a specific task"""
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        print(f"Task {task_id} not found!")
        return
    
    duration = task["duration"] * 60  # Convert to seconds
    print(f"\n⏱️  Starting timer for: {task['name']}")
    print(f"Duration: {task['duration']} minutes\n")
    
    try:
        for remaining in range(duration, 0, -1):
            mins, secs = divmod(remaining, 60)
            print(f"\r⏰ {mins:02d}:{secs:02d} remaining", end='', flush=True)
            time.sleep(1)
        
        print("\n\n🎉 Time's up! Great work!")
        
        # Mark as completed
        task["completed"] = True
        task["completed_at"] = datetime.now().isoformat()
        save_tasks(tasks)
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Timer stopped.")

def delete_task(task_id):
    """Delete a task"""
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print(f"✓ Task {task_id} deleted")

def show_stats():
    """Show completion statistics"""
    tasks = load_tasks()
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    total_time = sum(t["duration"] for t in tasks if t["completed"])
    
    print("\n📊 Your Statistics:")
    print("-" * 50)
    print(f"Total tasks: {total}")
    print(f"Completed: {completed}")
    print(f"Pending: {total - completed}")
    print(f"Total time spent: {total_time} minutes")
    print("-" * 50)

def main():
    """Main CLI interface"""
    import sys
    
    if len(sys.argv) < 2:
        print("Task Timer CLI - Pomodoro Timer & Task Tracker")
        print("\nUsage:")
        print("  python task_timer.py add <task_name> [duration_minutes]")
        print("  python task_timer.py list")
        print("  python task_timer.py start <task_id>")
        print("  python task_timer.py delete <task_id>")
        print("  python task_timer.py stats")
        return
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Task name required")
            return
        name = sys.argv[2]
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 25
        add_task(name, duration)
    
    elif command == "list":
        list_tasks()
    
    elif command == "start":
        if len(sys.argv) < 3:
            print("Error: Task ID required")
            return
        task_id = int(sys.argv[2])
        start_timer(task_id)
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Task ID required")
            return
        task_id = int(sys.argv[2])
        delete_task(task_id)
    
    elif command == "stats":
        show_stats()
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
