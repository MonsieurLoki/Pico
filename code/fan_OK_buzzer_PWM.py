
# https://www.youtube.com/watch?v=S4zPLBTC7_w
# ATTENTION : the pins 18 and 26 are inverted in this tuto ! (but the rest is OK)

from machine import Pin, PWM
import utime

# darlington = Pin(0, Pin.OUT)
# darlington.value(1)
# pulse = Pin(18, Pin.OUT)
# receiver = Pin(26, Pin.IN, Pin.PULL_DOWN)

speaker = PWM(Pin(15))

bp = 3 		# blanche
b  = 2 		# blanche
n  = 1		# noire
c  = 0.5		# croche
dc = 0.25	# double-croche
qc = 0.125	# double-croche


class Song:
    def __init__(self, notes, dur, bm):
        self.notes = notes
        self.dur = dur
        self.bm = bm


frereJacques = Song(
    notes = ['C', 'D', 'E', 'C', 'C', 'D', 'E','C' ],
    dur =  	[n,   n,   n,   n,   n,   n,   n,    n],
    bm = 220  # beats per minute
    )

song2 = Song(
    notes = ['C',' ','G','G','G#','G',' ', 'B2',' ','C2' ],
    dur =  	[ c,  c,  c,  c,  n,   c,  b,  c,  c, c  ],
    bm = 200  # beats per minute
    )

alarm = Song(
    notes = ['A',' ','A',' ','A'],
    dur =  	[ dc, dc, dc, dc, dc ],
    bm = 200  # beats per minute
    )

wifi_notif = Song(
    notes = ['A',' ','E',' ','A2'],
    dur =  	[ dc, qc, dc, qc, dc ],
    bm = 200  # beats per minute
    )


#------------------
def note_to_frequency(note):
  """
  This function takes a musical note (A, B, C, D, E, F, or G) and returns its corresponding frequency in Hz.

  Args:
      note: A string representing a musical note (uppercase only).

  Returns:
      The frequency of the note in Hz or None if the note is invalid.
  """

  # Base frequency for A4 (440 Hz)
  base_frequency = 440.0

  # Define the semitone multipliers for each note relative to A4
  semitone_steps = {
      'A': 0,
      'B': 2,
      'C': 3,
      'D': 5,
      'E': 7,
      'F': 8,
      'G': 10,
      'G#':11,
      'A2': 12,
      'B2': 14,
      'C2': 15,
      ' ' : -1
  }

  # Check for valid note
  if note not in semitone_steps:
      return None
  if note == ' ':
      return 1

  # Calculate the number of semitones from A4
  semitones_from_a4 = semitone_steps[note]

  # Calculate the frequency using the formula: f = base_frequency * 2^(semitones/12)
  frequency = base_frequency * 2**(semitones_from_a4 / 12)

  return int(frequency)



def play(song):

    notes = song.notes
    dur = song.dur
    bm = song.bm
    for i in range(len(notes)):
        frequency = note_to_frequency(notes[i])
        if frequency:
            print(f"Note: {notes[i]} - Frequency: {frequency:.2f} Hz {dur[i]}")
        else:
            print(f"Invalid note: {notes[i]}")
          
        speaker.duty_u16(3000)
        if frequency > 1:
            speaker.freq(frequency)
        else:
            speaker.duty_u16(0)
        dur_ms = int(dur[i]*60/bm*1000)
        utime.sleep_ms(dur_ms)
        print(dur_ms)
        speaker.duty_u16(0)
        utime.sleep(0.01)
        

def test():
    distance = 200
    frequency = 1700
    frequency = 440
    while False:
        print(distance, frequency)
        speaker.duty_u16(3000)
        speaker.freq(frequency)
    #     utime.sleep(0.05)
        utime.sleep(1)
        speaker.duty_u16(0)
        utime.sleep(distance/ 1000)
        utime.sleep(0.1)
        distance -= 1
        frequency += 30

    speaker.duty_u16(0)



def main():

    print("start")

    # while True:
    #     check_HC_SR04()

    #play(frereJacques)
    #play(song2)

    #    theme2()
#     play(alarm)
    play(wifi_notif)
    
    
if __name__ == "__main__":
    main()

