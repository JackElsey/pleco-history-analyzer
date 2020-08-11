import glob

# read list of known words from known_words.txt
known_words = list()
with open('known_words.txt') as f:
    for line in f:
        known_words.append(line.split('\t')[0])

# read list of words from Pleco flashcard export file
flashcards = list()
flashcard_file = glob.glob('flash-*.txt')[0]
with open(flashcard_file) as f:
    for line in f:
        flashcards.append(line.split('\t')[0])
        
flashcards[0] = flashcards[0].replace('\ufeff','')

# determine set of words that are in Pleco flashcard export
# file but not in list of known words
kw_set = set(known_words)
fc_set = set(flashcards)
out_set = fc_set - kw_set

# save output
with open('output.txt', 'w') as f:
    for i, word in enumerate(out_set, start=1):
        f.write(word+'\r\n')
