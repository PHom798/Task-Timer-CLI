#!/usr/bin/env python3
"""
Generate a simple notification sound for Task Timer CLI
Creates a pleasant bell-like sound using sine waves
"""

import wave
import struct
import math

def generate_notification_sound(
    filename="notification.wav",
    duration=0.7,
    sample_rate=44100
):
    """
    Generate a multi-tone notification bell sound
    
    Args:
        filename: Output WAV filename
        duration: Duration in seconds
        sample_rate: Audio sample rate in Hz
    """
    num_samples = int(sample_rate * duration)
    
    # Generate a pleasant bell sound using multiple frequencies
    # Bell sounds typically have multiple harmonics
    frequencies = [800, 1200, 1600]  # Main tone and harmonics
    amplitudes = [0.5, 0.3, 0.2]     # Relative volumes
    
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        sample = 0
        
        # Combine multiple sine waves for richer sound
        for freq, amp in zip(frequencies, amplitudes):
            sample += math.sin(2 * math.pi * freq * t) * amp
        
        # Apply exponential decay for natural bell fade
        decay = math.exp(-4 * t / duration)
        sample *= decay
        
        # Apply slight fade in at the start to avoid clicks
        if t < 0.01:
            fade_in = t / 0.01
            sample *= fade_in
        
        # Convert to 16-bit integer (-32768 to 32767)
        sample_int = int(sample * 32767 * 0.8)  # 0.8 to avoid clipping
        samples.append(sample_int)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)        # Mono
        wav_file.setsampwidth(2)        # 2 bytes (16-bit)
        wav_file.setframerate(sample_rate)
        
        for sample in samples:
            wav_file.writeframes(struct.pack('h', sample))
    
    # Get file size
    import os
    file_size = os.path.getsize(filename)
    
    print(f"✓ Generated {filename}")
    print(f"  Duration: {duration}s")
    print(f"  Sample rate: {sample_rate} Hz")
    print(f"  File size: {file_size / 1024:.1f} KB")
    print(f"\nTest the sound:")
    print(f"  python -c \"from playsound import playsound; playsound('{filename}')\"")

def generate_simple_beep(
    filename="notification_simple.wav",
    duration=0.5,
    frequency=800,
    sample_rate=44100
):
    """
    Generate a simple beep sound (alternative option)
    
    Args:
        filename: Output WAV filename
        duration: Duration in seconds
        frequency: Tone frequency in Hz
        sample_rate: Audio sample rate in Hz
    """
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        # Linear fade out
        fade = 1.0 - (t / duration)
        sample = math.sin(2 * math.pi * frequency * t) * fade
        sample_int = int(sample * 32767)
        samples.append(sample_int)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for sample in samples:
            wav_file.writeframes(struct.pack('h', sample))
    
    print(f"✓ Generated {filename} (simple beep)")

if __name__ == "__main__":
    import sys
    
    print("Task Timer CLI - Notification Sound Generator\n")
    
    # Check if user wants simple or bell sound
    if len(sys.argv) > 1 and sys.argv[1] == "--simple":
        print("Generating simple beep sound...")
        generate_simple_beep()
    else:
        print("Generating bell-like notification sound...")
        generate_notification_sound()
        
        print("\n💡 Tip: Use --simple flag for a basic beep sound")
        print("   python generate_sound.py --simple")
