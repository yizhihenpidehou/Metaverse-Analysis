#key:AIzaSyCWpYSh-u2G29oAKlFsg4sA_ziYYNF9hJg
# Python program to get a set of
# places according to your search
# query using Google Places API

# importing required modules
import requests, json
import googlemaps
import random
#AIzaSyCWpYSh-u2G29oAKlFsg4sA_ziYYNF9hJg
key2 = 'AIzaSyCWpYSh-u2G29oAKlFsg4sA_ziYYNF9hJg'
save = open ('11月location_google_geotext_certain.json','a+')

allnum = 0
counthit = 0

with open('11月location_uncertain2.json','r') as ww:

    splist = [".","'"]
    str=ww.read()
    sum=0
    lst=str.split('---------------------------------\n')

    #print(lst)
    
    countrystata = {}

    for i in range(0,len(lst)-1):

        article =json.loads(lst[i])
        print(i,article["title"])
        article['country'] = []
        article.setdefault('ctmighterror',[])
                
        if article['author_location']==[]:
            continue
            
        author_location = article['author_location']
            
        if len(author_location)!=0 and ('not found' not in author_location):
            for j in range(0, len(author_location)):
                if len(author_location[j])<2:
                    print(author_location[j]+'invalid')
                    article['country'].append('')
                    continue
                #标记是不是可能不准
                mighterror = 0
                
                allnum = allnum+1
                query = author_location[j]
                
                #有时候抓到了多余信息
                if "</" in query:
                    query = query.split(">")[len(query.split(">"))-1]
                
                query=query.lower()
                print(query)


#                url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+query+"&key=AIzaSyCWpYSh-u2G29oAKlFsg4sA_ziYYNF9hJg"


                url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+query+"&key="+key2

                payload={}
                headers = {}

                response = requests.request("GET", url, headers=headers, data=payload)

                oldresponse = response
                #print(response.text)
                response = json.loads(response.text)
                
                #针对多个地址结果的，把仓库排除，剩下的里面随便选一个，并且如果国家都不一样就标记可能有问题
                try:
                    rcountrylst = []
                    
                    if len(response['results'])>1:
                        print('匹配到多个地址')
                        for r in range(0,len(response['results'])):
                            if 'storage' not in response['results'][r]['types']:
                                rcountry =response['results'][r]['formatted_address']
                                rcountrylst.append(rcountry.split(',')[len(rcountry.split(','))-1])
                                
                        rcountrylst = list(set(rcountrylst))
                        print('多个地址的国家：')
                        print(rcountrylst)
                        if len(rcountrylst)>1:
                            #print(rcountrylst)
                            print('匹配到多个国家的位置，需要标记')
                            article['ctmighterror'].append(j)
                            
                        #随便选一个不是仓库的地点
                        while True:
                            rand = random.randint(0,len(response['results'])-1)
                            if 'storage' not in response['results'][rand]['types']:
                                resultaddress = response['results'][rand]['geometry']['location']
                                break
                    
                     
                    #之匹配到一个地点
                    else:
                        print('只匹配到一个地址')
                        resultaddress = response['results'][0]['geometry']['location']
                    
                    print(resultaddress)

                    #根据坐标再返回信息
                    gmaps = googlemaps.Client(key=key2)

                    reverse_geocode_result = gmaps.reverse_geocode((resultaddress['lat'],resultaddress['lng']))

                    #找到信息里面的国家
                    resultlst = reverse_geocode_result[0]['address_components']
                    for e in reverse_geocode_result[0]['address_components']:
                        if 'country' in e['types']:
                            print(e['short_name'])
                            resultcountry = e['short_name']
            
                    resultcountry = resultcountry.lower()
                    print(resultcountry)
                    author_country = resultcountry

                    article['country'].append(author_country)
                    
                    
                    if author_country not in countrystata.keys():
                        countrystata.setdefault(author_country,1)

                    else:
                        countrystata[author_country]+=1

                except Exception as e:
                    print((e))
                    print('response:')
#                    print(oldresponse.text)
                    article['country']=['not found']
                    pass
                    

                else:
                    pass


        print(article['country'])
        print('---------------------------------\n')
        json_r=json.dumps(article)
        save.write((json_r))
        save.write('\n')
        save.write('---------------------------------\n')

    sortedcountry=sorted(countrystata.items(), key=lambda x: x[1], reverse=True)
    print((sortedcountry))
    
    
    print('allnum:')
    print(allnum)
    
