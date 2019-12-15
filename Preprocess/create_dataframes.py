import nltk
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
import string
import pandas as pd

def text_to_frame(filename):
    text = open(filename,'r').read()

    compname = filename.split('_')[0]
    para_list = text.splitlines()    
    text_frame = pd.DataFrame(columns=['text_type','speaker_name','speaker_affiliation','speaker_title','text_raw','text_tokens'])

    section_marker = 0
    text_type = ''
    speaker_name = ''
    speaker_affiliation = ''
    speaker_title = ''

    for p in para_list:
  
        t = word_tokenize(p)
    
        dash_list = []
        for i in range(len(t)):
            if t[i] == '--': dash_list.append(i)
        if len(dash_list) > 0:
            if dash_list[0] > 5: dash_list = []
        if len(dash_list) > 0:               
            if len(t) > 20: dash_list = []
    
        if p == 'Questions and Answers:':
            section_marker = 1
            text_type = ''
            speaker_name = ''
            speaker_affiliation = ''
            speaker_title = ''
        elif p == 'Operator':
            section_marker = 1
            text_type = ''
            speaker_name = p
            speaker_affiliation = ''
            speaker_title = ''   
        elif p == 'Unidentified Participant':
            section_marker = 1
            text_type = 'question'
            speaker_name = p
            speaker_affiliation = ''
            speaker_title = ''  
        elif len(dash_list) == 1:
            if section_marker == 0: text_type = 'general'
            else: text_type = 'answer'
            speaker_affiliation = compname
            speaker_name = ''
            speaker_title = ''
            for i in range(dash_list[0]):
                speaker_name = speaker_name + t[i] + ' '
            for j in range(dash_list[0]+1,len(t)):
                speaker_title = speaker_title + t[j] + ' '
        elif len(dash_list) == 2:
            if section_marker == 0: text_type = '?'
            else: text_type = 'question'
            speaker_name = ''
            speaker_affiliation = ''
            speaker_title = ''
            for i in range(dash_list[0]):
                speaker_name = speaker_name + t[i] + ' '
            for j in range(dash_list[0]+1,dash_list[1]):
                speaker_affiliation = speaker_affiliation + t[j] + ' '
            for k in range(dash_list[1]+1,len(t)):
                speaker_title = speaker_title + t[k] + ' '
        elif len(t) > 0:
            text_d = {'text_type':text_type,'speaker_name':speaker_name,'speaker_affiliation':speaker_affiliation,
                  'speaker_title':speaker_title,'text_raw':p,'text_tokens':t}
            text_frame = text_frame.append(text_d,ignore_index=True)
    return text_frame

aapl_2019_Q4_frame = text_to_frame('Transcripts/AAPL_2019_Q4.txt')
jnj_2019_Q3_frame = text_to_frame('Transcripts/JNJ_2019_Q3.txt')
jpm_2019_Q3_frame = text_to_frame('Transcripts/JPM_2019_Q3.txt')
msft_2020_Q1_frame = text_to_frame('Transcripts/MSFT_2020_Q1.txt')
wmt_2019_Q4_frame = text_to_frame('Transcripts/WMT_2019_Q4.txt')

print(aapl_2019_Q4_frame['text_type'].value_counts())
print(aapl_2019_Q4_frame['speaker_name'].value_counts())
print(aapl_2019_Q4_frame['speaker_affiliation'].value_counts())
print(aapl_2019_Q4_frame['speaker_title'].value_counts())

print(jnj_2019_Q3_frame['text_type'].value_counts())
print(jnj_2019_Q3_frame['speaker_name'].value_counts())
print(jnj_2019_Q3_frame['speaker_affiliation'].value_counts())
print(jnj_2019_Q3_frame['speaker_title'].value_counts())

print(jpm_2019_Q3_frame['text_type'].value_counts())
print(jpm_2019_Q3_frame['speaker_name'].value_counts())
print(jpm_2019_Q3_frame['speaker_affiliation'].value_counts())
print(jpm_2019_Q3_frame['speaker_title'].value_counts())

print(msft_2020_Q1_frame['text_type'].value_counts())
print(msft_2020_Q1_frame['speaker_name'].value_counts())
print(msft_2020_Q1_frame['speaker_affiliation'].value_counts())
print(msft_2020_Q1_frame['speaker_title'].value_counts())

print(wmt_2019_Q4_frame['text_type'].value_counts())
print(wmt_2019_Q4_frame['speaker_name'].value_counts())
print(wmt_2019_Q4_frame['speaker_affiliation'].value_counts())
print(wmt_2019_Q4_frame['speaker_title'].value_counts())







