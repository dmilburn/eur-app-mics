from music21 import note, stream, meter
import random


def simple_rhythm(ts = meter.TimeSignature('4/4')):
    ## TODO: Just generate a list of rhythmic vocab and randomly choose from that
    ql = ts.beatDuration.quarterLength
    tl = ts.totalLength
    basic = [ql*(x+1) for x in range(int(tl/ql))]
    subdivisions = [.25*(x+1) for x in range(int(ql/.25))]
    triplet = [x/3 for x in basic if x not in basic+subdivisions]
    durations = list(set(basic+subdivisions+triplet))

    rhythm = stream.Measure()
    rhythm.timeSignature = ts
    while(tl):
        n = note.Note(quarterLength=random.choice(durations))
        if n.quarterLengthFloat in triplet:
            tl -= n.quarterLength*3
            rhythm.repeatAppend(n, 3)
        else:
            tl -= n.quarterLength
            rhythm.append(n)
        durations = [d for d in set(basic+subdivisions+triplet)
                     if tl-d >= 0]
    return rhythm
