from flask import Flask, request, jsonify
import torch
from model import load_model
import pandas as pd

app = Flask(__name__)

# Load preprocessed data and model
cdata = pd.read_csv('preprocessed_data.csv')
num_users = cdata['reviewerID'].nunique()
num_items = cdata['asin_id'].nunique()
model = load_model(num_users, num_items, 'model_cf.pt')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    user_id = int(data['user_id'])
    item_id = int(data['item_id'])
    prediction = model(torch.tensor([user_id]), torch.tensor([item_id]))
    return jsonify({'prediction': prediction.item()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
