# Task Tags - Complete Usage Guide

Learn how to organize and categorize your tasks using tags in Task Timer CLI.

## Table of Contents
- [Quick Start](#quick-start)
- [Adding Tags](#adding-tags)
- [Viewing Tagged Tasks](#viewing-tagged-tasks)
- [Tag Statistics](#tag-statistics)
- [Best Practices](#best-practices)
- [Common Use Cases](#common-use-cases)
- [Advanced Tips](#advanced-tips)

## Quick Start

### Basic Tag Usage

```bash
# Add a task with one tag
python task_timer.py add "Team meeting" 30 --tag work

# Add a task with multiple tags
python task_timer.py add "Python tutorial" 45 --tag personal learning

# List tasks with a specific tag
python task_timer.py list --filter work

# View statistics for a tag
python task_timer.py stats --filter personal
```

That's it! You're now using tags to organize your tasks.

## Adding Tags

### Single Tag

```bash
python task_timer.py add "Client call" 30 --tag work
```

### Multiple Tags

```bash
python task_timer.py add "Bug fix" 60 --tag work urgent bug-fixing
```

### With Custom Duration

```bash
# Duration before tags
python task_timer.py add "Code review" 45 --tag work development

# Duration after tags also works
python task_timer.py add "Code review" --tag work development 45
```

### No Tags (Still Works!)

```bash
# Tasks without tags work perfectly
python task_timer.py add "Quick task" 15
```

## Viewing Tagged Tasks

### List All Tasks

Shows all tasks with their tags and a summary of available tags:

```bash
python task_timer.py list
```

**Output:**
```
📋 Your Tasks:
------------------------------------------------------------
○ [1] Team meeting - 30min #work #meetings
○ [2] Python tutorial - 45min #personal #learning
✓ [3] Code review - 30min #work #development
------------------------------------------------------------

Available tags: #work (2), #personal (1), #meetings (1), #learning (1), #development (1)
```

### Filter by Tag

View only tasks with a specific tag:

```bash
python task_timer.py list --filter work
```

**Output:**
```
📋 Tasks filtered by 'work':
------------------------------------------------------------
○ [1] Team meeting - 30min #work #meetings
✓ [3] Code review - 30min #work #development
------------------------------------------------------------
```

### Case-Insensitive Filtering

These all show the same results:

```bash
python task_timer.py list --filter work
python task_timer.py list --filter Work
python task_timer.py list --filter WORK
```

## Tag Statistics

### Overall Statistics

See breakdown by tag in your general stats:

```bash
python task_timer.py stats
```

**Output:**
```
📊 Your Statistics:
--------------------------------------------------
Total tasks: 5
Completed: 2
Pending: 3
Total time spent: 75 minutes

Breakdown by tag:
--------------------------------------------------
#work: 3 tasks, 2 completed (67%), 60min
#personal: 2 tasks, 0 completed (0%), 0min
#meetings: 1 tasks, 1 completed (100%), 30min
#learning: 1 tasks, 0 completed (0%), 0min
#development: 1 tasks, 1 completed (100%), 30min
--------------------------------------------------
```

### Tag-Specific Statistics

View stats for a particular tag:

```bash
python task_timer.py stats --filter work
```

**Output:**
```
📊 Statistics for 'work':
--------------------------------------------------
Total tasks: 3
Completed: 2
Pending: 1
Total time spent: 60 minutes
--------------------------------------------------
```

## Best Practices

### 1. Use Consistent Tag Names

✅ **Good:**
```bash
python task_timer.py add "Task 1" 30 --tag work
python task_timer.py add "Task 2" 30 --tag work
```

❌ **Avoid:**
```bash
python task_timer.py add "Task 1" 30 --tag work
python task_timer.py add "Task 2" 30 --tag Work-Related  # Inconsistent
```

### 2. Keep Tags Short and Simple

✅ **Good:**
```bash
--tag work urgent frontend
```

❌ **Avoid:**
```bash
--tag "work related tasks" "very urgent" "frontend-development-javascript"
```

### 3. Use Multiple Tags for Context

Tasks can have multiple dimensions:

```bash
# Project + Priority + Type
python task_timer.py add "API endpoint" 90 --tag project-alpha urgent backend

# Category + Subcategory
python task_timer.py add "Spanish lesson" 45 --tag personal learning language
```

### 4. Create a Tag System

Develop your own tag conventions:

**By Category:**
- `work`, `personal`, `study`, `health`

**By Priority:**
- `urgent`, `important`, `low-priority`

**By Project:**
- `project-alpha`, `project-beta`, `side-project`

**By Type:**
- `meeting`, `coding`, `writing`, `admin`

### 5. Review Your Tags Regularly

Check which tags you're using:

```bash
python task_timer.py list  # Shows all tags at bottom
```

Consolidate similar tags for better organization.

## Common Use Cases

### Work/Life Balance

Track personal vs professional time:

```bash
# Work tasks
python task_timer.py add "Team standup" 15 --tag work meetings
python task_timer.py add "Code feature" 120 --tag work development

# Personal tasks
python task_timer.py add "Gym" 60 --tag personal health
python task_timer.py add "Read book" 30 --tag personal learning

# Compare time spent
python task_timer.py stats --filter work
python task_timer.py stats --filter personal
```

### Project Management

Track multiple projects:

```bash
# Project Alpha
python task_timer.py add "Design mockup" 60 --tag project-alpha design
python task_timer.py add "Backend API" 120 --tag project-alpha backend

# Project Beta
python task_timer.py add "User research" 90 --tag project-beta research
python task_timer.py add "Prototype" 60 --tag project-beta design

# View project-specific tasks
python task_timer.py list --filter project-alpha
python task_timer.py stats --filter project-beta
```

### Priority Management

Organize by urgency:

```bash
# High priority
python task_timer.py add "Fix production bug" 60 --tag work urgent bug

# Medium priority
python task_timer.py add "Update docs" 30 --tag work docs

# Low priority
python task_timer.py add "Refactor old code" 90 --tag work low-priority refactor

# Focus on urgent tasks
python task_timer.py list --filter urgent
```

### Client Work (Freelancers)

Track billable hours per client:

```bash
# Client A tasks
python task_timer.py add "Website redesign" 120 --tag client-a design billable
python task_timer.py add "Client meeting" 30 --tag client-a meetings billable

# Client B tasks
python task_timer.py add "App development" 180 --tag client-b development billable

# Non-billable
python task_timer.py add "Invoice creation" 20 --tag admin non-billable

# Track billable time per client
python task_timer.py stats --filter client-a
python task_timer.py stats --filter billable
```

### Learning & Development

Organize study topics:

```bash
# Programming
python task_timer.py add "Python tutorial" 60 --tag learning programming python
python task_timer.py add "JavaScript course" 90 --tag learning programming javascript

# Languages
python task_timer.py add "Spanish lesson" 30 --tag learning language spanish
python task_timer.py add "French practice" 30 --tag learning language french

# Track learning time
python task_timer.py stats --filter learning
python task_timer.py list --filter programming
```

### Health & Wellness

Track different health activities:

```bash
# Exercise
python task_timer.py add "Morning run" 30 --tag health exercise cardio
python task_timer.py add "Yoga" 45 --tag health exercise flexibility

# Nutrition
python task_timer.py add "Meal prep" 60 --tag health nutrition

# Mental health
python task_timer.py add "Meditation" 20 --tag health mindfulness

# View health stats
python task_timer.py stats --filter health
python task_timer.py list --filter exercise
```

## Advanced Tips

### 1. Hierarchical Tags

Use prefixes for hierarchy:

```bash
# Development tasks
python task_timer.py add "Frontend work" 60 --tag dev-frontend
python task_timer.py add "Backend work" 90 --tag dev-backend
python task_timer.py add "DevOps setup" 45 --tag dev-devops

# All development tasks
python task_timer.py list --filter dev
```

### 2. Time-Based Tags

Track tasks by time period:

```bash
python task_timer.py add "Q1 Review" 60 --tag work q1-2024
python task_timer.py add "Annual planning" 120 --tag work q4-2024

python task_timer.py stats --filter q1-2024
```

### 3. Status Tags

Track task states:

```bash
python task_timer.py add "Research" 30 --tag work project-alpha research
python task_timer.py add "Implementation" 120 --tag work project-alpha in-progress
python task_timer.py add "Testing" 60 --tag work project-alpha review

python task_timer.py list --filter in-progress
```

### 4. Context Tags

Tag by location or context:

```bash
python task_timer.py add "Deep work" 120 --tag work home focus
python task_timer.py add "Quick emails" 15 --tag work office admin
python task_timer.py add "Team meeting" 30 --tag work office meetings

python task_timer.py list --filter home
python task_timer.py list --filter office
```

### 5. Combining Filters with Grep (Advanced)

For complex filtering:

```bash
# Show only completed work tasks
python task_timer.py list --filter work | grep "✓"

# Show only pending personal tasks
python task_timer.py list --filter personal | grep "○"

# Count tasks by tag
python task_timer.py list | grep "#urgent" | wc -l
```

## Tag Naming Conventions

### Recommended Formats

**Single word (best):**
```bash
--tag work urgent python
```

**Hyphenated (for compound terms):**
```bash
--tag high-priority client-work front-end
```

**Avoid spaces:**
```bash
# ❌ Don't do this
--tag "work related" "high priority"

# ✅ Do this instead
--tag work-related high-priority
```

### Tag Categories

Consider organizing tags into categories:

**Category Tags:**
- `work`, `personal`, `study`, `health`, `finance`

**Priority Tags:**
- `urgent`, `high`, `medium`, `low`

**Type Tags:**
- `meeting`, `coding`, `writing`, `admin`, `research`

**Project Tags:**
- `project-name`, `client-name`, `initiative-name`

**Status Tags:**
- `planned`, `in-progress`, `review`, `blocked`

## Troubleshooting

### Tag Not Showing in Filter

**Problem:** Task not appearing when filtering by tag

**Solution:**
1. Check tag spelling: `python task_timer.py list` (shows all tags)
2. Tags are case-insensitive but must match exactly
3. Ensure the task actually has that tag

### Too Many Tags

**Problem:** Tag list becoming unwieldy

**Solution:**
1. Review tags regularly: `python task_timer.py list`
2. Consolidate similar tags (manually edit data file if needed)
3. Stick to your tag conventions

### Finding Old Tags

**Problem:** Can't remember which tags you've used

**Solution:**
```bash
# List all tasks to see tag summary
python task_timer.py list

# View statistics to see all tags with counts
python task_timer.py stats
```

## Integration with Workflow

### Morning Routine

```bash
# Review today's work tasks
python task_timer.py list --filter work

# Check personal goals
python task_timer.py list --filter personal

# See what's urgent
python task_timer.py list --filter urgent
```

### End of Day Review

```bash
# See what you completed today
python task_timer.py stats --filter work

# Review personal time
python task_timer.py stats --filter personal

# Overall productivity
python task_timer.py stats
```

### Weekly Review

```bash
# Check each project's progress
python task_timer.py stats --filter project-alpha
python task_timer.py stats --filter project-beta

# Review time allocation
python task_timer.py stats  # Shows full breakdown
```

## Examples from Real Users

### Software Engineer

```bash
# Daily work
python task_timer.py add "Code review" 30 --tag work dev code-review
python task_timer.py add "Feature development" 120 --tag work dev feature
python task_timer.py add "Bug fixing" 60 --tag work dev bugs urgent

# Meetings
python task_timer.py add "Stand-up" 15 --tag work meetings daily
python task_timer.py add "Sprint planning" 60 --tag work meetings planning

# Learning
python task_timer.py add "Learn Rust" 45 --tag personal learning rust

# Track coding time
python task_timer.py stats --filter dev
```

### Content Creator

```bash
# Content production
python task_timer.py add "Video editing" 120 --tag work video production
python task_timer.py add "Script writing" 60 --tag work writing content
python task_timer.py add "Thumbnail design" 30 --tag work design graphics

# Social media
python task_timer.py add "Social posts" 20 --tag work social-media marketing

# Track content creation time
python task_timer.py stats --filter production
```

### Student

```bash
# Classes
python task_timer.py add "Math homework" 45 --tag school math homework
python task_timer.py add "History essay" 90 --tag school history writing
python task_timer.py add "Physics lab" 120 --tag school physics lab

# Study
python task_timer.py add "Exam prep" 60 --tag study finals
python task_timer.py add "Reading" 30 --tag study reading

# Per subject time
python task_timer.py stats --filter math
python task_timer.py stats --filter history
```

## Future Enhancements

Features we're considering:
- Tag autocomplete
- Tag rename/merge commands
- Tag color customization
- Tag templates
- Most-used tags report

---

**Happy tagging! 🏷️** Use tags to unlock powerful organization in your task management workflow.
