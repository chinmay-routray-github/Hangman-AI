
import torch
import torch.nn as nn

class RNN(nn.Module):
    
    n_vocab, extra = 26, 1
    num_layers = 2
    hidden_size = 512

    def __init__(self):
        super(RNN, self).__init__()

        # for LSTM layer
        self.rnn_name = 'LSTM'
        self.input_dim = RNN.n_vocab + RNN.extra      # 27
        self.hidden_dim = RNN.hidden_size         # 512
        self.num_layers = RNN.num_layers          # 2
        self.output_dim = RNN.n_vocab             # 26

        # for linear layer after LSTM 
        in_features = 256 + self.hidden_dim*2      # 256 + 512*2 = 1280
        mid_features = 256

        self.linear1_out = nn.Linear(in_features, mid_features)
        self.relu = nn.ReLU()
        self.linear2_out = nn.Linear(mid_features, self.output_dim)

        self.miss_linear = nn.Linear(RNN.n_vocab, 256)

        # setting up the LSTM
        self.rnn = nn.LSTM(input_size = self.input_dim, hidden_size = self.hidden_dim, 
                           num_layers = self.num_layers, dropout = 0.3, bidirectional = True, 
                           batch_first = True)
        
    
    # forward propagation
    def forward(self, x_in, wr_guess, x_lens):

        batch, seq_len, input_size = x_in.size()
        # pack the padded sequence
        x = torch.nn.utils.rnn.pack_padded_sequence(x_in, x_lens, batch_first=True, enforce_sorted=False)

        # run through RNN and collect hidden state                            # x - (batch x max_len x 27)
        out, (hidden, c_n) = self.rnn(x)
        
        hidden = hidden.view(self.num_layers, 2, -1, self.hidden_dim)         # (2, 2, -1, 512)
        hidden = hidden[-1]

        hidden = hidden.permute(1, 0, 2)

        hidden = hidden.contiguous().view(hidden.shape[0], -1)

        # pass wrong guesses through miss_linear layer
        wr_guess = self.miss_linear(wr_guess).squeeze(1)                                 # wr_guess - (1 x 256)

        # print(hidden.shape, wr_guess.shape)
        # concatenate wrong guesses and hidden state
        concatenated = torch.cat((hidden, wr_guess), dim=1)

        # predict
        return self.linear2_out(self.relu(self.linear1_out(concatenated)))
