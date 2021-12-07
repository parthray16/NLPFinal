import pandas as pd
import dateparser
from nltk.corpus import stopwords
import re
import datetime
import pickle
from geotext import GeoText
import spacy
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


nlp = spacy.load("en_core_web_sm")

c = open('countries.txt','r')
countryList = []
for x in c.readlines():
  countryList.append(x.strip())
c.close()


def get_dates(text):
    char_nums = []
    text_bubbles = []
    dates = []
    text += 'dum junk'
    match = re.finditer("\d+/\d+/\d",text)
    for m in match:
        date_str = text[m.start():m.end()]
        datet = dateparser.parse(date_str,settings={'STRICT_PARSING': True})
        if datet:
            char_nums.append(m.start())
            start=max(m.start()-40,0)
            end = min(m.end()+15,len(text))
            text_bubbles.append(re.sub('\s+',' ',text[start:end]))
            dates.append(datet.replace(tzinfo=None))
    match = re.finditer("jan|feb|mar|apr|may|jun|jul|aug|sep|nov|dec",text)
    for m in match:
        date_str = text[m.start()-10:m.end()+15]
        date_str = re.sub('-\s*\d+|,|\s+',' ',date_str)
        toks = re.split('\s+',date_str)
        datet=None
        for i in range(len(toks)-3):
            datet = dateparser.parse(' '.join(toks[i:i+3]),settings={'STRICT_PARSING': True})
            part_date = None
            if datet:
                break
            else:
                datet = dateparser.parse(' '.join(toks[i:i+2]))
        if datet:
            char_nums.append(m.start())
            start=max(m.start()-40,0)
            end = min(m.end()+15,len(text))
            text_bubbles.append(re.sub('\s+',' ',text[start:end]))
            dates.append(datet.replace(tzinfo=None))
    df_dates = pd.DataFrame()
    df_dates['date']=dates
    xgb_classifier = pickle.load(open('pkl_models/xgb_classifier2.pkl', "rb"))
    tfidfvec = pickle.load(open('pkl_models/tfidfvec2.pkl', "rb"))

    if len(dates)==0:
        return [None,None,None]
    df_dates['text']=text_bubbles
    tfidf_wm = tfidfvec.transform(text_bubbles)
    tfidf_tokens = tfidfvec.get_feature_names_out()
    df_tfidfvect = pd.DataFrame(data = tfidf_wm.toarray(),columns = tfidf_tokens)
    labels = xgb_classifier.predict(df_tfidfvect)
    probas = xgb_classifier.predict_proba(df_tfidfvect)

    df_dates['label']=labels
    df_dates['prob'] = [max(p) for p in probas]
    df_dates.drop_duplicates(inplace=True)
    df_dates = df_dates.loc[df_dates.groupby('label')['prob'].idxmax()]
    conf_date = df_dates[df_dates['label']=='conf_date']['date'].values
    if conf_date.size>0:
        conf_date=datetime.datetime.utcfromtimestamp(conf_date[0].tolist()/1e9).strftime("%A, %d %b %Y")
    else:
        conf_date = None
    sub_date = df_dates[df_dates['label']=='sub_date']['date'].values
    if sub_date.size>0:
        sub_date=datetime.datetime.utcfromtimestamp(sub_date[0].tolist()/1e9).strftime("%A, %d %b %Y")
    else:
        sub_date = None
    notif_date = df_dates[df_dates['label']=='notif_date']['date'].values
    if notif_date.size>0:
        notif_date=datetime.datetime.utcfromtimestamp(notif_date[0].tolist()/1e9).strftime("%A, %d %b %Y")
    else:
        notif_date = None
    
    return [conf_date,
            sub_date,
            notif_date]


def get_location(un_doc):
    doc = nlp(un_doc)
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


def get_consecutive_words(sent):
    stop_words = stopwords.words('english')
    months = {'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'}
    sent = sent.replace('-', '')
    sent = sent.replace('/', ' ')
    words = word_tokenize(sent)
    phrases = []
    current_phrase = []
    for word in words:
        if bool(re.match("[A-Z]+'\d+", word)):
            if len(current_phrase) > 0:
                # remove extra stopwords
                i = len(current_phrase) - 1
                while (current_phrase[i] in stop_words):
                    del current_phrase[i]
                    i -= 1
                phrases.append(' '.join(current_phrase))
                current_phrase = []
            phrases.append(word)
        else:
            if (bool(re.match(r'\w*[A-Z]\w*', word)) or bool(re.search(r'\d', word))) and word.lower() not in months:
                current_phrase.append(word)
            else:
                if word in stop_words and len(current_phrase) > 0:
                    current_phrase.append(word)
                else:
                    if len(current_phrase) > 0:
                        # remove extra stopwords
                        i = len(current_phrase) - 1
                        while (current_phrase[i] in stop_words):
                            del current_phrase[i]
                            i -= 1
                    phrases.append(' '.join(current_phrase))
                    current_phrase = []
    better_phrases = []
    for phrase in phrases:
        if len(phrase.split()) > 1:
            better_phrases.append(phrase)
    if len(better_phrases) == 0:
        return phrases
    return better_phrases



def select_conference(phrases):
  if len(phrases) == 0:
    return ""
  for phrase in phrases:
    if 'conference' in phrase.lower() or 'confrence' in phrase.lower():
      return phrase
  for phrase in phrases:
    if 'conf' in phrase.lower():
      return phrase
  for phrase in phrases:
    if 'event' in phrase.lower():
      return phrase
  for phrase in phrases:
    if 'congress' in phrase.lower():
      return phrase
  return max(phrases, key=len)




def get_name(email_text):
    lemmatizer = WordNetLemmatizer()
    clf = pickle.load(open('pkl_models/catboost_sent_clf.pkl', "rb"))
    vectorizer = pickle.load(open('pkl_models/tfidf_sent_vecs.pkl', "rb"))
    columns = vectorizer.get_feature_names_out()
    sents = sent_tokenize(email_text)
    lemmatized_sents = []
    for sent in sents:
        words = [lemmatizer.lemmatize(w) for w in sent.split()]
        sent = " ".join(words)
        lemmatized_sents.append(sent)
    sents_wm = vectorizer.transform(lemmatized_sents)
    stop_i = 0
    for i in range(len(columns)):
        colname = columns[i]
        if colname[0] == 'a':
            stop_i = i
            break
    df_sents_vecs = pd.DataFrame(sents_wm.toarray(), columns=columns).iloc[:, stop_i:]
    predictions = clf.predict_proba(df_sents_vecs)
    df_predictions = pd.DataFrame(predictions, columns=['not_in_sent', 'in_sent'])
    df_predictions['compound'] = df_predictions['in_sent'] - df_predictions['not_in_sent']
    best = list(df_predictions['compound'].sort_values(ascending=False).index)[0]
    best_sent = sents[best]
    pred_name = select_conference(get_consecutive_words(best_sent))
    return pred_name