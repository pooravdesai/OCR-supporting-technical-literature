import Recogniser
import Identifier

def start(str1):
    print('Recogniser')
    recogniser = Recogniser.Recogniser()
    image, lines, words, characters = recogniser.recognise(str1)

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


if __name__ == '__main__':
    start('C:\\Users\\Dell\\Documents\Euler-000001.jpg')
