import urllib3
import sys
import json
import random


class get_bibtex(object):

    def __init__(self,cite):
        
        self.cite=str(cite) 
        self.ids={'bibtexid':None, 'eprint':None, 'inspireid':None }
        self.is_eprint=False         # arxiv numbers e.g. 2022.12345, hep-ph/123456
        self.is_inspirePID=False     # hep inspire id e.g 1234567
        self.is_missing=False 
        self.is_inprep=False
        self.is_privcomm=False
        try: 
            float(self.cite)
            self.is_eprint=True                           
        except ValueError:
            if 'hep-' in self.cite: self.is_eprint=True
        if self.cite.isdigit(): self.is_inspirePID=True    
        if '(inprep)(' in self.cite: self.is_inprep=True
        if '(privatecomm)(' in self.cite: self.is_privcomm=True
        
        http = urllib3.PoolManager()

        try:                
            if self.is_inspirePID: 
                url = 'https://inspirehep.net/api/literature/{}?format=bibtex'.format(self.cite)
                resp = http.request('GET', url)
                out=resp.data.decode('utf-8')
                self.bibtex=out
                #==============
                out=out.replace(' ',''); out=out.replace('\n','');
                out=out.replace('"',''); out=out.split(',')
                for x in out:
                    if 'eprint'in x: self.ids['eprint']=x.split('=')[-1]
                    if '@' in x: self.ids['bibtexid']=x.split('{')[-1]
                self.ids['inspireid']=self.cite
                
            elif self.is_eprint:        
                url = 'https://inspirehep.net/api/arxiv/{}?format=bibtex'.format(self.cite)
                resp = http.request('GET', url)
                out=resp.data.decode('utf-8')
                self.bibtex=out
                #==============               
                out=out.replace(' ',''); out=out.replace('\n','');
                out=out.replace('"',''); out=out.split(',')
                for x in out:
                    if 'eprint'in x: self.ids['eprint']=x.split('=')[-1]
                    if '@' in x: self.ids['bibtexid']=x.split('{')[-1]                    
                url='https://inspirehep.net/api/literature?q={}'.format(self.ids['bibtexid'])
                resp = http.request('GET', url)
                self.ids['inspireid']=int(json.loads(resp.data.decode('utf-8'))['hits']['hits'][0]['id'])

            elif self.is_inprep:
                authors=self.cite.replace('(inprep)','')
                authors=authors.replace('(','')
                authors=authors.replace(')',' ')
                authors=[a.replace(';',', ') for a in authors.split()]
                authors=' and '.join(authors)
                self.ids = self.ids.fromkeys(self.ids,str(None))
                self.bibtex='@article{'+self.cite+',\n    author = "'+authors+'",\n    title = "{In Preparation}"\n}\n'

            elif self.is_privcomm:
                authors=self.cite.replace('(privatecomm)','')
                authors=authors.replace('(','')
                authors=authors.replace(')',' ')
                authors=[a.replace(';',', ') for a in authors.split()]
                authors=' and '.join(authors)
                self.ids = self.ids.fromkeys(self.ids,str(None))
                self.bibtex='@article{'+self.cite+',\n    author = "'+authors+'",\n    title = "{Private Communication}"\n}\n'

            else:
                url='https://inspirehep.net/api/literature?q={}'.format(self.cite)
                resp = http.request('GET', url)
                self.ids['inspireid']=int(json.loads(resp.data.decode('utf-8'))['hits']['hits'][0]['id'])
                url = 'https://inspirehep.net/api/literature/{}?format=bibtex'.format(self.ids['inspireid'])
                resp = http.request('GET', url)
                out=resp.data.decode('utf-8') 
                self.bibtex=out
                #==============
                out=out.replace(' ',''); out=out.replace('\n','');
                out=out.replace('"',''); out=out.split(',')
                for x in out:
                    if 'eprint'in x: self.ids['eprint']=x.split('=')[-1]
                    if '@' in x: self.ids['bibtexid']=x.split('{')[-1]
        
        except (IndexError or KeyError):
            self.is_missing=True  
            self.bibtex={"status": 404, "message": "PID does not exist."}
            self.ids={'bibtexid': None, 'eprint': None, 'inspireid':None}


def make_bib(tex, output=False, verbose=True):
    
    tex_cites={}
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
                        if cite not in tex_cites.keys(): tex_cites[cite]=[str(n)]
                        else: tex_cites[cite].append(str(n))

    bib=open(output,'w',encoding="ascii")
    bib.write('% Automatically generated with BiBminer 3000 (https://github.com/dfaroughy/BiBMiner)\n\n')
    
    for b in tex_cites.keys():
        #=================
        cite=get_bibtex(b)
        #=================
        if cite.is_missing:
            print(u'l:{}| {} ---------<ERROR {}! {}> {}'.format(','.join(tex_cites[b]),b,cite.bibtex["status"],cite.bibtex["message"],'\u2717'))

        elif cite.ids['bibtexid']!=b:
            if verbose: print(u'l:{}| {} {}'.format(','.join(tex_cites[b]),b,'\u2714'))
            cite.bibtex=cite.bibtex.replace(cite.ids['bibtexid'],b)
            cite.bibtex = cite.bibtex.encode('ascii', 'ignore').decode('ascii')
            bib.write(cite.bibtex)
        
        else:
            if verbose: print(u'l:{}| {} {}'.format(','.join(tex_cites[b]),b,'\u2714'))
            cite.bibtex = cite.bibtex.encode('ascii', 'ignore').decode('ascii')
            bib.write(cite.bibtex)

    print('done!')
    bib.close()

if len(sys.argv)==2: make_bib(tex=sys.argv[1])
