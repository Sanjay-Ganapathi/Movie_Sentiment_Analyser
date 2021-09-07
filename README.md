# Movie Sentiment Analyser
### [Link](https://moviesenti.azurewebsites.net/)
![alt text](https://github.com/Sanjay-Ganapathi/Movie_Sentiment_Analyser/blob/main/img/front.png "front page")
![alt text](https://github.com/Sanjay-Ganapathi/Movie_Sentiment_Analyser/blob/main/img/bottom.png "bottom")
***

### *Containerized Dash app deployed on Azure*

Movie Sentiment Analyser that takes input as movie name, scrapes Rotten Tomatoes for user and critic reviews (60 each), then analyses the sentiment using Model trained and performs EDA 

---

### Model Description

Model : Bidirection LSTM <br/>
Embeddings : Pretrained Word2Vec Google News Corpus(Dim:300) <br/>
Training Data: [Sentiment140 dataset with 1.6 million tweets](https://www.kaggle.com/kazanova/sentiment140 "Dataset Link")
 
*Model Summary*:

![alt text](https://github.com/Sanjay-Ganapathi/Movie_Sentiment_Analyser/blob/main/img/model_summary.png "model_summary_image")


Accuracy : ~ 75% on test data <br/>
[Kaggle Notebook link](https://www.kaggle.com/ethanhunt1080/sentiment-analyzer "Descriptive notebook on Kaggle")

---
*Contents to be in app directory :*<br/>
  + app.py - Dash template of page.<br/>
  + scraper.py - Contains various scraper funtions to scrape Rotten Tomatoes.
  + utils.py - Contains functions to predict the score and sentiment of the given review
  + model.hdf - model file (Can be downloaded from Kaggle Notebook) 
  + tokens.pkl - token file in pickle format (Can be downloaded from Kaggle Notebook)
  <br/>
  
  + model_check.ipynb - ipynb file to check downloaded model
  + rotten_tomatoes_scraper.ipynb - ipynb file to check scraper functions
  ---
  
