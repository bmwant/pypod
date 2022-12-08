"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
import contextlib

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
with contextlib.closing(stream):
    # read data
    # while data := wf.readframes(CHUNK):
    #     stream.write(data)

    data = wf.readframes(CHUNK)
    # play stream (3)
    while len(data):
        stream.write(data)
        data = wf.readframes(CHUNK)
        # stream.stop_stream()
        
        # print(stream.get_time())
        # stream.start_stream()

    # stop stream (4)
    stream.stop_stream()

    # close PyAudio (5)
    p.terminate()
