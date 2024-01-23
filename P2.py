import re
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
data = pd.read_csv('customer_support_messages.csv')

# Remove unwanted characters and words
data['clean_text'] = data['text'].apply(lambda x: re.sub(r'[^\w\s]','',x))
data['clean_text'] = data['clean_text'].apply(lambda x: x.lower())
data['clean_text'] = data['clean_text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwords.words('english'))]))

# Tokenize the text
data['tokenized_text'] = data['clean_text'].apply(lambda x: word_tokenize(x))

# Load the pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(data.category.unique()))

# Define the data and label arrays
X = data.tokenized_text.values
y = data.category.values

# Define the training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10
)

# Define the trainer and train the model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=X,
    eval_dataset=y
)

trainer.train()