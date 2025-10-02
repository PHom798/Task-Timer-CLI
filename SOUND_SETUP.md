# Sound Notification Setup Guide

This guide will help you set up sound notifications for Task Timer CLI.

## Quick Setup

### Option 1: Generate Sound File (Recommended)

The easiest way is to generate the sound file using the included script:

```bash
# Generate a pleasant bell-like notification sound
python generate_sound.py

# Or generate a simple beep
python generate_sound.py --simple
```

This creates `notification.wav` in the current directory - exactly what you need!

### Option 2: Download Free Sound

Download a free notification sound from these sources:

#### Freesound.org (Recommended)
1. Visit [freesound.org](https://freesound.org)
2. Search for "notification bell" or "timer bell"
3. Filter by "CC0" license (public domain)
4. Download as WAV format
5. Rename to `notification.wav`

**Good search terms:**
- "notification bell"
- "timer complete"
- "ding"
- "chime"

#### Pixabay
1. Visit [pixabay.com/sound-effects](https://pixabay.com/sound-effects/)
2. Search "notification" or "bell"
3. All sounds are royalty-free
4. Download and convert to WAV if needed

#### Recommended sounds:
- Short bell/chime (0.5-1 second)
- Clean, not too loud
- Pleasant tone

### Option 3: Use System Sounds

**macOS:**
```bash
# List available system sounds
ls /System/Library/Sounds/

# Use Glass sound (recommended)
afconvert /System/Library/Sounds/Glass.aiff notification.wav -d LEI16

# Or use Ping
afconvert /System/Library/Sounds/Ping.aiff notification.wav -d LEI16
```

**Linux (with sox):**
```bash
# Install sox if needed
sudo apt-get install sox  # Ubuntu/Debian
sudo yum install sox      # Fedora/RHEL

# Generate a bell sound
sox -n notification.wav synth 0.7 sine 800 sine 1200 sine 1600 remix - fade 0 0.7 0.5

# Or a simple beep
sox -n notification.wav synth 0.5 sine 800 fade 0 0.5 0.3
```

**Windows:**
```bash
# Windows doesn't have built-in tools, use Option 1 or 2
python generate_sound.py
```

## Installation Steps

### Step 1: Install Dependencies

```bash
# Install playsound library
pip install playsound

# Or install all requirements
pip install -r requirements.txt
```

### Step 2: Add Sound File

Choose one of the options above to create `notification.wav`, then place it in the same directory as `task_timer.py`:

```
task-timer-cli/
├── task_timer.py
├── notification.wav  ← Your sound file goes here
├── requirements.txt
└── README.md
```

### Step 3: Test It

Test the sound notification:

```bash
# Test using playsound directly
python -c "from playsound import playsound; playsound('notification.wav')"

# Or test with the timer
python task_timer.py add "Test task" 1
python task_timer.py start 1
```

## Sound File Specifications

For best results, use these specifications:

| Property | Recommended Value |
|----------|-------------------|
| Format | WAV (uncompressed) |
| Sample Rate | 44100 Hz |
| Bit Depth | 16-bit |
| Channels | Mono (1 channel) |
| Duration | 0.5 - 1.0 seconds |
| File Size | < 100 KB |

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'playsound'"

**Solution:**
```bash
pip install playsound
```

### Problem: Sound doesn't play

**Check these:**
1. Is `notification.wav` in the same directory as `task_timer.py`?
   ```bash
   ls -la notification.wav
   ```

2. Is the file a valid WAV file?
   ```bash
   file notification.wav
   # Should output: notification.wav: RIFF (little-endian) data, WAVE audio
   ```

3. Can you play it manually?
   ```bash
   python -c "from playsound import playsound; playsound('notification.wav')"
   ```

4. Check volume settings on your system

### Problem: "playsound" has issues on Python 3.10+

**Solution:** Use an older version or alternative:
```bash
# Try older version
pip install playsound==1.2.2

# Or use alternative approach with PyAudio
pip install simpleaudio
```

### Problem: Permission denied or file not found

**Solution:**
```bash
# Check file permissions
chmod 644 notification.wav

# Or use absolute path in code (for debugging)
```

### Problem: Sound plays but is too quiet/loud

**Solution:** Adjust the volume in the sound file:

```python
# Increase volume in generated sound
# Edit generate_sound.py, change this line:
sample_int = int(sample * 32767 * 0.8)  # Change 0.8 to higher (1.0 max) or lower
```

Or edit with audio software (Audacity, etc.)

## Using Silent Mode

If you prefer no sound notifications:

```bash
# Use --silent flag
python task_timer.py start 1 --silent

# Works with break timer too
python task_timer.py start 1 --break 5 --silent
```

## Advanced: Custom Sound Files

You can use any WAV file as the notification sound:

1. Find or create your preferred sound
2. Convert to WAV format (use online converters or Audacity)
3. Optimize the file:
   - Keep it short (< 1 second)
   - Use mono channel
   - Use 44100 Hz sample rate
   - Keep file size small
4. Name it `notification.wav` and place in the correct directory

### Converting with ffmpeg:

```bash
# Install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
# Windows: Download from ffmpeg.org

# Convert any audio file to WAV
ffmpeg -i your_sound.mp3 -ar 44100 -ac 1 -y notification.wav

# Trim to first second
ffmpeg -i your_sound.wav -t 1 -ar 44100 -ac 1 -y notification.wav
```

## Testing Different Sounds

Create multiple sound files and test them:

```bash
# Generate different variations
python generate_sound.py  # Bell-like (default)
mv notification.wav notification_bell.wav

python generate_sound.py --simple  # Simple beep
mv notification_simple.wav notification_beep.wav

# Test each one
cp notification_bell.wav notification.wav
python task_timer.py start 1

cp notification_beep.wav notification.wav
python task_timer.py start 1
```

## For Contributors

When contributing sound-related changes:

1. **Don't commit large binary files** - Keep notification.wav small (< 100 KB)
2. **Document the source** - Note where the sound came from
3. **Use free/open licenses** - CC0, Public Domain, or MIT
4. **Test cross-platform** - Verify on Windows, macOS, and Linux
5. **Provide alternatives** - Include the generate_sound.py script

## License Information

If you download a sound from online sources:
- Use CC0 (Creative Commons Zero) for no attribution required
- Use CC-BY for attribution required (include credit in README)
- Avoid copyrighted commercial sounds
- When in doubt, generate your own using the included script

## Support

If you continue having issues:
1. Check the GitHub issues for similar problems
2. Verify playsound installation: `pip show playsound`
3. Test with the generated sound file first
4. Try the --silent flag as a workaround
5. Open an issue with detailed error messages

---
