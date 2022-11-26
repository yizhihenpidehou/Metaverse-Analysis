"""
python_arXiv_parsing_example.py

This sample script illustrates a basic arXiv api call
followed by parsing of the results using the
feedparser python module.

Please see the documentation at
http://export.arxiv.org/api_help/docs/user-manual.html
for more information, or email the arXiv api
mailing list at arxiv-api@googlegroups.com.

urllib is included in the standard python library.
feedparser can be downloaded from http://feedparser.org/ .

Author: Julius B. Lucks

This is free software.  Feel free to do what you want
with it, but please play nice with the arXiv API!
"""

import urllib.request
import feedparser
import json


f=open("11新增/11月arxiv.txt",'r')
f_str=f.read()
lst=f_str.split("---------------------------------\n")
arxiv_f=open("11新增/arxiv_res.txt",'w')
count=0
arxiv_id_lst=[]

for i in range(0,len(lst)-1):
    arxiv_id=""
    arxiv_res_dict = {}
    link = lst[i].split("ee:")[1].split("\n")[0]
    date=lst[i].split("Year:")[1].split("\n")[0]
    title=lst[i].split("title:")[1].split("\n")[0]
    journal=""
    if len(lst[i].split('journal:')) < 2:
        journal = lst[i].split('booktitle:')[1].split('\n')[0]
    else:
        journal = lst[i].split('journal:')[1].split('\n')[0]
    source="arxiv"
    keywords=[]
    author_lst=[]
    abstract=""
    if "https://doi.org/10.48550/" in link:
        arxiv_id = link.split("https://doi.org/10.48550/arXiv.")[1]
        print("arxiv_id:", arxiv_id)
        count += 1
        # arxiv_id_lst.append(arxiv_id)
    elif "https://arxiv.org/" in link:
        arxiv_id = link.split("https://arxiv.org/abs/")[1]
        print("arxiv_id:", arxiv_id)
        count += 1
        # arxiv_id_lst.append(arxiv_id)

    base_url = 'http://export.arxiv.org/api/query?';
    start = 0  # retreive the first 5 results
    max_results = 1
    query = 'id_list=%s&start=%i&max_results=%i' % (arxiv_id,
                                                         start,
                                                         max_results)
    # Search parameters


    # Opensearch metadata such as totalResults, startIndex,
    # and itemsPerPage live in the opensearch namespase.
    # Some entry metadata lives in the arXiv namespace.
    # This is a hack to expose both of these namespaces in
    # feedparser v4.1
    # feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
    # feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

    # perform a GET request using the base_url and query
    response = urllib.request.urlopen(base_url + query).read()
    print("respnse:",response)
    # parse the response using feedparser
    feed = feedparser.parse(response)
    print("feed:",feed)
    # print out feed information
    print('Feed title: %s' % feed.feed.title)

    print('Feed last updated: %s' % feed.feed.updated)
    # print opensearch metadata
    print('totalResults for this query: %s' % feed.feed.opensearch_totalresults)

    print('itemsPerPage for this query: %s' % feed.feed.opensearch_itemsperpage)

    print('startIndex for this query: %s' % feed.feed.opensearch_startindex)


    # Run through each entry, and print out information
    for entry in feed.entries:
        print('e-print metadata')

        print('arxiv-id: %s' % entry.id.split('/abs/')[-1])

        print('Published: %s' % entry.published)

        print('Title:  %s' % entry.title)


        # feedparser v4.1 only grabs the first author
        author_string = entry.author

        # grab the affiliation in <arxiv:affiliation> if present
        # - this will only grab the first affiliation encountered
        #   (the first affiliation for the first author)
        # Please email the list with a way to get all of this information!
        try:
            author_string += ' (%s)' % entry.arxiv_affiliation
        except AttributeError:
            pass

        print('Last Author:  %s' % author_string)


        # feedparser v5.0.1 correctly handles multiple authors, print them all
        try:
            print('Authors:  %s' % ', '.join(author.name for author in entry.authors))
            for author in entry.authors:
                author_lst.append(author)
        except AttributeError:
            pass

        # get the links to the abs page and pdf for this e-print
        # for link in entry.links:
        #     if link.rel == 'alternate':
        #         print('abs page link: %s' % link.href)
        #
        #     elif link.title == 'pdf':
        #         print('pdf link: %s' % link.href)


        # The journal reference, comments and primary_category sections live under
        # the arxiv namespace
        # try:
        #     journal_ref = entry.arxiv_journal_ref
        # except AttributeError:
        #     journal_ref = 'No journal ref found'
        # print('Journal reference: %s' % journal_ref)

        #
        # try:
        #     comment = entry.arxiv_comment
        # except AttributeError:
        #     comment = 'No comment found'
        # print('Comments: %s' % comment)


        # Since the <arxiv:primary_category> element has no data, only
        # attributes, feedparser does not store anything inside
        # entry.arxiv_primary_category
        # This is a dirty hack to get the primary_category, just take the
        # first element in entry.tags.  If anyone knows a better way to do
        # this, please email the list!
        print('Primary Category: %s' % entry.tags[0]['term'])


        # Lets get all the categories
        all_categories = [t['term'] for t in entry.tags]
        print('All Categories: %s' % (', ').join(all_categories))


        # The abstract is in the <summary> element
        print('Abstract: %s' % entry.summary)
        abstract=entry.summary
    arxiv_res_dict["title"]=title
    arxiv_res_dict["publish"]=journal
    arxiv_res_dict["date"]=date
    arxiv_res_dict["abstract"]=abstract
    arxiv_res_dict["source"]=source
    arxiv_res_dict["author"]=author_lst
    arxiv_res_dict["author_location"]=[]
    arxiv_res_dict["link"]=link
    arxiv_f.write(json.dumps(arxiv_res_dict)+'\n')
    arxiv_f.write("---------------------------------\n")
