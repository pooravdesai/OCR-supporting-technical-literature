import pickle
class EqnParser:
    
##########################################################################################################
    
    def parse(self, pseudoOutput):
        self.inp = pseudoOutput
        #print(self.inp)
        get = open('greektex.pickle','rb')
        greektex = pickle.load(get)
        get.close()
        self.out = ''
        
        for i in range(0, len(self.inp)):
            self.inp[i] = self.inp[i].replace('—','-')
            self.inp[i] = self.inp[i].replace('−','-')
            self.inp[i] = self.inp[i].replace('‐','-')
            self.inp[i] = self.inp[i].replace('--','=')
            self.inp[i] = self.inp[i].replace('∞','\infty ')
            self.inp[i] = self.inp[i].replace('..','=')
            self.inp[i] = self.inp[i].replace('-:-:','=')
            self.inp[i] = self.inp[i].replace('.:1', 'i')
            self.inp[i] = self.inp[i].replace(':)-:', '):-:')
            self.inp[i] = self.inp[i].replace(':)', '):')
            self.inp[i] = self.inp[i].replace('.:ι', 'i')
            self.inp[i] = self.inp[i].replace('.:I', 'i')
            self.inp[i] = self.inp[i].replace('.:-', 'i')
            self.inp[i] = self.inp[i].replace('.-', 'i')
            self.inp[i] = self.inp[i].replace('l:.', '!')
             
            self.inp[i] = self.inp[i].replace('>:-:','>=')
            self.inp[i] = self.inp[i].replace('<:-:','<=')
            self.inp[i] = self.inp[i].replace("ln", " ln ")
            self.inp[i] = self.inp[i].replace("sin", " sin ")
            self.inp[i] = self.inp[i].replace("cos", " cos ")
            self.inp[i] = self.inp[i].replace("c0s", " cos ")
            self.inp[i] = self.inp[i].replace("tan", " tan ")
            self.inp[i] = self.inp[i].replace("cot", " cot ")
            self.inp[i] = self.inp[i].replace("c0t", " cot ")
            self.inp[i] = self.inp[i].replace("log", " log ")
            self.inp[i] = self.inp[i].replace("sec", " sec ")
            self.inp[i] = self.inp[i].replace("csc", " csc ")
            self.inp[i] = self.inp[i].replace('1.:', '!')
            self.inp[i] = self.inp[i].replace('l.:', '!')
            self.inp[i] = self.inp[i].replace(',.', '!')
            
            #self.inp[i] = self.inp[i].replace('):=', ')=:')
            for j in greektex:
                if j in self.inp[i]:
                    self.inp[i] = self.inp[i].replace(j,'\\' + greektex[j] + ' ')
    
        #print(self.inp)
        for i in range(0, len(self.inp)-2):
            if self.inp[i] == '(:' and self.inp[i+2] == '):' and self.inp[i+1].count(':') == 2:
                tmp = self.inp[i+1].split(':')
                #self.inp[i] = 'C('+ tmp[0] + ', ' + tmp[1] + '):'
                self.inp[i] = '{' + tmp[0] + r' \choose ' + tmp[1] + '}:'
                self.inp[i+1] = ':'
                self.inp[i+2] = ':'
        
        #print(self.inp)
        i = len(self.inp)
        while i > -1:
            i -= 1
            if self.inp[i].find('√') != -1:
                self.handleSqrt(i)
            if self.inp[i].find(':/:') != -1:
                self.handleDiv(i)
            if self.inp[i].find('∑') != -1:
                self.handleSum(i)
            if self.inp[i].find('∏') != -1:
                self.handleProduct(i)
            if self.inp[i].find('∫') != -1:
                self.handleIntegral(i)


        for i in range(0, len(self.inp)):
            for j in range(0, len(self.inp[i])):
                if self.inp[i][j] != ":":
                    self.out += self.inp[i][j]

        #the code below is to handle power.  
        for i in range(0, len(self.out)):
            if self.out[i] == '^':
                self.handlePower(i)
        
        self.out = self.out.replace("c0s", " cos ")
        return self.out
    
##########################################################################################################
    #^{}
    def handlePower(self, powIndex):
        numParen = 1
        self.out = self.out[:powIndex+1] + '{' + self.out[powIndex+2:]
        for i in range(powIndex+1, len(self.out)):
            if self.out[i] == '(':
                numParen += 1
            elif self.out[i] == ')':
                numParen -= 1
            if numParen == 0:
                self.out = self.out[:i] + '}' + self.out[i+1:]
                break

    
##########################################################################################################
    #\frac{}{}
    def handleDiv(self, divIndex):
        index = self.inp[divIndex].find(':/:')
        #print(self.inp)
        self.inp[divIndex] = r'\frac' + '{' + self.inp[divIndex][0:index] + '}' + '{' + self.inp[divIndex][index+3:-1] + '}:'
        #print(self.inp)
        
##########################################################################################################
    #\sqrt{}
    def handleSqrt(self, sqrtIndex):
        index = self.inp[sqrtIndex].find('√')
        parenNum = 1
        tmp = ''
        for i in range(index + 2, len(self.inp[sqrtIndex])):
            if self.inp[sqrtIndex][i] == '(':
                parenNum += 1
            elif self.inp[sqrtIndex][i] == ')':
                parenNum -= 1
                if parenNum == 0:
                    break
            tmp += self.inp[sqrtIndex][i]
        
        self.inp[sqrtIndex] = self.inp[sqrtIndex][0:index] +  r'\sqrt' + '{' + \
        tmp + '}' + self.inp[sqrtIndex][i+1:]
        
        if parenNum != 0:
            self.inp[sqrtIndex+1] = self.inp[sqrtIndex+1][1:]
        
        '''indexEnd = self.inp[sqrtIndex].find(':')
        self.inp[sqrtIndex] = self.inp[sqrtIndex][0:index] +  r'\sqrt' + '{' + \
        self.inp[sqrtIndex][index+1:indexEnd] + '}' + self.inp[sqrtIndex][indexEnd:]'''
                
##########################################################################################################
    #\sum_{}^{}    
    def handleSum(self, sumIndex):
        #print(self.inp)
        index = self.inp[sumIndex].find('∑')
        tmp = ''
        if index == 0:
            #tmp = 'sum of ('
            tmp = r'\sum'
        else:
            #tmp = 'sum from ' + self.inp[sumIndex][index+2:-1] + ' to ' + \
                    #self.inp[sumIndex][0:index-1] + ' of ('
            tmp = r'\sum' + '_' + '{' + self.inp[sumIndex][index+2:-1] + '}' + '^' + '{' + self.inp[sumIndex][0:index-1] + '}'
                            
        j = 0
        parenNum = 0
        flag = False
        for j in range(sumIndex+1, len(self.inp)):
            for k in range(0, len(self.inp[j])):
                if self.inp[j][k] == '(':
                    parenNum += 1
                elif self.inp[j][k] == ')':
                    parenNum -= 1
                elif parenNum == 0 and (self.inp[j][k] == '+' or self.inp[j][k] == '-' or \
                                  self.inp[j][k] == '='):
                    flag = True
                    break
            if flag:
                break
    
        for l in range(sumIndex+1, j):
            tmp += self.inp[l][0:-1]
            self.inp[l] = ':'
        
        tmp += self.inp[j][0:k]
        self.inp[j] = self.inp[j][k:]
                    
        self.inp[sumIndex] = tmp
        
        #print(self.inp)
                        
##########################################################################################################
    #\prod_{}^{}    
    def handleProduct(self, productIndex):
        index = self.inp[productIndex].find('∏')
        tmp = ''
        if index == 0:
            #tmp = 'product of ('
            tmp = r'\prod'
        else:
            #tmp = 'product from ' + self.inp[productIndex][index+2:-1] + ' to ' + \
                    #self.inp[productIndex][0:index-1] + ' of ('
            tmp = r'\prod' + '_' + '{' + self.inp[productIndex][index+2:-1] + '}' + '^' + '{' + \
                    self.inp[productIndex][0:index-1] +  '}'
                            
        j = 0
        parenNum = 0
        flag = False
        for j in range(productIndex+1, len(self.inp)):
            for k in range(0, len(self.inp[j])):
                if self.inp[j][k] == '(':
                    parenNum += 1
                elif self.inp[j][k] == ')':
                    parenNum -= 1
                elif parenNum == 0 and (self.inp[j][k] == '+' or self.inp[j][k] == '-' or \
                                  self.inp[j][k] == '='):
                    flag = True
                    break
            if flag:
                break
    
        for l in range(productIndex+1, j):
            tmp += self.inp[l][0:-1]
            self.inp[l] = ':'
        
        tmp += self.inp[j][0:k]
        self.inp[j] = self.inp[j][k:]
                    
        self.inp[productIndex] = tmp
        
       # print(self.inp)             

##########################################################################################################
    #\int_{}^{}    
    def handleIntegral(self, integralIndex):
        index = self.inp[integralIndex].find('∫')
        tmp = ''
        frm = ''
        to = ''
        parenNum = 0
        for j in range(integralIndex, len(self.inp)):
            flag = False
            for k in range(0, len(self.inp[j])):
                if self.inp[j][k] == '(':
                    parenNum += 1
                elif self.inp[j][k] == ')':
                    parenNum -= 1
                    if parenNum == 0:
                        break
                elif self.inp[j][k] == '_':
                    frm += self.inp[j][k+1:-1]
                    flag = True
                    break
                elif self.inp[j][k] == '~':
                    to += self.inp[j][k+1:-1]
                    flag = True
                    break
            if flag and j == integralIndex:
                tmp += '('  
            if not flag and j != integralIndex:
                tmp += self.inp[j][:-1]
            if parenNum == 0:
                tmp += self.inp[j][k+1:-1]
                break
        #print(tmp)
        if frm == '' and to == '':
            #ans = 'integrate ' + tmp
            ans = r'\int' + tmp
        elif frm != '' and to == '':
            #ans = 'integrate over ' + frm + ' ' + tmp
            ans = r'\int' + '_' + '{' + frm + '}' + ' ' + tmp
        else:
            #ans = 'integrate from ' + frm +  ' to ' + to + ' ' +  tmp
            ans = r'\int' + '_' + '{' + frm + '}' + ' ^ ' + '{' + to + '}' + ' ' +  tmp
        
        ans += ':'
        
        self.inp[integralIndex] = ans
        
        for k in range(integralIndex+1, j+1):
            self.inp[k] = ':' 
        


##########################################################################################################
'''
if __name__ == '__main__':
    e = EqnParser()
    out = e.parse(['∫(_D:', '(:', 'Θ:', 'ρ:', '):', 'α:', 'l:', 'f:', 'l:', '^(2:', ')d:', 'V:', '):'])
    print(e.inp)
    print(out)
'''    
#some changes for i and j