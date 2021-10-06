import re, collections


class Corrector:

######################################################################################################
    def __init__(self):
        self.tokens_normal = re.findall('[a-z]+', open('english_words.txt').read().lower())
        self.tokens_scientific = re.findall('[a-z]+', open('custom_scientific_UK.txt').read().lower())
        self.tokens = self.tokens_normal + self.tokens_scientific
        self.alphabet= 'abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLZXCVBNM'        
        #self.model1 = []
        self.buildModel()
        
######################################################################################################

    def buildModel(self):
        #self.model1 = self.errors_train()
        self.model2 = self.train(self.tokens)
        
######################################################################################################
    def correct(self, words):
        for i in range (0, len(words)):
            if words[i][-1] == 'text':
                w = words[i][-2]    #This is the predicted word.It may be incorrect or contain punctuations
                if w != '' and w[0] in ['(', '\'', '\"']:
                    w = w[1:]
                if w != '' and w[-1] in [')', ',', '.', ';', ':', '-', '?' '`', '\'', '\"']:
                    w = w[:-1]
                w = self.spell_check(w)
                if w != '':
                    words[i][-2] = w
        return words
        
###################################################################################################### 
    def spell_check(self, word):
        w = word
        if w=='': 
            return
        '''if self.model1[w] != 0:
            return self.model1[w]
        else:'''
        options = self.known([w]) or self.known(self.edits1(w)) or [w]
        return max(options, key=self.model2.get)


######################################################################################################
    def errors_train(self):
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
        return model1

######################################################################################################
    def train(self, tokens):
        model2 = collections.defaultdict(lambda: 1)
        for t in tokens:
            model2[t] += 1
        return model2

    # nwords = train(tokens)
######################################################################################################
    def edits1(self, word):
        splits     = [(word[:i], word[i:]) for i in range(len(word)+1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
        inserts    = [a + c + b for a, b in splits for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

######################################################################################################
    def known(self, words):
        return set(w for w in words if w in self.model2)

######################################################################################################
if __name__ == '__main__':
    L = [['bergman', 'text'], ['b3t', 'text']]
    correct_test = Corrector()
    #correct_test.buildModel()
    words = correct_test.correct(L)
    for w in words:
        print(w)
