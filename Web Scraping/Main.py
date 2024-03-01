import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')

import nltk
nltk.download('punkt')

#Read data
df=pd.read_csv('C:/Users/Naman Sharma/Desktop/Folders/ML Projects/Web Scraping/Reviews.csv/Reviews.csv')
example=df['Text'][50]
print(example)
nltk.word_tokenize(example)