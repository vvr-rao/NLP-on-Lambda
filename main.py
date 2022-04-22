import json
import transformers
from transformers import AutoModel, AutoTokenizer
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader

def handler(event, context):
    #import tokenizer and bert-base-cased model
    local_path = '/bert-base-cased-LOCAL/'
    tokenizer = AutoTokenizer.from_pretrained(local_path)
    bert_model = AutoModel.from_pretrained(local_path) 
    
    #Define our model
    class SentimentClassifier(nn.Module):
        def __init__(self, n_classes):
            super(SentimentClassifier, self).__init__()
            self.bert = bert_model  #AutoModel.from_pretrained(local_path) 
            self.drop = nn.Dropout(p=0.3)
            self.out = nn.Linear(self.bert.config.hidden_size, n_classes)

        def forward(self, input_ids, attention_mask):
            returned = self.bert(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
            pooled_output = returned["pooler_output"]
            output = self.drop(pooled_output)
            return self.out(output)

    model = SentimentClassifier(3)

    #load the model state dict

    m = torch.load('/model/best_model_state_cpu.bin')
    model.load_state_dict(m)

    #read the input
            
    data = json.loads(json.dumps(event))
    payload = data['data']
    
    
    string1 = payload.replace('\d+', '') # remove digits
    string1 = string1.replace('[^\w\s]', '') # remove punctuation
    
    #make a prediction
    encoded_review = tokenizer.encode_plus(
        string1,
        max_length=30,
        add_special_tokens=True,
        return_token_type_ids=False,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt',
    )


    model.eval()
    class_names = ['Negative','Neutral','Positive']

    with torch.no_grad():
        input_ids = encoded_review['input_ids']
        attention_mask = encoded_review['attention_mask']
        
        output = model(input_ids, attention_mask)

        _, prediction = torch.max(output, dim=1)

    response = {"Input": payload, "Sentiment": class_names[prediction]}
    return response
