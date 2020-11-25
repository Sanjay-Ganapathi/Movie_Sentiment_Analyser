from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import plotly.graph_objects as go


stopwords = stopwords.words('english')

model = load_model('model.hdf')
tokens = pickle.load(open('tokens.pkl','rb'))

def preprocess(text):
    tokens = []
    for token in text.split():
        if token not in stopwords:
            tokens.append(token)
    return ' '.join(tokens)


def decode_sentiment(score):
    label = None
    if score <= 0.4:
        label = 'Negative'
    elif score >= 0.7:
        label = 'Positive'
    else:
        label = 'Neutral'
    
    return label

max_length = 20
trunc_type = 'post'
padd_type = 'post'

def predict(text):
    x_test = pad_sequences(tokens.texts_to_sequences([text]), maxlen=max_length,padding=padd_type,truncating=trunc_type)
    score = model.predict([x_test])[0]
    
    label = decode_sentiment(score)

    return {"label": label, "score": round(float(score),3)} 

#print(predict('i Hate to tell you this but you suck'))

def labels_list(lst):
    labels = [predict(preprocess(i))['label'] for i in lst]
    return labels

def scores_list(lst):
    scores = [predict(preprocess(i))['score'] for i in lst]
    return scores


