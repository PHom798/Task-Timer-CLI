# Configuration Guide  

Task Timer CLI supports customizable configuration through a JSON file. This guide explains all available settings and how to use them.

## Table of Contents
- [Quick Start](#quick-start)
- [Configuration File](#configuration-file)
- [Available Settings](#available-settings)
- [Managing Configuration](#managing-configuration)
- [Use Cases](#use-cases)
- [Troubleshooting](#troubleshooting)
- [Advanced Tips](#advanced-tips)

## Quick Start

### View Current Configuration

```bash
python task_timer.py config
```

or

```bash
python task_timer.py config show
```

### Change a Setting

```bash
python task_timer.py config set default_duration 30
python task_timer.py config set sound_enabled false
```

### Reset to Defaults

```bash
python task_timer.py config reset
```

That's it! Your preferences are now saved and will be used for all future tasks.

## Configuration File

### Location

**Config file:** `~/.task_timer_config.json`

- **macOS/Linux:** `/Users/username/.task_timer_config.json`
- **Windows:** `C:\Users\username\.task_timer_config.json`

### Format

The configuration file is a simple JSON file:

```json
{
  "default_duration": 25,
  "default_break": 5,
  "sound_enabled": true,
  "data_file": "/Users/username/.task_timer_data.json",
  "sound_file": "/path/to/notification.wav"
}
```

You can edit this file directly with any text editor, or use the `config` command.

### Automatic Creation

The config file is created automatically:
- When you first run the app (uses defaults)
- When you run `python task_timer.py config init`
- When you change a setting with `config set`

## Available Settings

### 1. default_duration

**Type:** Integer (minutes)  
**Default:** 25  
**Description:** Default duration for new tasks when not specified

**Usage:**
```bash
# Set default to 30 minutes
python task_timer.py config set default_duration 30

# Now tasks without duration use 30min
python task_timer.py add "Task"  # Uses 30 minutes
```

**Valid values:** Any positive integer (1-999)

**Use case:** If you prefer 20-minute or 50-minute work sessions instead of the standard 25-minute Pomodoro.

---

### 2. default_break

**Type:** Integer (minutes)  
**Default:** 5  
**Description:** Default duration for break timers when not specified

**Usage:**
```bash
# Set default break to 10 minutes
python task_timer.py config set default_break 10

# Now --break without duration uses 10min
python task_timer.py start 1 --break  # Uses 10-minute break
```

**Valid values:** Any positive integer (1-60)

**Use case:** If you prefer longer or shorter breaks than the standard 5-minute Pomodoro break.

---

### 3. sound_enabled

**Type:** Boolean  
**Default:** true  
**Description:** Global enable/disable for sound notifications

**Usage:**
```bash
# Disable sound globally
python task_timer.py config set sound_enabled false

# Enable sound globally
python task_timer.py config set sound_enabled true
```

**Valid values:**
- `true`, `1`, `yes`, `on` → Enabled
- `false`, `0`, `no`, `off` → Disabled

**Use case:** 
- Disable during work hours in shared spaces
- Enable when working alone
- Prefer visual-only notifications

**Note:** The `--silent` flag overrides this setting for individual timers.

---

### 4. data_file

**Type:** String (file path)  
**Default:** `~/.task_timer_data.json`  
**Description:** Location where task data is stored

**Usage:**
```bash
# Move data to Documents folder
python task_timer.py config set data_file ~/Documents/tasks.json

# Move data to Dropbox for sync
python task_timer.py config set data_file ~/Dropbox/task_timer_data.json

# Custom location
python task_timer.py config set data_file /path/to/my_tasks.json
```

**Valid values:** Any valid file path. Supports `~` for home directory.

**Use case:**
- Sync tasks across devices (Dropbox, Google Drive, etc.)
- Organize data in specific folder
- Separate personal and work task data
- Backup location

---

### 5. sound_file

**Type:** String (file path)  
**Default:** `./notification.wav` (relative to app directory)  
**Description:** Path to the notification sound file

**Usage:**
```bash
# Use custom notification sound
python task_timer.py config set sound_file ~/sounds/my_bell.wav

# Use system sound (macOS)
python task_timer.py config set sound_file /System/Library/Sounds/Glass.aiff

# Relative path
python task_timer.py config set sound_file ./custom_sound.wav
```

**Valid values:** Any valid path to a WAV or compatible audio file.

**Use case:**
- Personalize notification sound
- Use different sounds for different contexts
- Use less intrusive notification sounds

---

## Managing Configuration

### View Configuration

```bash
# Show all settings
python task_timer.py config
python task_timer.py config show
```

Output:
```
⚙️  Current Configuration:
------------------------------------------------------------
Default task duration: 25 minutes
Default break duration: 5 minutes
Sound enabled: True
Data file: /Users/username/.task_timer_data.json
Sound file: /path/to/notification.wav
------------------------------------------------------------

Config file location: /Users/username/.task_timer_config.json
```

### Initialize Configuration

```bash
# Create config file with defaults
python task_timer.py config init
```

Use this if you've deleted your config file or want to start fresh.

### Update Settings

```bash
# General syntax
python task_timer.py config set <key> <value>

# Examples
python task_timer.py config set default_duration 30
python task_timer.py config set default_break 10
python task_timer.py config set sound_enabled false
python task_timer.py config set data_file ~/Documents/tasks.json
```

### Reset to Defaults

```bash
# Reset all settings to defaults
python task_timer.py config reset
```

This restores:
- `default_duration`: 25
- `default_break`: 5
- `sound_enabled`: true
- `data_file`: `~/.task_timer_data.json`
- `sound_file`: `./notification.wav`

### Manual Editing

You can also edit the config file directly:

```bash
# Open in your favorite editor
nano ~/.task_timer_config.json
vim ~/.task_timer_config.json
code ~/.task_timer_config.json
```

Just make sure it's valid JSON!

## Use Cases

### Case 1: Quick Pomodoros (20min)

You prefer shorter, more frequent work sessions:

```bash
python task_timer.py config set default_duration 20
python task_timer.py config set default_break 3
```

Now:
```bash
python task_timer.py add "Task"  # 20 minutes
python task_timer.py start 1 --break  # 3-minute break
```

### Case 2: Deep Work Sessions (90min)

You need longer focus periods:

```bash
python task_timer.py config set default_duration 90
python task_timer.py config set default_break 20
```

Now:
```bash
python task_timer.py add "Deep work"  # 90 minutes
python task_timer.py start 1 --break  # 20-minute break
```

### Case 3: Silent Mode

Working in a library or shared office:

```bash
python task_timer.py config set sound_enabled false
```

All timers are now silent by default. Use `--silent` flag unnecessary!

### Case 4: Cloud Sync

Sync tasks across multiple computers:

```bash
# On all machines:
python task_timer.py config set data_file ~/Dropbox/task_timer_data.json
```

Your tasks are now synced via Dropbox!

### Case 5: Work/Personal Separation

Separate work and personal tasks:

**Work hours:**
```bash
python task_timer.py config set data_file ~/work_tasks.json
python task_timer.py config set default_duration 50
```

**Personal hours:**
```bash
python task_timer.py config set data_file ~/personal_tasks.json
python task_timer.py config set default_duration 25
```

Or create shell aliases:
```bash
alias work-timer='python task_timer.py --config ~/work_config.json'
alias personal-timer='python task_timer.py --config ~/personal_config.json'
```

### Case 6: Different Workflows

**Morning (focused work):**
```bash
python task_timer.py config set default_duration 50
python task_timer.py config set default_break 10
python task_timer.py config set sound_enabled true
```

**Afternoon (meetings & admin):**
```bash
python task_timer.py config set default_duration 30
python task_timer.py config set default_break 5
python task_timer.py config set sound_enabled false
```

## Troubleshooting

### Config Not Loading

**Problem:** Changes don't seem to take effect

**Solution:**
```bash
# Verify config was saved
python task_timer.py config show

# Check file exists
ls -la ~/.task_timer_config.json

# Re-initialize if needed
python task_timer.py config reset
```

### Invalid Configuration

**Problem:** "Could not load config" warning

**Solution:**
```bash
# Reset to defaults
python task_timer.py config reset

# Or manually fix JSON
nano ~/.task_timer_config.json
# Ensure valid JSON format
```

### Permission Issues

**Problem:** "Error saving config: Permission denied"

**Solution:**
```bash
# Check file permissions
ls -la ~/.task_timer_config.json

# Fix permissions
chmod 644 ~/.task_timer_config.json

# Or delete and recreate
rm ~/.task_timer_config.json
python task_timer.py config init
```

### Sound Not Working

**Problem:** Sound enabled but not playing

**Check:**
1. Is `sound_enabled` set to `true`?
   ```bash
   python task_timer.py config show
   ```

2. Is playsound installed?
   ```bash
   pip show playsound
   ```

3. Does sound file exist?
   ```bash
   python task_timer.py config show  # Check sound_file path
   ls -la /path/to/sound/file
   ```

4. Test manually:
   ```bash
   python -c "from playsound import playsound; playsound('notification.wav')"
   ```

### Data File Not Found

**Problem:** Tasks not loading

**Solution:**
```bash
# Check data file location
python task_timer.py config show

# Verify file exists
ls -la ~/.task_timer_data.json

# Reset to default location
python task_timer.py config set data_file ~/.task_timer_data.json
```

## Advanced Tips

### Backup Configuration

```bash
# Backup config
cp ~/.task_timer_config.json ~/.task_timer_config.backup

# Backup data too
cp ~/.task_timer_data.json ~/.task_timer_data.backup
```

### Share Configuration

```bash
# Export for sharing
cat ~/.task_timer_config.json > my_config.json

# Import on another machine
cp my_config.json ~/.task_timer_config.json
```

### Version Control

Add config to git (optional):

```bash
cd ~
git init
git add .task_timer_config.json
git commit -m "My task timer config"
```

### Multiple Profiles

Create different config files:

```bash
# Save different profiles
cp ~/.task_timer_config.json ~/configs/work_config.json
cp ~/.task_timer_config.json ~/configs/personal_config.json

# Switch profiles
cp ~/configs/work_config.json ~/.task_timer_config.json
```

### Environment-Specific Defaults

Use different defaults on different machines:

**Laptop (on-the-go, shorter sessions):**
```json
{
  "default_duration": 20,
  "default_break": 3,
  "sound_enabled": false
}
```

**Desktop (focused work, longer sessions):**
```json
{
  "default_duration": 50,
  "default_break": 15,
  "sound_enabled": true
}
```

### Scripted Configuration

Automate config changes:

```bash
#!/bin/bash
# setup_work_mode.sh

python task_timer.py config set default_duration 50
python task_timer.py config set default_break 10
python task_timer.py config set sound_enabled false
python task_timer.py config set data_file ~/work_tasks.json

echo "Work mode activated!"
```

```bash
chmod +x setup_work_mode.sh
./setup_work_mode.sh
```

## Configuration Best Practices

### 1. Start with Defaults

Don't change everything at once. Try the defaults first, then adjust.

### 2. Experiment

Try different durations to find your optimal work/break rhythm:
- 25/5 (classic Pomodoro)
- 50/10 (extended focus)
- 90/20 (deep work)
- 20/3 (quick sprints)

### 3. Context Matters

Different tasks need different durations:
- Creative work: longer sessions (50min)
- Administrative tasks: shorter sessions (25min)
- Learning: medium sessions (30-40min)

### 4. Backup Regularly

```bash
# Weekly backup
cp ~/.task_timer_config.json ~/backups/config_$(date +%Y%m%d).json
```

### 5. Document Your Changes

Add comments to your backup:
```json
// backup_notes.txt
// 2024-10-03: Changed to 30min sessions for better focus
// 2024-10-10: Disabled sound for library work
```

## Configuration Values Reference

| Setting | Type | Default | Min | Max | Example |
|---------|------|---------|-----|-----|---------|
| default_duration | int | 25 | 1 | 999 | 30 |
| default_break | int | 5 | 1 | 60 | 10 |
| sound_enabled | bool | true | - | - | false |
| data_file | string | ~/.task_timer_data.json | - | - | ~/Documents/tasks.json |
| sound_file | string | ./notification.wav | - | - | ~/sounds/bell.wav |

## FAQ

**Q: Do I need to create a config file?**  
A: No! The app works fine with defaults. Config is optional for customization.

**Q: Can I have different configs for work and personal?**  
A: Yes! Use different data_file locations and switch the config as needed.

**Q: What happens if I delete the config file?**  
A: The app uses defaults. Your tasks are safe (stored separately).

**Q: Can I sync my config across devices?**  
A: Yes! Store the config file in Dropbox, Git, or any sync service.

**Q: How do I reset a single setting?**  
A: Set it back to the default value manually, or reset all with `config reset`.

---

**Master your workflow with custom configuration!** ⚙️
