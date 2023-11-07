import winsound
import time

def beep_pattern(pattern, repeat=8):
    for _ in range(repeat):
        for freq, duration in pattern:
            winsound.Beep(freq, duration)
            time.sleep(0.1)

# Function to start playing the sound
def start_sound():
    beep_pattern([(500, 200), (700, 300), (300, 500)])

# Call start_sound when you want to start playing the sound
#start_sound()
