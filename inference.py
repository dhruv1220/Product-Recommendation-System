import torch
import numpy as np
from model import DotModel, load_model

def predict(user_id, item_id, model):
    user_id_tensor = torch.tensor([user_id])
    item_id_tensor = torch.tensor([item_id])
    with torch.no_grad():
        prediction = model(user_id_tensor, item_id_tensor)
    return prediction.item()
