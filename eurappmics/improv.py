from music21 import note, stream, meter, pitch, scale
import random

def simple():
    i = 0
    rhythms = stream.Part()
    while i < 100:
        rhythms.append(simple_rhythm())
        i += 1
    return simple_melody(rhythms)

def simple_rhythm(ts = meter.TimeSignature('4/4')):
    ## TODO: Just generate a list of rhythmic vocab and randomly choose from that
    ql = ts.beatDuration.quarterLength
    tl = ts.barDuration.quarterLength
    basic = [ql*(x+1) for x in range(int(tl/ql))]
    subdivisions = [.25*(x+1) for x in range(int(ql/.25))]
    triplet = [x/3 for x in basic if x/3 not in basic+subdivisions]
    durations = list(set(basic+subdivisions+triplet))
    rhythm = stream.Measure()
    rhythm.timeSignature = ts
    while(tl):
        n = note.Note(quarterLength=random.choice(durations))
        if float(n.quarterLength) in triplet:
            tl -= n.quarterLength*3
            rhythm.repeatAppend(n, 3)
        else:
            tl -= n.quarterLength
            rhythm.append(n)
        durations = [d for d in set(basic+subdivisions) if tl-d >= 0] + \
                    [d for d in set(triplet) if tl-(d*3) >= 0]
    return rhythm

def simple_melody(melody, key='c'):
    hbscale = scale.WeightedHexatonicBlues(key)
    length_of_chain = 6
    chain = 0
    direction = 'ascending'
    next_pitch = hbscale.next()
    for measure in melody.measures(0,None):
        for note in measure.notes:
            if chain == length_of_chain:
                chain = 0
                direction = 'ascending' if direction == 'descending' else 'descending'

            next_pitch = hbscale.next(next_pitch, direction)
            note.pitch = next_pitch
            chain += 1

    return melody