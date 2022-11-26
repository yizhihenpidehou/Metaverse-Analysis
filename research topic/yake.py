import pke
from nltk.corpus import stopwords
from collections import defaultdict


for i in range(1,2):
    abstract_file=open("tmp_abstract"+str(i)+".txt", 'r')
    abstract_str=abstract_file.read()
    abstract_lst=abstract_str.split('---------------------------------\n')
    print(len(abstract_lst))
    # print("abs:",abstract_lst)
    # total_str=""
    # for a in abstract_lst:
    #     total_str+=a
    extractor=pke.unsupervised.YAKE()
    keyPhraseDict=defaultdict(int)
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'use', 'present', 'play', 'can','find','used','uses','using','design','paper','time','two'
                           ,'however','also','many','well','new','based','user','users','data','method','information','propose',
                           'provide','research','approach','problem','proposed','result','results','need','way','show',
                           'help','different','study','process','e g','within','become','order','finally','make','related',
                           'one','number','may','demostrate','methods','set','improve'])
    for a in abstract_lst:
        # print('a:',a)
        extractor.load_document(input=a,language="en",stoplist=stop_words,normalization=None)

        extractor.candidate_selection(n=3)
        window=2
        use_stems=True
        extractor.candidate_weighting(window=window,use_stems=use_stems)
        threshold=0.8
        keyphrases=extractor.get_n_best(n=5,threshold=threshold)
        # print(keyphrases)
        for phrase in keyphrases:
            # print("phrase",phrase)
            keyPhraseDict[phrase[0]]+=1

    # print(keyphrases)
    yake_res_file=open("yakeRes"+str(i)+"(完整版).txt",'w')
    keyPhraseDict=sorted(keyPhraseDict.items(), key=lambda d: d[1],reverse=True)
    print(keyPhraseDict)
    for key in keyPhraseDict:
        key_split=key[0].split(' ')
        if  len(key_split)>1 and key[1] >=1:
            yake_res_file.write(key[0]+':'+str(key[1])+'\n')
    yake_res_file.close()
    abstract_file.close()