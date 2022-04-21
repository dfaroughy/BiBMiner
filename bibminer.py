import urllib.request
import requests
import urllib3
import ssl
import sys
import json
import random

class bibtex(object):

    def __init__(self,key,method='urllib'):
        
        self.key=str(key) 
        self.entry=None
        self.inspire={'eprint':None, 'bibkey':None,  'id':None }
        self.is_eprint=False         # arxiv numbers e.g. 2022.12345, hep-ph/123456
        self.is_id=False             # hep inspire id e.g 1234567
        self.is_custom=False
        self.is_missing=False 
        try: 
            float(self.key)
            self.is_eprint=True                           
        except ValueError:
            if 'hep-' in self.key: self.is_eprint=True
        if self.key.isdigit(): self.is_id=True    
        if '<' in self.key and '>' in self.key: self.is_custom=True

        def fetch_bibtex_entry(key, identifier='key', method=method):
            url_id = 'https://inspirehep.net/api/literature/{}?format=bibtex'.format(key)
            url_eprint = 'https://inspirehep.net/api/arxiv/{}?format=bibtex'.format(key)
            url_key='https://inspirehep.net/api/literature?q={}'.format(key)
            if identifier=='key': url=url_key
            elif identifier=='id': url=url_id
            elif identifier=='eprint': url=url_eprint
            
            # #....urllib:
            if method=='urllib':
                with urllib.request.urlopen(url, context=ssl.SSLContext()) as response:
                    http=response.read()
                    http=http.decode('utf-8')
                    return http

            #....requests:
            if method=='requests':
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                http=requests.get(url, verify=False)
                http=http.content
                http=http.decode('utf-8')
                return http

            #....urllib3:
            if method=='urllib3':
                http=urllib3.PoolManager()
                http=http.request('GET', url)
                http=http.data.decode('utf-8')
                return http

        try:   
            if self.is_id: 
                self.entry=fetch_bibtex_entry(self.key, identifier='id')
                out=self.entry
                out=out.replace(' ',''); out=out.replace('\n','');
                out=out.replace('"',''); out=out.split(',')
                for x in out:
                    if 'eprint'in x: self.inspire['eprint']=x.split('=')[-1]
                    if '@' in x: self.inspire['bibkey']=x.split('{')[-1]
                self.inspire['id']=self.key
                
            elif self.is_eprint:        
                self.entry=fetch_bibtex_entry(self.key, identifier='eprint')
                out=self.entry
                out=out.replace(' ',''); out=out.replace('\n','');
                out=out.replace('"',''); out=out.split(',')
                for x in out:
                    if 'eprint'in x: self.inspire['eprint']=x.split('=')[-1]
                    if '@' in x: self.inspire['bibkey']=x.split('{')[-1]  
                id_tmp=fetch_bibtex_entry(self.inspire['bibkey'], identifier='key')
                self.inspire['id']=int(json.loads(id_tmp)['hits']['hits'][0]['id'])
            
            elif self.is_custom:
                custom=self.key.replace('<','')
                custom=custom.replace('>',' ')
                custom=custom.split()
                title=custom[0].replace('_',' '); authors=custom[1:-1]; year=custom[-1]
                authors=[a.replace(';',', ') for a in authors]
                authors=' and '.join(authors)
                self.inspire = self.inspire.fromkeys(self.inspire,str(None))
                self.entry='@article{'+self.key+',\n    author = "'+authors+'",\n    title = "'+title+'",\n    year = "'+year+'"}\n'

            else:
                key_tmp=fetch_bibtex_entry(self.key, identifier='key')
                self.inspire['id']=int(json.loads(key_tmp)['hits']['hits'][0]['id'])
                self.entry=fetch_bibtex_entry(self.inspire['id'], identifier='id')
                out=self.entry
                out=out.replace(' ',''); out=out.replace('\n','');
                out=out.replace('"',''); out=out.split(',')
                for x in out:
                    if 'eprint'in x: self.inspire['eprint']=x.split('=')[-1]
                    if '@' in x: self.inspire['bibkey']=x.split('{')[-1]
        
        except (IndexError or KeyError):
            self.is_missing=True  
            self.entry={"status": 404, "message": "PID does not exist."}
            self.inspire={'eprint':None, 'bibkey':None,  'id':None }


def make_bibtex_file(tex, output=False, verbose=True, method='urllib'):
    
    citations={}
    if not output: output=tex.split('.')[0]+'.bib'    
    rand=hex(random.getrandbits(100))

    with open(tex,encoding="ascii", errors="surrogateescape") as latex:
        n=0
        for line in latex:
            n+=1
            line=line.replace(' ','')
            line=line.replace('\n','')
            line=line.replace('\cite{',' {}'.format(rand))
            line=line.replace('}',' ')

            for l in line.split():         
                if str(rand) in l:
                    l=l.replace(str(rand),' ')
                    l=l.replace(',',' ')
                    
                    for cite in l.split():
                        if cite not in citations.keys(): citations[cite]=[str(n)]
                        else: citations[cite].append(str(n))

    bibtex_file=open(output,'w',encoding="ascii")
    bibtex_file.write('% Automatically generated with BiBminer 3000 (https://github.com/dfaroughy/BiBMiner)\n\n')
    
    for key in citations.keys():
        #=================
        ref=bibtex(key,method=method)
        #=================
        if ref.is_missing:
            print(u'l:{}| {} ---------<ERROR {}! {}> {}'.format(','.join(citations[key]),key,ref.entry["status"],ref.entry["message"],'\u2717'))
        else:
            if verbose: print(u'l:{}| {} {}'.format(','.join(citations[key]),key,'\u2714'))
            if ref.inspire['bibkey']!=key: ref.entry=ref.entry.replace(ref.inspire['bibkey'],key)
            ref.entry = ref.entry.encode('ascii', 'ignore').decode('ascii')
            bibtex_file.write(ref.entry)

    print('done!')
    bibtex_file.close()

if len(sys.argv)==2: make_bibtex_file(tex=sys.argv[1])
