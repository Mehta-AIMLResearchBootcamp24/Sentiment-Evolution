# -*- coding: utf-8 -*-
"""Final project AI + Politics.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1l74VhyVv1zPJalLkgVDaR7dhTDiHdt_i
"""

!pip install pandas==1.1.5
!pip install fasttext==0.9.2

from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
import google.generativeai as genai
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from gensim.models import FastText
#import fasttext
import tempfile

def split_string_into_groups(s: str, n: int) -> list[str]:
    sentences = s.split('.')
    grouped_sentences = [sentences[i:i + n] for i in range(0, len(sentences), n)]
    return [' '.join(group) for group in grouped_sentences if group]
def single_value_mean(x):
  if len(x) == 1:
    return x.iloc[0]
  else:
    return x.mean()

# @title Default title text
API_KEY = "AIzaSyCkSPdEzfWRAx8ANfezLnd0P5dS0O8jtpw"
text = input("text: ")
def split_string_into_groups(s: str, n: int) -> list[str]:
    sentences = s.split('.')
    grouped_sentences = [sentences[i:i + n] for i in range(0, len(sentences), n)]
    return [' '.join(group) for group in grouped_sentences if group]
grouped_result = split_string_into_groups(text, 4)
print(grouped_result)
for i in grouped_result:
  genai.configure(api_key=API_KEY)
  #https://ai.google.dev/api/python/google/generativeai/GenerativeModel
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
  #  https://ai.google.dev/gemini-api/docs/safety-settings
  )

  chat_session = model.start_chat(
    history=[
    ]
  )
  response = chat_session.send_message(f'given the following text{{{i}}} rate the text on positivity from -1 (very negative) to 1 (very positive). only give the rating as your answer')
  print(i)
  print(response.text)

filepath = '/content/AI Politics - Sheet1 (3).csv'
df = pd.read_csv(filepath)
df = df.dropna(how='any')
df.head()

# @title Model 1
data = pd.read_csv('/content/AI Politics - Sheet1 (3).csv')
data = data.iloc[:, :2]
data.dropna(inplace=True)
X = data['speech ']
y = data['Sentiment Score']
ohe = OneHotEncoder()
X_encoded = ohe.fit_transform(X.values.reshape(-1, 1))
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# @title  Model 1
text_input = input("Enter a text: ")
text_groups = split_string_into_groups(text_input, 4)
for j in text_groups:
  new_text_encoded = ohe.transform(np.reshape(j, (1, 1)))
  predicted_value = regressor.predict(new_text_encoded)
  print(f"Predicted value for '{j}': {predicted_value[0]:.2f}")

# @title Model 2
data = pd.read_csv('/content/AI Politics - Sheet1 (3).csv')
data = data.iloc[:, :2]
data.dropna(inplace=True)
X = data['speech ']
y = data['Sentiment Score']
with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
    for j in X:
        temp_file.write(j + '\n')
    temp_filename = temp_file.name
model = fasttext.train_unsupervised(input=temp_file.name, model='skipgram', minCount=1)
X_encoded = []
for sentence in X:
    sentence_vector = sum(model[word] for word in sentence.split() if word in model)
    X_encoded.append(sentence_vector)
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
import os
os.remove(temp_filename)

# @title Model 2
new_text_input = input("Enter a text: ")
text_groups = split_string_into_groups(new_text_input, 4)
for j in text_groups:
  encoded_input = sum(model[word] for word in j.split() if word in model)
  predicted_score = regressor.predict([encoded_input])
  print(f"{predicted_score[0]:.2f}")

data = pd.read_csv('/content/AI Politics - Sheet1 (3).csv')
data = data.iloc[:, :2]
data.dropna(inplace=True)
X = data['speech ']
y = data['Sentiment Score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), stop_words='english')
Xa = vectorizer.fit_transform(X_train)
Xb = vectorizer.transform(X_test)
model = LinearRegression()
model.fit(Xa, y_train)
y_pred = model.predict(Xb)
mse = mean_squared_error(y_test, (y_pred))
print(f"Mean Squared Error: {mse:.2f}")

j = 1
while j == 1:

  if j == 0:
    break
  text = input("Enter a text: ")
  text = split_string_into_groups(text, 4)
  li = list()
  for j in text:
    new_text = vectorizer.transform([j])
    predicted_score = model.predict(new_text)
    li.append(predicted_score)
    print(j)
  import matplotlib.pyplot as plt
  color = input("Enter a color: ")
  plt.plot(li, color)
  j = int(input('continue say 1: '))
plt.ylabel('Sentimen Score')
plt.show()

file = '/content/AI Politics - Sheet1 (7).csv'
data = pd.read_csv(file, na_filter=False)
data = data.drop(['Speaker', 'Date'], axis=1)
X = data['speech ']
y = data['Election Date']
y = pd.to_datetime(y, errors='coerce')
Z = list()
for j in X:
  new_text = vectorizer.transform([j])
  Z.append(float(model.predict(new_text)))
df = pd.DataFrame()
df['Z'] = Z
df['y'] = y
df_averaged = df.groupby('y')['Z'].first().reset_index()
df_averaged['year'] = df_averaged['y'].dt.year
df_averaged = df_averaged.sort_values('year')
df_averaged = df_averaged.drop('y', axis=1)
df_averaged

from matplotlib import pyplot as plt
import seaborn as sns
def _plot_series(series, series_name, series_index=0):
  palette = list(sns.palettes.mpl_palette('Dark2'))
  xs = series['year']
  ys = series['Z']

  plt.plot(xs, ys, label=series_name, color=palette[series_index % len(palette)])

fig, ax = plt.subplots(figsize=(10, 5.2), layout='constrained')
df_sorted = df_averaged.sort_values('year', ascending=True)
_plot_series(df_sorted, '')
sns.despine(fig=fig, ax=ax)
plt.xlabel('year')
plt.ylim(-1, 1)
_ = plt.ylabel('Sentiment Score')