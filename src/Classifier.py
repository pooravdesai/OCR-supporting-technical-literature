import re

class Classifier:
    
##################################################################################################################
    def classify(self, lines, words, chars):
        waitFlag = False
        prevWaitFlag = False
        waitFlagLen = False
        prevWaitFlagLen = False
        
        
        for j in range(0, len(words)):
            prevWaitFlag = waitFlag
            waitFlag = False
            prevWaitFlagLen = waitFlagLen
            waitFlagLen = False
            minr = 0
            maxr = 0
            if words[j][4] <= words[j][5]:
                minr = min([chars[i][1] for i in range(words[j][4], words[j][5]+1)])
                maxr = max([chars[i][3] for i in range(words[j][4], words[j][5]+1)])
            mid = (minr + maxr)//2
            flag = False
            for i in range(words[j][4], words[j][5]+1):
                if (chars[i][4] in ['∑', '∫', '∏', '√', '^', '=', '>', '<', '<=', '>=']) \
                or ((chars[i][3]-0.15*(chars[i][3]-chars[i][1])<= mid or \
                     chars[i][1]+0.15*(chars[i][3]-chars[i][1]) >= mid) \
                        and chars[i][4] not in [',','\"','\'', '.', '`']):
                    words[j].append('math')
                    #print(words[j])
                    flag = True
                    break
                    
            if not flag:                      
                if not bool(re.compile(r'[^0-9&]').search(words[j][-1])):
                    words[j].append('math')
                
                elif not bool(re.compile(r'[^.,:;&]').search(words[j][-1])):
                    words[j].append('math')
                    
                elif len(words[j][-1]) == 1 and ('a' <= words[j][-1] and words[j][-1] <= 'z') or \
                ('A' <= words[j][-1] and words[j][-1] <= 'Z'):
                    waitFlagLen = True
                    
                elif not bool(re.compile(r'[^a-zA-Z\-æœﬀﬁﬂﬃﬄﬅ@._\'\&#01&]').search(words[j][-1])):
                    words[j].append('text')
                    
                elif words[j][-1][0] == '(' and words[j][-1][-1] ==')' and \
                not bool(re.compile(r'[^a-zA-Zæœﬀﬁﬂﬃﬄﬅ@._\'\&#01\-&]').search(words[j][-1][1:-1])):
                    words[j].append('text')
                    
                    
                elif words[j][-1][0] == '(' and \
                not bool(re.compile(r'[^a-zA-Zæœﬀﬁﬂﬃﬄﬅ@._\'\&#01\-&]').search(words[j][-1][1:-1])):
                    waitFlag = True
                    
                elif words[j][-1][0] == ')' and \
                not bool(re.compile(r'[^a-zA-Zæœﬀﬁﬂﬃﬄﬅ@._\'\&#01\-&]').search(words[j][-1][1:-1])):
                    if j!=0:
                        words[j].append(words[j-1][-1])
                    else:
                        words[j].append('math')
                
                elif not bool(re.compile(r'[^a-zA-Zæœﬀﬁﬂﬃﬄﬅ@._\'\&#01\-&]').search(words[j][-1][:-1])) and \
                              words[j][-1][-1] in ['.',',',';',':','-','!','?']:
                    words[j].append('text')
                else:
                    words[j].append('math')
                    #print(words[j])
                    
            if prevWaitFlag:
                if waitFlag:
                    words[j-1].append('math')
                    words[j].append('math')
                    waitFlag = False
                else:
                    words[j-1].append(words[j][-1])
                    
            if waitFlag and j == len(words)-1:
                words[j-1].append('math')
                
            if prevWaitFlagLen:
                if waitFlagLen:
                    words[j-1].append('text')
                    words[j].append('text')
                    waitFlagLen = False
                else:
                    words[j-1].append(words[j][-1])
                
            if waitFlagLen and j == len(words)-1:
                words[j-1].append('text')

        
        #words = self.getMathLines(lines, words) 
        words = self.mergeMathReg(lines, words)
        return words
    
##################################################################################################################
    def getMathLines(self, lines, words):
        for l in lines:
            math = False
            for i in range(l[-2], l[-1]+1):
                if words[i][-1] == 'math':
                    math = True
                    break
            if math:
                for i in range(l[-1][0], l[-1][1]+1):
                    words[i][-1] = 'math'
        return words
                    
##################################################################################################################
    def mergeMathReg(self, lines, words):
        newWords = []
        for i in range(0, len(lines)):
            beg = len(newWords)
            prevWasMath = False
            for j in range(lines[i][-2], lines[i][-1]+1):
                if words[j][-1] == 'text':
                    prevWasMath = False
                    newWords.append(words[j])
                elif prevWasMath:
                    newWords[-1][2] = words[j][2]
                    newWords[-1][5] = words[j][5]
                else:
                    prevWasMath = True
                    newWords.append(words[j])
            lines[i][-2] = beg
            lines[i][-1] = len(newWords) - 1
        return newWords
    
    
#Add 10 pixels vertically to the eqn image
                    
                     
                    
        