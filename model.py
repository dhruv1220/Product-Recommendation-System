import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd

class ScaledEmbedding(nn.Embedding):
    def reset_parameters(self):
        self.weight.data.normal_(0, 1.0 / self.embedding_dim)
        if self.padding_idx is not None:
            self.weight.data[self.padding_idx].fill_(0.0)

class ZeroEmbedding(nn.Embedding):
    def reset_parameters(self):
        self.weight.data.zero_()
        if self.padding_idx is not None:
            self.weight.data[self.padding_idx].fill_(0.0)

class DotModel(nn.Module):
    def __init__(self, num_users, num_items, embedding_dim=32):
        super(DotModel, self).__init__()
        self.user_embeddings = ScaledEmbedding(num_users, embedding_dim)
        self.item_embeddings = ScaledEmbedding(num_items, embedding_dim)
        self.user_biases = ZeroEmbedding(num_users, 1)
        self.item_biases = ZeroEmbedding(num_items, 1)

    def forward(self, user_ids, item_ids):
        user_embedding = self.user_embeddings(user_ids)
        item_embedding = self.item_embeddings(item_ids)
        user_bias = self.user_biases(user_ids).squeeze()
        item_bias = self.item_biases(item_ids).squeeze()
        dot = torch.mul(user_embedding, item_embedding).sum(1)
        res = dot + user_bias + item_bias
        return res

def train_model(cdata, embedding_dim=32, n_iter=10, learning_rate=0.01, l2=1e-8):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    num_users = cdata['reviewerID'].nunique()
    num_items = cdata['asin_id'].nunique()

    model = DotModel(num_users, num_items, embedding_dim).to(device)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=l2)
    loss_func = nn.MSELoss()

    train_data, val_data = train_test_split(cdata, test_size=0.1, random_state=42)
    train_users = torch.tensor(train_data['reviewerID'].values).to(device)
    train_items = torch.tensor(train_data['asin_id'].values).to(device)
    train_ratings = torch.tensor(train_data['overall'].values, dtype=torch.float32).to(device)

    val_users = torch.tensor(val_data['reviewerID'].values).to(device)
    val_items = torch.tensor(val_data['asin_id'].values).to(device)
    val_ratings = torch.tensor(val_data['overall'].values, dtype=torch.float32).to(device)

    for epoch in range(n_iter):
        model.train()
        optimizer.zero_grad()
        predictions = model(train_users, train_items)
        loss = loss_func(predictions, train_ratings)
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            val_predictions = model(val_users, val_items)
            val_loss = loss_func(val_predictions, val_ratings)
        print(f'Epoch {epoch+1}/{n_iter}, Training Loss: {loss.item()}, Validation Loss: {val_loss.item()}')

    torch.save(model.state_dict(), 'model_cf.pt')

def load_model(num_users, num_items, model_path='model_cf.pt', embedding_dim=32):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = DotModel(num_users, num_items, embedding_dim).to(device)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

cdata = pd.read_csv('preprocessed_data.csv')
train_model(cdata)