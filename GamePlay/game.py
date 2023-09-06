
import time
from pwinput import pwinput
import requests

key = "Copywrite @ Chinmay Routray"

class Game:

    def __init__(self):
        self.max_chances = 8
        self.guess_list = []
        self.status = 'to be played'
        self.base_url = "http://127.0.0.1:8000/Hangman-AI/game/guess/"

        # hash of key is stored
        self.header = {"X-API-Key" : key}

    @staticmethod
    def valid_word(word):
        for letter in word:
            if ord(letter) not in range(97, 97+26):
                return False
        return True
    

    @staticmethod
    def make_obscure(word, guess_list):
        hidden = []
        for w in word:
            if w in guess_list:
                hidden.append(w)
            else:
                hidden.append('_')
        return hidden
    
    
    
    def guess_letter(self, hidden_word, guess_list):
        l_str = ''
        for s in guess_list:
            l_str += s 
        if guess_list == []:
            l_str = ' '
        
        #making request
        url = self.base_url + hidden_word + '/' + l_str
        header = self.header
        return requests.get(url, headers = header).json()


if __name__ == '__main__':

    game = Game()
    # print(type(game.guess_letter('a_t', 'a')))

    print("Please enter the word you want to be guess.\n Enter quit to abort.")
    n = 3
    flag = 0
    while n > 0 :
        word = pwinput("Enter the word...   ", '*').strip().lower() 

        if word == 'quit':
            flag = 0
            print("As you wish loser !")
            break

        # creating hidden word
        hidden_word = game.make_obscure(word, game.guess_list)
        if Game.valid_word(word):
            flag = 1
            n = 0
        else:
            print("Please, enter an English word.")
            n -=1
    
    # game begins
    count = 0
    if flag:

        print("Let the games begin...")
        print("Trying to guess letters...\n")

        game.status = 'failure'

        while count < game.max_chances:

            print("Word to guess           ", *hidden_word, sep=' ', end='\n')

            guess = str(game.guess_letter(''.join(hidden_word), game.guess_list))

            time.sleep(1)
            
            #same version can be used by human player
            # guess = input()
            print('\n')

            print(f"AI guess is       {guess}")

            # adding to guess list
            game.guess_list.append(guess)

            hidden_word = game.make_obscure(word, game.guess_list)
            
            if '_' not in hidden_word:
                print("Revealed...                  ", *hidden_word, sep=' ')
                game.status = 'success'
                break
            
            if guess not in word:
                count += 1 

            print(f"Tries left  ---->  {game.max_chances - count}", end='\n')
            print('\n')

    print(f"Game exited with {game.status}")
                


# Api key Reference - https://medium.com/@valerio.uberti23/a-beginners-guide-to-using-api-keys-in-fastapi-and-python-256fe284818d   