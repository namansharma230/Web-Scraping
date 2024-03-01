
import openpyxl

workbook = openpyxl.load_workbook(r'C:\Users\Naman Sharma\Desktop\ML Projects\Web Scraping\Input.xlsx')

worksheet = workbook.active

urls = []
for row in worksheet.iter_rows():
    
    for cell in row:
        if cell.hyperlink:
            hyperlink_url = cell.hyperlink.target
            urls.append(hyperlink_url)

# with open(r'C:\Users\Naman Sharma\Desktop\ML Projects\Web Scraping\URL_ID.txt', 'w') as file:
#     for url in urls:
#         file.write(url + '\n')
from bs4 import BeautifulSoup
import json
import numpy as np
import requests
from requests.models import MissingSchema
import spacy
import trafilatura
data = {}

for url in urls:
    # 1. Obtain the response:
    resp = requests.get(url)
    
    # 2. If the response content is 200 - Status Ok, Save The HTML Content:
    if resp.status_code == 200:
        data[url] = resp.text

def beautifulsoup_extract(response_content):
    soup= BeautifulSoup(response_content, 'html.parser')
    texy =soup.find_all(text=True)

    cleaned=''
    blacklist = [
        '[document]',
        'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', 'style']
    for item in text:
        if item.parent.name not in blacklist:
            cleaned+='{}'.format(item)

    cleaned=cleaned.replace('\t', '')
    return cleaned.strip()

def extract_text_from_single_webpage(url):
    downloaded_url = trafilatura.fetch_url(url)
    try:
        a= trafilatura.extract(downloaded_url, json_output=True, with_metadata=True, include_comments=False, 
                               date_extraction_params={'extensive_search':True, 'original_data': True})
        
    except AttributeError:
        a = trafilatura.extract(downloaded_url, json_output=True, with_metadata=True,
                            date_extraction_params={'extensive_search': True, 'original_date': True})
    
    if a:
        json_output=json.loads(a)
        return json_output['text']
    else:
        try:
            resp=requests.get(url)
            if resp.status_code==200:
                return beautifulsoup_extract(resp.content)
            else:
                return np.nan
        except MissingSchema:
            return np.nan

urls=urls+['fake_url']
text= [extract_text_from_single_webpage(url) for url in urls]
cleaned_textual_content = [text for text in text if str(text) != 'nan']
nlp = spacy.load("en_core_web_sm")
for cleaned_text in cleaned_textual_content:
    # 1. Create an NLP document with Spacy:
    doc = nlp(cleaned_text)
    # 2. Spacy has tokenised the text content:
    print(f"This is a spacy token: {doc[0]}")
    # 3. Extracting the word count per text document:
    print(f"The estimated word count for this document is: {len(doc)}.")
    # 4. Extracting the number of sentences:
    print(f"The estimated number of sentences in the document is: {len(list(doc.sents))}")
    print('\n')
# print(text[1])
# print(text[-1:])