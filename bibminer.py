import urllib3
import sys
import json
import random

class bibtex(object):

    def __init__(self,key):
        
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

        http = urllib3.PoolManager()

        try:                
            if self.is_id: 
                url = 'https://inspirehep.net/api/literature/{}?format=bibtex'.format(self.key)
                resp = http.request('GET', url)
                out=resp.data.decode('utf-8')
                self.entry=out
                #==============
                out=out.replace(' ',''); out=out.replace('\n','');
                out=out.replace('"',''); out=out.split(',')
                for x in out:
                    if 'eprint'in x: self.inspire['eprint']=x.split('=')[-1]
                    if '@' in x: self.inspire['bibkey']=x.split('{')[-1]
                self.inspire['id']=self.key
                
            elif self.is_eprint:        
                url = 'https://inspirehep.net/api/arxiv/{}?format=bibtex'.format(self.key)
                resp = http.request('GET', url)
                out=resp.data.decode('utf-8')
                self.entry=out
                #==============               
                out=out.replace(' ',''); out=out.replace('\n','');
                out=out.replace('"',''); out=out.split(',')
                for x in out:
                    if 'eprint'in x: self.inspire['eprint']=x.split('=')[-1]
                    if '@' in x: self.inspire['bibkey']=x.split('{')[-1]                    
                url='https://inspirehep.net/api/literature?q={}'.format(self.inspire['bibkey'])
                resp = http.request('GET', url)
                self.inspire['id']=int(json.loads(resp.data.decode('utf-8'))['hits']['hits'][0]['id'])
            
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
                url='https://inspirehep.net/api/literature?q={}'.format(self.key)
                resp = http.request('GET', url)
                self.inspire['id']=int(json.loads(resp.data.decode('utf-8'))['hits']['hits'][0]['id'])
                url = 'https://inspirehep.net/api/literature/{}?format=bibtex'.format(self.inspire['id'])
                resp = http.request('GET', url)
                out=resp.data.decode('utf-8') 
                self.entry=out
                #==============
                out=out.replace(' ',''); out=out.replace('\n','');
                out=out.replace('"',''); out=out.split(',')
                for x in out:
                    if 'eprint'in x: self.inspire['eprint']=x.split('=')[-1]
                    if '@' in x: self.inspire['bibkey']=x.split('{')[-1]
        
        except (IndexError or KeyError):
            self.is_missing=True  
            self.entry={"status": 404, "message": "PID does not exist."}
            self.inspire={'eprint':None, 'bibkey':None,  'id':None }


def make_bibtex_file(tex, output=False, verbose=True):
    
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
        ref=bibtex(key)
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
