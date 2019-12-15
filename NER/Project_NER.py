import nltk
import argparse
from nltk import FreqDist
import pandas as pd
import matplotlib.pyplot as plt

def processNER(  processed_content  ):

    entities = {}
    nerSet = set()

    for entry in processed_content:
        entry_value = entry[0]
        entry_type = entry[1]
        nerSet.add(entry_type)
        if entry_type in entities.keys():
            entities[entry_type].append( entry_value )
        else:
            entities[entry_type] = list()
            entities[entry_type].append( entry_value )

    print (nerSet)
    return entities

def make_plot(entities, title_prefix):

    for entity_type in entities:

        f_dist = FreqDist(  entities[entity_type]  )
        print(entity_type)
        print(f_dist.most_common(20))

        df = pd.DataFrame( f_dist.most_common(20) )
        df = df.rename(columns={0: entity_type, 1: 'count'})
        fig = plt.figure()
        df.plot(x=entity_type,y='count',kind='bar',legend=False,title=title_prefix+'_'+entity_type)
        plt.xlabel(entity_type)
        plt.ylabel('count')
        plt.tight_layout()
        plt.savefig(title_prefix+'_'+entity_type+'.png')
        plt.close(fig)

def main():

    from nltk.tag import StanfordNERTagger as snt
    stg = snt('/home/hwdata/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz','/home/hwdata/stanford-ner-2018-10-16/stanford-ner.jar', encoding='utf-8')
    
    # get input arguments
    parser = argparse.ArgumentParser(description='NER tool')
    parser.add_argument('filename', type=str, help='filename')
    args = parser.parse_args()
    f = open(args.filename,"r")
    rawContent = f.read()

    from pycorenlp import StanfordCoreNLP
    nlp = StanfordCoreNLP('http://localhost:64000')

    # #Offline StanfordNERTagger Tagger
    # print( '-------------------------')
    # print( 'Offline StanfordNERTagger' )
    # processed_content = stg.tag( nltk.word_tokenize(rawContent) )
    # entities = processNER(processed_content)

    # StanfordCoreNLP server 
    print( '-------------------------')
    print( 'StanfordCoreNLP' )

    result = list()
    sents = nltk.sent_tokenize(rawContent)
    #We need to feed to NLP server one sentence at a time or else it will time out
    for sent in sents:
        result.append(nlp.annotate(sent, properties={ 'annotators': 'ner', 'outputFormat': 'json','timeout ': 3000} ))
    
    ner = list()
    for i in range(  len(sents)  ):
        for word in result[i]['sentences'][0]['tokens']:
            ner.append( (word['word'],word['ner']) )

    entities = processNER(ner)
    
    # plot
    make_plot(entities, args.filename[:-4])
    
if __name__ == '__main__': 
    main()