import json

import requests

url = "https://v2.namsor.com/NamSorAPIv2/api2/json/genderBatch"

# payload = {
#   "personalNames": [
#     {
#       "firstName": "John",
#       "lastName": "David N. Dionisio"
#     },
# {
#       "firstName": "Yan",
#       "lastName": "Chen"
#     }
#   ]
# }
headers = {
    "X-API-KEY": "6101232d739e61525e0b718ac3a9a42f",
    "Accept": "application/json",
    "Content-Type": "application/json"
}



def get_gender_amsor(lst,respath):
    res_file=open(respath,'a+')
    for i in range(0,len(lst)-1):
        json_str=json.loads(lst[i])
        author_lst=json_str["author"]
        gender_res_lst=[]
        for author in author_lst:
            author_split=author.split(" ")
            first_name=author_split[0]
            last_name=""
            for j in range(0,len(author_split)-1):
                last_name+=author_split[j]
            request_dict={"firstName": first_name,"lastName": last_name}
            payload = {
                "personalNames": [
                    request_dict
                ]
            }
            response = requests.request("POST", url, json=payload, headers=headers)
            response=json.loads(response.text)
            gender_res=response["personalNames"][0]["likelyGender"]
            if gender_res=="male":
                gender_res_lst.append(1)
            else:
                gender_res_lst.append(0)
        json_str["gender"]=gender_res_lst
        res_file.write(json.dumps(json_str)+'\n')
        res_file.write("---------------------------------\n")
    res_file.close()


if __name__=='__main__':
    baseurl = '/Users/yizhihenpidehou/Desktop/fdu/Metaverse-Analysis/'

    for i in range(1,12):
        targeturl = baseurl
        resurl = baseurl
        if i < 10:
            targeturl+="2022-0"+str(i)+"/fourpublisher_arxiv_withsource_updatedauthor2022-0"+str(i)+".json"
            resurl+="2022-0"+str(i)+"/fourpublisher_arxiv_withsource_updatedauthor2022-0"+str(i)+"_withgender.json"
        else:
            targeturl+="2022-"+str(i)+"/fourpublisher_arxiv_withsource_updatedauthor2022-"+str(i)+".json"
            resurl += "2022-" + str(i) + "/fourpublisher_arxiv_withsource_updatedauthor2022-" + str(
                i) + "_withgender.json"
        request_file=open(targeturl,'r')
        request_file_str=request_file.read()
        request_file_lst=request_file_str.split("---------------------------------\n")
        get_gender_amsor(request_file_lst,resurl)
        request_file.close()