from random import choice 


class wordList:
    def __init__(self, filename): 
        with open(filename, 'r') as file: 
            self.text = file.read()

        self.words = self.text.split()


    def get_word(self):
        return choice(self.words)

    def get_words(self):
        return self.words

if __name__ == '__main__':
    word = wordList('words.txt')
    print(word.get_word())

