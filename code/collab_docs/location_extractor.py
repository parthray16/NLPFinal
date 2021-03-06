# -*- coding: utf-8 -*-
"""Location_Extractor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w9wlMR8V2O90ETYS-18uIoidZhKyj-ou
"""

from google.colab import drive
drive.mount('/content/drive')

#!pip install tqdm
#!pip install eml_parser

import pandas as pd
import numpy as np
import os
import eml_parser
from tqdm.notebook import tqdm
import re
from bs4 import BeautifulSoup
import email

# Commented out IPython magic to ensure Python compatibility.
# %cd '/content/drive/MyDrive/FinalProject/'

files = os.listdir('conf_emails_numbered')
files.sort()

df_annot = pd.read_csv('combined_annotations.csv')
df_annot.head()

"""#Spacy"""

# !pip install spacy
# !python -m spacy download en_core_web_sm
!pip install geotext

import spacy

nlp = spacy.load("en_core_web_sm")

gpe = [] # countries, cities, states
loc = [] # non gpe locations, mountain ranges, bodies of water

# doc = nlp(open('subtitle.txt').read())
for ent in doc.ents:
    if (ent.label_ == 'GPE'):
        gpe.append(ent.text)
    elif (ent.label_ == 'LOC'):
        loc.append(ent.text)

cities = []
countries = []
other_places = []
import wikipedia
for text in gpe:
    summary = str(wikipedia.summary(text))
    if ('city' in summary):
        cities.append(text)
    elif ('country' in summary):
        countries.append(text)
    else:
        other_places.append(text)


for text in loc:
    other_places.append(text)

def pretty_print(path):
  with open(path, 'rb') as fhdl:
      raw_email = fhdl.read()
      msg = email.message_from_bytes(raw_email)
      email_body=''
      for part in msg.walk():
          if part.get_content_type().find('text') != -1:
              email_body = part.get_payload(None, True)
      soup = BeautifulSoup(email_body, 'html')
      
      return re.sub('[^A-Z|^a-z|^\s|^,]',' ',soup.text)

from geotext import GeoText

"""USE THIS"""

def locations(doc, un_doc):
  gpe = []
  countries = []
  places = GeoText(un_doc)
  cities = places.cities
  for token in doc.ents:
    if token.label_ == 'GPE':
      gpe.append(token.text)
  for token in doc:
    if token.text.isupper() and token.text in countryList and token.text not in gpe:
      gpe.append(token.text)
  for x in gpe:
    if x in countryList:
      countries.append(x)
  inter = []
  for x in gpe:
    if x in cities:
      inter.append(x)
  gpe = inter
  if len(countries) == 0:
    countries = places.countries
  if len(countries) == 0 and len(gpe) == 0:
    return ""
  elif len(countries) > 0 and len(gpe) == 0:
      return countries[0]
  elif len(countries) == 0 and len(gpe) > 0:
    return gpe[0]
  else:
    return gpe[0] +", " + countries[0]

import email
locations_pred = []
c = open('countries.txt','r')
countryList = []
for x in c.readlines():
  countryList.append(x.strip())
for x in tqdm(range(0,len(files))) :
  doc = pretty_print('conf_emails_numbered/'+files[x])
  locations_pred.append(locations(nlp(doc),doc))

locations_pred

loc_actual = []
loc_pred=[]
# len(files)
for x in range(0,len(files)):
  labels = df_annot[df_annot['ID']==x]
  if len(labels)==0:
    continue
  loc_pred.append(locations_pred[x])
  if labels.iloc[0]['Event location'] is np.nan:
    loc_actual.append("")
  else:
    loc_actual.append(labels.iloc[0]['Event location'])

score = 0
hit = 0
miss = 0
partial = 0

for x in range(0,len(loc_actual)):
  if len(loc_actual[x]) > 0 and len(loc_pred) > 0:
    a_split = loc_actual[x].split(",")
    p_split = loc_pred[x].split(",")
    if a_split == p_split:
      hit += 1
    sum=0
    score+=(len(set(a_split).intersection(set(p_split)))/(min(len(a_split),len(p_split)))*2)
    if len(set(a_split).intersection(set(p_split))):
      miss+=1
hit,score,miss

score/(len(loc_actual)*2)