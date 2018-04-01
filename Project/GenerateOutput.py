import Recogniser
import Identifier
import threading

class myThread(threading.Thread):
    def __init__(self, str):
        super(myThread, self).__init__()
        self.threadData = str
        self._stop_event = threading.Event()
    def run(self):
        print('Recogniser')
        recogniser = Recogniser.Recogniser()
        image, lines, words, characters = recogniser.recognise(self.threadData)

        print('Identifier')
        identifier = Identifier.Identifier()
        characters = identifier.identify(image, characters)

        print('Generating Output')
        for i in range(0, len(words)):
            string = ''
            for j in range(words[i][4], words[i][5] + 1):
                string += characters[j][4]
            words[i].append(string)
        
        for w in words:
            print(w[6], end = ' ')
        '''
        try:
            thread1.stop()
        except:
            print("Thread could not be stopped")
        '''


        def stop(self):
            self._stop_event.set()

        def stopped(self):
            return self._stop_event.is_set()


def started(str1):
    thread1 = myThread(str1)
    thread1.start()

'''
if __name__ == '__main__':
    start('00_000.png')
'''
