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

# Default file paths
DATA_FILE = Path.home() / ".task_timer_data.json"
CONFIG_FILE = Path.home() / ".task_timer_config.json"
SOUND_FILE = Path(__file__).parent / "notification.wav"

# Default configuration
DEFAULT_CONFIG = {
    "default_duration": 25,
    "default_break": 5,
    "sound_enabled": True,
    "data_file": str(DATA_FILE),
    "sound_file": str(SOUND_FILE)
}

def load_config():
    """Load configuration from file or create with defaults"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with defaults to handle missing keys
                merged_config = DEFAULT_CONFIG.copy()
                merged_config.update(config)
                return merged_config
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not load config, using defaults{Style.RESET_ALL}")
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error saving config: {e}{Style.RESET_ALL}")
        return False

def init_config():
    """Initialize configuration file with defaults"""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        print(f"{Fore.GREEN}✓ Configuration file created at {CONFIG_FILE}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Configuration file already exists at {CONFIG_FILE}{Style.RESET_ALL}")

def show_config():
    """Display current configuration"""
    config = load_config()
    print(f"\n{Fore.BLUE}{Style.BRIGHT}⚙️  Current Configuration:{Style.RESET_ALL}")
    print(f"{Fore.BLUE}-" * 60 + Style.RESET_ALL)
    print(f"Default task duration: {Fore.CYAN}{config['default_duration']} minutes{Style.RESET_ALL}")
    print(f"Default break duration: {Fore.CYAN}{config['default_break']} minutes{Style.RESET_ALL}")
    print(f"Sound enabled: {Fore.CYAN}{config['sound_enabled']}{Style.RESET_ALL}")
    print(f"Data file: {Fore.CYAN}{config['data_file']}{Style.RESET_ALL}")
    print(f"Sound file: {Fore.CYAN}{config['sound_file']}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}-" * 60 + Style.RESET_ALL)
    print(f"\n{Fore.YELLOW}Config file location: {CONFIG_FILE}{Style.RESET_ALL}")

def update_config(key, value):
    """Update a configuration value"""
    config = load_config()
    
    # Validate and convert value based on key
    if key == "default_duration" or key == "default_break":
        try:
            value = int(value)
            if value <= 0:
                print(f"{Fore.RED}Error: Duration must be positive{Style.RESET_ALL}")
                return False
        except ValueError:
            print(f"{Fore.RED}Error: Duration must be a number{Style.RESET_ALL}")
            return False
    elif key == "sound_enabled":
        if value.lower() in ['true', '1', 'yes', 'on']:
            value = True
        elif value.lower() in ['false', '0', 'no', 'off']:
            value = False
        else:
            print(f"{Fore.RED}Error: sound_enabled must be true/false{Style.RESET_ALL}")
            return False
    elif key == "data_file" or key == "sound_file":
        # Expand ~ to home directory
        value = str(Path(value).expanduser())
    elif key not in DEFAULT_CONFIG:
        print(f"{Fore.RED}Error: Unknown configuration key '{key}'{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Valid keys: {', '.join(DEFAULT_CONFIG.keys())}{Style.RESET_ALL}")
        return False
    
    config[key] = value
    if save_config(config):
        print(f"{Fore.GREEN}✓ Configuration updated: {key} = {value}{Style.RESET_ALL}")
        return True
    return False

def reset_config():
    """Reset configuration to defaults"""
    if save_config(DEFAULT_CONFIG):
        print(f"{Fore.GREEN}✓ Configuration reset to defaults{Style.RESET_ALL}")
        return True
    return False

def load_tasks():
    """Load tasks from JSON file"""
    config = load_config()
    data_file = Path(config['data_file'])
    
    if data_file.exists():
        with open(data_file, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    config = load_config()
    data_file = Path(config['data_file'])
    
    with open(data_file, 'w') as f:
        json.dump(tasks, f, indent=2)

def play_notification_sound():
    """Play notification sound if available and enabled"""
    config = load_config()
    
    if not config['sound_enabled']:
        return
    
    if SOUND_AVAILABLE:
        sound_file = Path(config['sound_file'])
        if sound_file.exists():
            try:
                playsound(str(sound_file))
            except Exception as e:
                # Silently fail if sound playback fails
                pass

def add_task(name, duration=None, tags=None):
    """
    Add a new task
    
    Args:
        name: Task name
        duration: Task duration in minutes (uses config default if None)
        tags: List of tags for categorization
    """
    config = load_config()
    
    # Use default duration from config if not specified
    if duration is None:
        duration = config['default_duration']
    
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "name": name,
        "duration": duration,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "tags": tags if tags else []
    }
    tasks.append(task)
    save_tasks(tasks)
    
    tags_str = f" {Fore.MAGENTA}[{', '.join(tags)}]{Style.RESET_ALL}" if tags else ""
    print(f"{Fore.GREEN}✓ Task added: {Style.BRIGHT}{name}{Style.RESET_ALL}{tags_str} {Fore.CYAN}({duration} minutes){Style.RESET_ALL}")

def list_tasks(filter_tag=None):
    """
    List all tasks, optionally filtered by tag
    
    Args:
        filter_tag: Optional tag to filter tasks by
    """
    tasks = load_tasks()
    
    # Filter by tag if specified
    if filter_tag:
        tasks = [t for t in tasks if filter_tag.lower() in [tag.lower() for tag in t.get("tags", [])]]
        if not tasks:
            print(f"{Fore.YELLOW}No tasks found with tag '{filter_tag}'{Style.RESET_ALL}")
            return
    
    if not tasks:
        print(f"{Fore.YELLOW}No tasks found. Add one with 'add' command!{Style.RESET_ALL}")
        return
    
    # Header
    if filter_tag:
        print(f"\n{Fore.BLUE}{Style.BRIGHT}📋 Tasks filtered by '{filter_tag}':{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.BLUE}{Style.BRIGHT}📋 Your Tasks:{Style.RESET_ALL}")
    
    print(f"{Fore.BLUE}-" * 60 + Style.RESET_ALL)
    
    for task in tasks:
        if task["completed"]:
            status_color = Fore.GREEN
            status = "✓"
        else:
            status_color = Fore.YELLOW
            status = "○"
        
        # Format tags
        tags_display = ""
        if task.get("tags"):
            tags_formatted = [f"{Fore.MAGENTA}#{tag}{Style.RESET_ALL}" for tag in task["tags"]]
            tags_display = f" {' '.join(tags_formatted)}"
        
        print(f"{status_color}{status} [{task['id']}] {Style.BRIGHT}{task['name']}{Style.RESET_ALL} {Fore.CYAN}- {task['duration']}min{Style.RESET_ALL}{tags_display}")
    
    print(f"{Fore.BLUE}-" * 60 + Style.RESET_ALL)
    
    # Show tag summary if not filtering
    if not filter_tag:
        all_tags = {}
        for task in tasks:
            for tag in task.get("tags", []):
                all_tags[tag.lower()] = all_tags.get(tag.lower(), 0) + 1
        
        if all_tags:
            print(f"\n{Fore.CYAN}Available tags:{Style.RESET_ALL} ", end="")
            tag_items = [f"{Fore.MAGENTA}#{tag}{Style.RESET_ALL} ({count})" for tag, count in sorted(all_tags.items())]
            print(", ".join(tag_items))

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
        break_duration: Optional break duration in minutes (uses config default if True, None means no break)
        silent: Whether to disable sound notifications
    """
    config = load_config()
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        print(f"{Fore.RED}✗ Task {task_id} not found!{Style.RESET_ALL}")
        return
    
    # Show sound status at the start
    if not silent and config['sound_enabled'] and SOUND_AVAILABLE:
        sound_file = Path(config['sound_file'])
        if sound_file.exists():
            print(f"{Fore.CYAN}🔔 Sound notifications enabled{Style.RESET_ALL}")
    elif not silent and not config['sound_enabled']:
        print(f"{Fore.YELLOW}🔇 Sound notifications disabled in config{Style.RESET_ALL}")
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
            # Use config default if True, otherwise use specified duration
            if break_duration is True:
                break_duration = config['default_break']
            
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

def show_stats(filter_tag=None):
    """
    Show completion statistics, optionally filtered by tag
    
    Args:
        filter_tag: Optional tag to filter statistics by
    """
    tasks = load_tasks()
    
    # Filter by tag if specified
    if filter_tag:
        tasks = [t for t in tasks if filter_tag.lower() in [tag.lower() for tag in t.get("tags", [])]]
    
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    total_time = sum(t["duration"] for t in tasks if t["completed"])
    
    # Header
    if filter_tag:
        print(f"\n{Fore.BLUE}{Style.BRIGHT}📊 Statistics for '{filter_tag}':{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.BLUE}{Style.BRIGHT}📊 Your Statistics:{Style.RESET_ALL}")
    
    print(f"{Fore.BLUE}-" * 50 + Style.RESET_ALL)
    print(f"Total tasks: {Fore.CYAN}{Style.BRIGHT}{total}{Style.RESET_ALL}")
    print(f"Completed: {Fore.GREEN}{Style.BRIGHT}{completed}{Style.RESET_ALL}")
    print(f"Pending: {Fore.YELLOW}{Style.BRIGHT}{total - completed}{Style.RESET_ALL}")
    print(f"Total time spent: {Fore.MAGENTA}{Style.BRIGHT}{total_time} minutes{Style.RESET_ALL}")
    
    # Show breakdown by tag if not filtering
    if not filter_tag:
        all_tasks = load_tasks()  # Get all tasks again for tag breakdown
        tag_stats = {}
        
        for task in all_tasks:
            for tag in task.get("tags", []):
                tag_lower = tag.lower()
                if tag_lower not in tag_stats:
                    tag_stats[tag_lower] = {"total": 0, "completed": 0, "time": 0}
                
                tag_stats[tag_lower]["total"] += 1
                if task["completed"]:
                    tag_stats[tag_lower]["completed"] += 1
                    tag_stats[tag_lower]["time"] += task["duration"]
        
        if tag_stats:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}Breakdown by tag:{Style.RESET_ALL}")
            print(f"{Fore.BLUE}-" * 50 + Style.RESET_ALL)
            
            for tag, stats in sorted(tag_stats.items()):
                completion_rate = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0
                print(f"{Fore.MAGENTA}#{tag}{Style.RESET_ALL}: "
                      f"{Fore.CYAN}{stats['total']} tasks{Style.RESET_ALL}, "
                      f"{Fore.GREEN}{stats['completed']} completed{Style.RESET_ALL} "
                      f"({completion_rate:.0f}%), "
                      f"{Fore.YELLOW}{stats['time']}min{Style.RESET_ALL}")
    
    print(f"{Fore.BLUE}-" * 50 + Style.RESET_ALL)

def main():
    """Main CLI interface"""
    
    if len(sys.argv) < 2:
        config = load_config()
        print(f"{Fore.CYAN}{Style.BRIGHT}Task Timer CLI - Pomodoro Timer & Task Tracker{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Usage:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}python task_timer.py add <task_name> [duration_minutes] [--tag <tag1> <tag2> ...]{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}python task_timer.py list [--filter <tag>]{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}python task_timer.py start <task_id> [--break [<minutes>]] [--silent]{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}python task_timer.py delete <task_id>{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}python task_timer.py stats [--filter <tag>]{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}python task_timer.py config [show|set|reset|init]{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Examples:{Style.RESET_ALL}")
        print(f"  python task_timer.py add \"Team meeting\" 30 --tag work meetings")
        print(f"  python task_timer.py add \"Study Python\" --tag personal learning  # Uses default {config['default_duration']}min")
        print(f"  python task_timer.py list --filter work")
        print(f"  python task_timer.py start 1 --break  # Uses default {config['default_break']}min break")
        print(f"  python task_timer.py config show")
        print(f"  python task_timer.py config set default_duration 30")
        
        if not COLORS_AVAILABLE:
            print(f"\n💡 Tip: Install colorama for colorful output!")
            print(f"   pip install colorama")
        
        if not SOUND_AVAILABLE:
            print(f"\n💡 Tip: Install playsound for audio notifications!")
            print(f"   pip install playsound")
        
        return
    
    command = sys.argv[1]
    
    try:
        if command == "config":
            # Configuration commands
            if len(sys.argv) < 3:
                show_config()
            elif sys.argv[2] == "show":
                show_config()
            elif sys.argv[2] == "init":
                init_config()
            elif sys.argv[2] == "reset":
                reset_config()
            elif sys.argv[2] == "set":
                if len(sys.argv) < 5:
                    print(f"{Fore.RED}Error: Usage: config set <key> <value>{Style.RESET_ALL}")
                    return
                update_config(sys.argv[3], sys.argv[4])
            else:
                print(f"{Fore.RED}Error: Unknown config command '{sys.argv[2]}'{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Usage: config [show|set|reset|init]{Style.RESET_ALL}")
        
        elif command == "add":
            if len(sys.argv) < 3:
                print(f"{Fore.RED}Error: Task name required{Style.RESET_ALL}")
                return
            
            name = sys.argv[2]
            duration = None
            tags = []
            
            # Parse duration and tags
            i = 3
            while i < len(sys.argv):
                if sys.argv[i] == "--tag":
                    # Collect all tags after --tag flag
                    i += 1
                    while i < len(sys.argv) and not sys.argv[i].startswith("--"):
                        tags.append(sys.argv[i])
                        i += 1
                elif sys.argv[i].isdigit():
                    duration = int(sys.argv[i])
                    i += 1
                else:
                    i += 1
            
            add_task(name, duration, tags if tags else None)
        
        elif command == "list":
            filter_tag = None
            
            # Check for --filter flag
            if len(sys.argv) > 2 and sys.argv[2] == "--filter":
                if len(sys.argv) > 3:
                    filter_tag = sys.argv[3]
                else:
                    print(f"{Fore.RED}Error: Tag name required after --filter{Style.RESET_ALL}")
                    return
            
            list_tasks(filter_tag)
        
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
                        break_duration = True  # Use config default
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
            filter_tag = None
            
            # Check for --filter flag
            if len(sys.argv) > 2 and sys.argv[2] == "--filter":
                if len(sys.argv) > 3:
                    filter_tag = sys.argv[3]
                else:
                    print(f"{Fore.RED}Error: Tag name required after --filter{Style.RESET_ALL}")
                    return
            
            show_stats(filter_tag)
        
        else:
            print(f"{Fore.RED}Unknown command: {command}{Style.RESET_ALL}")
    
    except ValueError as e:
        print(f"{Fore.RED}Error: Invalid input - {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
