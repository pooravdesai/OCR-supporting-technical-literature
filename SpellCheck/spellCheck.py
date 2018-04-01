import re, collections

file = open('spell-errors.txt', 'r')
model1 = collections.defaultdict(lambda: 0)
for line in file:
    line = line.replace('\n', '')
    lis = line.split(': ')
    correct_word = lis[0]
    wrong_words = lis[1].split(', ')
    for wrong_word in wrong_words:
        model1[wrong_word] = correct_word
file.close()

tokens_normal = re.findall('[a-z]+', open('english_words.txt').read().lower())
tokens_scientific = re.findall('[a-z]+', open('custom_scientific_UK.txt').read().lower())
tokens = tokens_normal + tokens_scientific
def train(tokens):
    model2 = collections.defaultdict(lambda: 1)
    for t in tokens:
        model2[t] += 1
    # print(model2)
    return model2

nwords = train(tokens)
alphabet= 'abcdefghijklmnopqrstuvwxyz'
def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word)+1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known(words):
    return set(w for w in words if w in nwords)

def spell_check(word):
    w = word
    if w=='': return
    if model1[w] != 0:
        print (model1[w])
    else:
        options = known([w]) or known(edits1(w)) or [w]
        print (max(options, key=nwords.get))

spell_check('cucomber')