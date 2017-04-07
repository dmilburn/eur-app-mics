from music21 import note, stream, meter, pitch, scale, corpus
import random
from collections import Counter, defaultdict

def simple():
    rhythms = stream.Part()
    for i in range(0,100):
        rhythms.append(simple_rhythm())
    return simple_melody(rhythms)


def generate_rhythm_library(paths=corpus.getBachChorales()):
    rhythm_library = defaultdict(Counter)
    for i, path in enumerate(paths):
        print("Working [{}/{}]: {}".format(i, len(paths), path))
        piece = corpus.parse(path)
        current_beat = []
        current_measure = 0
        for note in piece.recurse().notesAndRests:
            ts = note.getContextByClass('TimeSignature')
            if current_measure != note.measureNumber:
                current_beat.clear()
                current_measure = note.measureNumber
            current_beat.append(note.quarterLength)
            if sum(current_beat) % ts.beatDuration.quarterLength == 0:
                rhythm_library[ts.ratioString][tuple(current_beat)] += 1
                current_beat.clear()
    return rhythm_library


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