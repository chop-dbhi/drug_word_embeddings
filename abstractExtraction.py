import socket
from difflib import *
import urllib
# import urllib.error
from urllib.parse import unquote
import pdb

import json
import xml.etree.ElementTree as ET
from functools import reduce
import numpy as np
import matplotlib
matplotlib.use('Agg')
# matplotlib inline
from matplotlib import pyplot as plt
import pandas as pd
import time

#max articles to retrieve
retmax = 500000

site = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax={0}&retmode=json&{1}'
query = 'drug[All Fields] AND hasabstract[text] AND English[lang] AND (Case Reports[ptyp] OR Clinical Trial[ptyp] OR Clinical Conference[ptyp] OR Clinical Study[ptyp])'
qrydict = {'term': query}
encoded_qry = urllib.parse.urlencode(qrydict)
print("query is: %s" % query)

request = urllib.request.urlopen(site.format(retmax, encoded_qry))
json_response_string = request.read().decode("utf-8")
json_response = json.loads(json_response_string)
raw_idlist = json_response['esearchresult']['idlist']
total_ids = len(raw_idlist)
print(total_ids)
idlist = raw_idlist
print(len(idlist))



def recursive_find(xml, child_path):
    child = xml.find(child_path[0])
    if child is not None and len(child_path)==1:
        return child.text
    elif child is not None:
        return recursive_find(child, child_path[1:])
    else:
        return None

def recursive_findall(xml, child_path):
    if len(child_path) == 1:
        # last child in path, so get all children and values
        values = []
        for child in xml.findall(child_path[0]):
            values.append(child.text)
        if len(values)==0:
            return None
        else:
            return values
    else:
        child = xml.find(child_path[0])
        if child is not None:
            return recursive_findall(child, child_path[1:])
        else:
            return None

def get_year(pubmed_article_xml):
    year = recursive_find(pubmed_article, ['MedlineCitation', 'Article', 'ArticleDate', 'Year'])
    if year is None:
        year = recursive_find(pubmed_article, ['MedlineCitation', 'DateCreated', 'Year'])
    return year

def get_affiliations(article_xml):
    affiliations = []
    try:
        authors = article_xml.find('AuthorList').findall('Author')
        for author in authors:
            try:
                author_affiliations = author.find('AffiliationInfo').findall('Affiliation')
                for affilliation in author_affiliations:
                    affiliations.append(affilliation.text)
            except:
                pass
    except:
        pass
    return affiliations


journal_info = []
journal_info_toNow = []
incomplete_info_ids = []
for cnt, idx in enumerate(idlist):
    site = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id={0}'
    try:
        request = urllib.request.urlopen(site.format(idx))
        xml_response_string = request.read().decode("utf-8")
    except urllib.error.URLError as e: xml_response_string = ''
    except socket.timeout as e: xml_response_string = ''
    except urllib.error.HTTPError as e: xml_response_string = ''
    # except socket.error as e: xml_response_string = ''
    # except UnicodeEncodeError as e: xml_response_string = ''
    # except http.client.BadStatusLine as e: xml_response_string = ''
    # except http.client.IncompleteRead as e: xml_response_string = ''
    # except urllib.error.URLError as e: xml_response_string = e.read().decode("utf8", 'ignore')
    if not xml_response_string:
        continue

    tree = ET.fromstring(xml_response_string)
    if cnt % 50 == 0:
        print('completed {0} of {1}'.format(cnt, total_ids))
        journal_info_toNow.extend(journal_info)
        journal_info = []
    for pubmed_article in tree.getchildren():
        try:
            article_id_list = pubmed_article.find('PubmedData').find('ArticleIdList')
            pubmed_id = ''
            for child in article_id_list.getchildren():
                if child.attrib['IdType']=='pubmed':
                    pubmed_id = child.text
                    if not pubmed_id == idx:
                        print("Error for {0}".format(idx))
            article = pubmed_article.find('MedlineCitation').find('Article')

            title = article.find('ArticleTitle').text
            abstract_xml = article.find('Abstract')
            abstract = ''
            for child in abstract_xml.getchildren():
                if child.tag=='AbstractText':
                    abstract = '{0}{1}\n'.format(abstract, child.text)
            year = get_year(pubmed_article)
            keywords = recursive_findall(pubmed_article, ['MedlineCitation', 'KeywordList', 'Keyword'])
            journal_type = recursive_findall(article, ['PublicationTypeList', 'PublicationType'])
            journal_type = [x.lower() for x in journal_type]
            lang = recursive_find(article, ['Language'])
            if lang is not None:
                lang = lang.lower()
            journal = recursive_find(article, ['Journal', 'Title'])
            author_affiliations = get_affiliations(article)
            journal_info.append({'pmid':pubmed_id,
                                   'title':title,
                                   'abstract':abstract,
                                   'year': year,
                                   'keywords':keywords,
                                   'affiliations':author_affiliations,
                                   'publication_types':journal_type,
                                   'language':lang,
                                   'journal': journal
                                   })
        except:
            incomplete_info_ids.append(idx)

print(len(incomplete_info_ids))

journal_info_toNow.extend(journal_info)

df = pd.DataFrame(journal_info_toNow)
qh = str(hash(query)).replace('-', '')
today = time.strftime("%d_%m_%Y")
with open('pubmed_queries.txt', 'a') as f:
    f.write('hash:{0}\nDate:\t{4}\nDocument Count:\t{1}\nIncomplete Data\t{2}\n{3}\n\n'.format(qh,
                                                                              len(idlist),
                                                                              len(incomplete_info_ids),
                                                                              query,
                                                                              today))

fp = './data/pubmed_{0}_{1}.csv'.format(qh, today)
df.to_csv(fp, index_label='idx')
print('Done')

df
