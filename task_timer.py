        #!/usr/bin/env python3
"""
Task Timer CLI - A simple pomodoro timer and task tracker
"""

import time
import json
import os
from datetime import datetime
from pathlib import Path
import sys

# Try to import colorama, fall back gracefully if not available
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Create dummy color constants if colorama is not available
    class Fore:
        GREEN = ''
        YELLOW = ''
        RED = ''
        CYAN = ''
        BLUE = ''
        MAGENTA = ''
    
    class Style:
        BRIGHT = ''
        RESET_ALL = ''

# Try to import playsound, fall back gracefully if not available
try:
    from playsound import playsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

DATA_FILE = Path.home() / ".task_timer_data.json"
DEFAULT_BREAK_DURATION = 5  # Default break duration in minutes
SOUND_FILE = Path(__file__).parent / "notification.wav"

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

def play_notification_sound():
    """Play notification sound if available"""
    if SOUND_AVAILABLE and SOUND_FILE.exists():
        try:
            playsound(str(SOUND_FILE))
        except Exception as e:
            # Silently fail if sound playback fails
            pass

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
    print(f"{Fore.GREEN}✓ Task added: {Style.BRIGHT}{name}{Style.RESET_ALL} {Fore.CYAN}({duration} minutes){Style.RESET_ALL}")

def list_tasks():
    """List all tasks"""
    tasks = load_tasks()
    if not tasks:
        print(f"{Fore.YELLOW}No tasks found. Add one with 'add' command!{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.BLUE}{Style.BRIGHT}📋 Your Tasks:{Style.RESET_ALL}")
    print(f"{Fore.BLUE}-" * 50 + Style.RESET_ALL)
    for task in tasks:
        if task["completed"]:
            status_color = Fore.GREEN
            status = "✓"
        else:
            status_color = Fore.YELLOW
            status = "○"
        
        print(f"{status_color}{status} [{task['id']}] {Style.BRIGHT}{task['name']}{Style.RESET_ALL} {Fore.CYAN}- {task['duration']}min{Style.RESET_ALL}")
    print(f"{Fore.BLUE}-" * 50 + Style.RESET_ALL)

def run_timer(duration_minutes, label, is_break=False, silent=False):
    """
    Run a timer for the specified duration
    
    Args:
        duration_minutes: Duration in minutes
        label: Label to display for the timer
        is_break: Whether this is a break timer (affects colors)
        silent: Whether to disable sound notification
    
    Returns:
        bool: True if timer completed, False if interrupted
    """
    duration = duration_minutes * 60  # Convert to seconds
    
    if is_break:
        print(f"\n{Fore.CYAN}☕ Starting break timer: {Style.BRIGHT}{label}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Duration: {duration_minutes} minutes{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Time to relax and recharge!{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.MAGENTA}⏱️  Starting timer for: {Style.BRIGHT}{label}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Duration: {duration_minutes} minutes{Style.RESET_ALL}\n")
    
    try:
        for remaining in range(duration, 0, -1):
            mins, secs = divmod(remaining, 60)
            
            # Color coding based on time remaining and timer type
            if is_break:
                # Break timer uses cyan/blue colors
                if remaining > duration * 0.5:
                    time_color = Fore.CYAN
                elif remaining > duration * 0.25:
                    time_color = Fore.BLUE
                else:
                    time_color = Fore.MAGENTA
            else:
                # Work timer uses green/yellow/red
                if remaining > duration * 0.5:
                    time_color = Fore.GREEN
                elif remaining > duration * 0.25:
                    time_color = Fore.YELLOW
                else:
                    time_color = Fore.RED
            
            timer_icon = "☕" if is_break else "⏰"
            print(f"\r{time_color}{timer_icon} {mins:02d}:{secs:02d} remaining{Style.RESET_ALL}", end='', flush=True)
            time.sleep(1)
        
        # Timer completed - play sound notification unless silent mode
        if not silent:
            play_notification_sound()
        
        if is_break:
            print(f"\n\n{Fore.GREEN}{Style.BRIGHT}✨ Break time is over! Ready to get back to work?{Style.RESET_ALL}")
        else:
            print(f"\n\n{Fore.GREEN}{Style.BRIGHT}🎉 Time's up! Great work!{Style.RESET_ALL}")
        
        return True
        
    except KeyboardInterrupt:
        if is_break:
            print(f"\n\n{Fore.YELLOW}⏸️  Break interrupted. Back to work early!{Style.RESET_ALL}")
        else:
            print(f"\n\n{Fore.YELLOW}⏸️  Timer stopped.{Style.RESET_ALL}")
        return False

def start_timer(task_id, break_duration=None, silent=False):
    """
    Start a timer for a specific task with optional break
    
    Args:
        task_id: ID of the task to start
        break_duration: Optional break duration in minutes (None means no break)
        silent: Whether to disable sound notifications
    """
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        print(f"{Fore.RED}✗ Task {task_id} not found!{Style.RESET_ALL}")
        return
    
    # Show sound status at the start
    if not silent and SOUND_AVAILABLE and SOUND_FILE.exists():
        print(f"{Fore.CYAN}🔔 Sound notifications enabled{Style.RESET_ALL}")
    elif not silent and not SOUND_AVAILABLE:
        print(f"{Fore.YELLOW}💡 Tip: Install playsound for audio notifications!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   pip install playsound{Style.RESET_ALL}")
    
    # Run the work timer
    completed = run_timer(task["duration"], task["name"], is_break=False, silent=silent)
    
    if completed:
        # Mark task as completed
        task["completed"] = True
        task["completed_at"] = datetime.now().isoformat()
        save_tasks(tasks)
        
        # Start break timer if requested
        if break_duration is not None:
            print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
            response = input(f"{Fore.YELLOW}Start {break_duration}-minute break? (Y/n): {Style.RESET_ALL}").strip().lower()
            
            if response != 'n':
                run_timer(break_duration, f"Break after {task['name']}", is_break=True, silent=silent)
                print(f"\n{Fore.GREEN}✓ Task and break completed!{Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}Break skipped. Keep up the momentum!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.BLUE}💡 Tip: Use --break to add a break timer after completing a task!{Style.RESET_ALL}")

def delete_task(task_id):
    """Delete a task"""
    tasks = load_tasks()
    task_exists = any(t["id"] == task_id for t in tasks)
    
    if not task_exists:
        print(f"{Fore.RED}✗ Task {task_id} not found!{Style.RESET_ALL}")
        return
    
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print(f"{Fore.GREEN}✓ Task {task_id} deleted{Style.RESET_ALL}")

def show_stats():
    """Show completion statistics"""
    tasks = load_tasks()
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    total_time = sum(t["duration"] for t in tasks if t["completed"])
    
    print(f"\n{Fore.BLUE}{Style.BRIGHT}📊 Your Statistics:{Style.RESET_ALL}")
    print(f"{Fore.BLUE}-" * 50 + Style.RESET_ALL)
    print(f"Total tasks: {Fore.CYAN}{Style.BRIGHT}{total}{Style.RESET_ALL}")
    print(f"Completed: {Fore.GREEN}{Style.BRIGHT}{completed}{Style.RESET_ALL}")
    print(f"Pending: {Fore.YELLOW}{Style.BRIGHT}{total - completed}{Style.RESET_ALL}")
    print(f"Total time spent: {Fore.MAGENTA}{Style.BRIGHT}{total_time} minutes{Style.RESET_ALL}")
    print(f"{Fore.BLUE}-" * 50 + Style.RESET_ALL)

def main():
    """Main CLI interface"""
    
    if len(sys.argv) < 2:
        print(f"{Fore.CYAN}{Style.BRIGHT}Task Timer CLI - Pomodoro Timer & Task Tracker{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Usage:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}python task_timer.py add <task_name> [duration_minutes]{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}python task_timer.py list{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}python task_timer.py start <task_id> [--break <minutes>] [--silent]{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}python task_timer.py delete <task_id>{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}python task_timer.py stats{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Examples:{Style.RESET_ALL}")
        print(f"  python task_timer.py start 1 --break 5")
        print(f"  python task_timer.py start 2 --break 10 --silent")
        print(f"  python task_timer.py start 3 --silent")
        
        if not COLORS_AVAILABLE:
            print(f"\n💡 Tip: Install colorama for colorful output!")
            print(f"   pip install colorama")
        
        if not SOUND_AVAILABLE:
            print(f"\n💡 Tip: Install playsound for audio notifications!")
            print(f"   pip install playsound")
        
        return
    
    command = sys.argv[1]
    
    try:
        if command == "add":
            if len(sys.argv) < 3:
                print(f"{Fore.RED}Error: Task name required{Style.RESET_ALL}")
                return
            name = sys.argv[2]
            duration = int(sys.argv[3]) if len(sys.argv) > 3 else 25
            add_task(name, duration)
        
        elif command == "list":
            list_tasks()
        
        elif command == "start":
            if len(sys.argv) < 3:
                print(f"{Fore.RED}Error: Task ID required{Style.RESET_ALL}")
                return
            
            task_id = int(sys.argv[2])
            
            # Parse flags
            break_duration = None
            silent = False
            
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == "--break":
                    if i + 1 < len(sys.argv) and sys.argv[i + 1].isdigit():
                        break_duration = int(sys.argv[i + 1])
                        i += 2
                    else:
                        break_duration = DEFAULT_BREAK_DURATION
                        i += 1
                elif sys.argv[i] == "--silent":
                    silent = True
                    i += 1
                else:
                    i += 1
            
            start_timer(task_id, break_duration, silent)
        
        elif command == "delete":
            if len(sys.argv) < 3:
                print(f"{Fore.RED}Error: Task ID required{Style.RESET_ALL}")
                return
            task_id = int(sys.argv[2])
            delete_task(task_id)
        
        elif command == "stats":
            show_stats()
        
        else:
            print(f"{Fore.RED}Unknown command: {command}{Style.RESET_ALL}")
    
    except ValueError as e:
        print(f"{Fore.RED}Error: Invalid input - {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
