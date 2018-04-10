import Recogniser
import Identifier
from threading import Thread

class myThread(Thread):
    def __init__(self, str1, str2, check):
        super(myThread, self).__init__()
        self.image_loc = str1
        self.save_loc = str2
        self.check_state = check
        print(self.check_state)
        
    def run(self):
        print('Recogniser')
        recogniser = Recogniser.Recogniser()
        image, lines, words, characters = recogniser.recognise(self.image_loc)

        print('Identifier')
        identifier = Identifier.Identifier()
        characters = identifier.identify(image, characters)

        print('Generating Output')
        print("thread")
        for i in range(0, len(words)):
            string = ''
            for j in range(words[i][4], words[i][5] + 1):
                string += characters[j][4]
            words[i].append(string)
        
        for w in words:
            print(w[6], end = ' ')
        print ('\n')
     

def started(str1, str2, check):
    thread1 = myThread(str1, str2, check).start()
   

'''
if __name__ == '__main__':
    start('00_000.png')
'''
