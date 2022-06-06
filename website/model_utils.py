import torch 

import io, tokenize, re, os

import torch
import torch.nn as nn

from transformers import RobertaTokenizer, RobertaModel
  
class VectorizeData(object):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    
    def __call__(self, source):
        code = source
        tokenizer = self.tokenizer
        cls = tokenizer.cls_token
        sep = tokenizer.sep_token
        eos = tokenizer.eos_token
        pad = tokenizer.pad_token

        # Place the code into a form such that it will 
        # be tokenized by the CodeBERT tokenizer
        ss = list(map(lambda s : s.strip(), code.split("\n")))
        #print(ss)
        # Flatten the list. 
        #ss = [cls] + [item for sublist in ss for item in sublist]
        ss = cls + '\n'.join(ss)
        
        # Tokenize
        ss = tokenizer.encode_plus(ss, return_tensors='pt')

        # Pad
        _, x2 = ss['input_ids'].shape
        
        if x2 < 512:
            padding = torch.tensor([[1 for _ in range(512 - x2)]])

            ss['input_ids'] = torch.cat((ss['input_ids'], padding), dim=1).squeeze()
            padding = padding - 1
            ss['token_type_ids'] = torch.cat((ss['token_type_ids'], padding), dim=1).squeeze()
        else:
            ss['input_ids'] = ss['input_ids'][:, 0:512].squeeze()
            ss['token_type_ids'] = ss['token_type_ids'][:, 0:512].squeeze()

        return ss

class Preprocessor(object):
    def __init__(self, tokenizer_path='./codebert'):
        #super().__init__()
        tokenizer = RobertaTokenizer.from_pretrained(tokenizer_path)
        self.vectorizer = VectorizeData(tokenizer)
    
    def __call__(self, source):
        return self.vectorizer(source)['input_ids'].unsqueeze(dim=0)
        

# https://stackoverflow.com/a/62074206/9432116
def py_cleaner(source):
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        if token_type == tokenize.COMMENT:
            pass
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    out = '\n'.join(l for l in out.splitlines() if l.strip())
    return out

# Cleaner for C-like languages such as Java and JavaScript.
# I can't find the original stack-overflow post anymore, sorry.
def c_cleaner(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    final_string = re.sub(pattern, replacer, text)
    final_string = '\n'.join(l for l in final_string.splitlines() if l.strip())

    return final_string

def preprocess_code(source, ext):
    if ext == 'python':
        return py_cleaner(source)
    else:
        return c_cleaner(source)

def init_weights(m):
    if isinstance(m, nn.Linear):
        torch.nn.init.xavier_uniform_(m.weight)
        m.bias.data.fill_(0.01)

class Model(nn.Module):
    def __init__(self, codebert, input=393_216, hidden=None, labels=9, train_rate=1e-3):
        super().__init__()
        
        self.transformer = codebert

        layers = [self.transformer.embeddings, *self.transformer.encoder.layer[:9]]
        for layer in layers: #self.transformer.parameters():
            for param in layer.parameters():
                param.requires_grad = False
                
        self.train_rate = train_rate

        layers = [nn.Dropout(p=0.1), nn.Linear(768 * 512, 420), nn.BatchNorm1d(420), nn.ReLU()]

        self.hidden_is_none = hidden is None
        last = 420
        if hidden is not None:

            for i in hidden:
                layers.append(nn.Dropout(p=0.1))
                layers.append(nn.Linear(last, i)) 
                layers.append(nn.BatchNorm1d(420))
                layers.append(nn.ReLU())

                last = i
        layers.append(nn.Linear(last, labels)) 
        
        for layer in layers:
            init_weights(layer)

        self.ann = nn.Sequential(*layers)
        
    def forward(self, x):
        (out, mask) = self.transformer(x)
        out = torch.flatten(out, 1)
        return self.ann(out)

def initialize_model(filepath='model.pth'):
    codebert = RobertaModel.from_pretrained("./codebert")
    m = Model(codebert)
    
    m.load_state_dict(torch.load(filepath, map_location=torch.device('cpu')), strict=False)
    m.eval()
    torch.no_grad()
    return m

def get_names(probs):
    cols = ["quicksort", "mergesort", "selectionsort", "insertionsort", 
            "bubblesort", "linearsearch", "binarysearch", "linkedlist", "hashmap"]
    # Calculated automatically using Precision-Recall Curve
    thresholds = torch.tensor([0.477, 0.493, 0.65, 0.65, 0.649, 0.366, 0.455, 0.564, 0.6])

    predictions = (probs >= thresholds).squeeze()
    preds = [col for col, pred in zip(cols, predictions) if pred]
    return preds

def predict(model, x):
    y_hat = torch.sigmoid(model(x))
    return y_hat.squeeze()