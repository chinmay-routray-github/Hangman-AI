
import torch
import player_model 

class Prediction:

    def __init__(self):
        self.n_vocab = 26
        self.extra = 1
        self.all_chars = [chr(97+i) for i in range(self.n_vocab)]
        char_idx = {k : i for i,k in enumerate(self.all_chars)}
        char_idx['_'] = 26
        self.char_to_id = char_idx
        self.id_to_char = {v : k for k, v in self.char_to_id.items()}
        

    def guess(self, word, guess_list): # word input example: "_ p p _ e "
        
        # clean the word so that we strip away the space characters and lowercase them
        word = word.strip().lower()
        
        # encoding the word
        encoded_word = torch.zeros(len(word), self.n_vocab + self.extra)
        for i, ch in enumerate(word):
            encoded_word[i][self.char_to_id[ch]] = 1
        
        encoded_word = encoded_word.unsqueeze(0)
        
        # encoding the guess_list
        vec = torch.zeros(1, self.n_vocab)
        if len(guess_list) > 0:
            for x in guess_list:
                vec[0][self.char_to_id[x]] = 1

        encoded_list = vec.unsqueeze(0)

        # loading the Trained model
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        data = torch.load(r"C:\Users\chinmay\Downloads\Hangman_player_trained_1000_epoch.pth", map_location=torch.device('cpu'))
        model_state = data['model_state']
        model = player_model.RNN().to(device)
        model.load_state_dict(model_state)

        # word length tensor
        w_len = torch.tensor([len(word)])

        # predicting
        pred = torch.argsort(torch.softmax(model(encoded_word, encoded_list, w_len), 1),-1, descending=True).squeeze(0)
        l = [self.id_to_char[x.item()] for x in pred]
        
        for p in l:
            if(p not in guess_list):
                return p