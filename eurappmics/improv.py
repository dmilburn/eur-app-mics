from music21 import note, stream
import random


def simple_rhythm(length=1):
    basic = [1, 1/2, 1/4]
    compound = [3/4]
    triplet = [1/3]
    durations = basic+compound+triplet

    rhythm = stream.Stream()
    while(length):
        n = note.Note(quarterLength=random.choice(durations))
        length -= n.quarterLength
        rhythm.append(n)
        durations = [d for d in durations
                     if length-d in durations or length-d == 0]
    return rhythm
