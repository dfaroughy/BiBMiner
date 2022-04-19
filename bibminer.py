import numpy as np
import urllib3
import sys
import json
from collections import OrderedDict

http = urllib3.PoolManager()

class get_bibtex(object):

    def __init__(self,cite):
 
        self.bibtexid=False    #    bibtex identifier e.g. Witten:123abc  
        self.eprint=False      #    arxiv numbers e.g. 2022.12345 , hep-ph/123456 
        self.inspireid=False   #    hep inspire id e.g 1234567
        self.unknown=False      
        self.cite=str(cite) 
        self.ids={'bibtexid': None, 'eprint': None, 'inspireid':None}
        
        try:
            if ':' in self.cite: 
                url='https://inspirehep.net/api/literature?q={}'.format(cite)
                resp = http.request('GET', url)
                self.ids['inspireid']=int(json.loads(resp.data.decode('utf-8'))['hits']['hits'][0]['id'])
                url = 'https://inspirehep.net/api/literature/{}?format=bibtex'.format(self.ids['inspireid'])
                resp = http.request('GET', url)
                out=resp.data.decode('utf-8') 
                self.bibtex=out
                #==============
                if '"status": 404' not in out:
                    out=out.replace(' ',''); out=out.replace('\n','');
                    out=out.replace('"',''); out=out.split(',')
                    for x in out:
                        if 'eprint'in x: self.ids['eprint']=x.split('=')[-1]
                        if '@' in x: self.ids['bibtexid']=x.split('{')[-1]
                    self.bibtexid=True
                
            elif self.cite.isdigit(): 
                url = 'https://inspirehep.net/api/literature/{}?format=bibtex'.format(cite)
                resp = http.request('GET', url)
                out=resp.data.decode('utf-8')
                self.bibtex=out
                #==============
                if '"status": 404' not in out:
                    out=out.replace(' ',''); out=out.replace('\n','');
                    out=out.replace('"',''); out=out.split(',')
                    for x in out:
                        if 'eprint'in x: self.ids['eprint']=x.split('=')[-1]
                        if '@' in x: self.ids['bibtexid']=x.split('{')[-1]
                    self.ids['inspireid']=self.cite
                    self.inspireid=True
                
            elif ('.' in self.cite or 'hep-' in self.cite):        
                url = 'https://inspirehep.net/api/arxiv/{}?format=bibtex'.format(cite)
                resp = http.request('GET', url)
                out=resp.data.decode('utf-8')
                self.bibtex=out
                #==============
                if '"status": 404' not in out:
                    out=out.replace(' ',''); out=out.replace('\n','');
                    out=out.replace('"',''); out=out.split(',')
                    for x in out:
                        if 'eprint'in x: self.ids['eprint']=x.split('=')[-1]
                        if '@' in x: self.ids['bibtexid']=x.split('{')[-1]                    
                    url='https://inspirehep.net/api/literature?q={}'.format(self.ids['bibtexid'])
                    resp = http.request('GET', url)
                    self.ids['inspireid']=int(json.loads(resp.data.decode('utf-8'))['hits']['hits'][0]['id'])
                    self.eprint=True
            else:
                self.unknown=True  
                self.bibtex={"status": 404, "message": "PID does not exist."}
                self.ids={'bibtexid': None, 'eprint': None, 'inspireid':None}
        
        except IndexError or KeyError:
            self.unknown=True  
            self.bibtex={"status": 404, "message": "PID does not exist."}
            self.ids={'bibtexid': None, 'eprint': None, 'inspireid':None}

def make_bib(tex, output=False, new_tex=False):
    tex_cites=[]
    if not output:
        output=tex.split('.')[0]+'.bib'    
    bib=open(output,'w')
    with open(tex,encoding="ascii", errors="surrogateescape") as latex:
        for line in latex:
            line=line.replace(' ','')
            line=line.replace('\cite{',' __________')
            line=line.replace('}',' ')
            for l in line.split():         
                if '__________' in l:
                    l=l.replace('__________',' ')
                    l=l.replace(',',' ')
                    for cite in l.split():
                        tex_cites.append(cite)
    tex_cites=OrderedDict.fromkeys(tex_cites)  
    bibdic={}
    for b in tex_cites:
        cite=get_bibtex(b)
        if cite.unknown:
            print(u'{} {} ------------- ERROR {}! {}'.format(b,'\u2717',cite.bibtex["status"],cite.bibtex["message"]))
        elif b!=cite.ids['bibtexid']:
            bibdic[b]=cite.ids['bibtexid']
            print(u'{} {} ------------- WARNING! PID superseded by: {}'.format(b,'\u2717',cite.ids['bibtexid']))
        else:
            bibdic[b]=cite.ids['bibtexid']
            print(u'{} {}'.format(b,'\u2714'))
            bib.write(cite.bibtex)

    if new_tex:
        print('\n')
        print('writting new .tex file with corrected bibliography...')
        tex2=open(tex.split('.')[0]+'_v2_bibminer.tex','w') 
        with open(tex,encoding="ascii", errors="surrogateescape") as latex:
            n=0
            for line in latex:
                n+=1
                if '\cite{' in line:
                    for b in list(bibdic.keys()):
                        if b in line: 
                            if b!=bibdic[b]:
                                line=line.replace(b,bibdic[b])
                                print('\treplaced {} --> {}'.format(b,bibdic[b]))
                try:
                    tex2.write(line)
                except UnicodeEncodeError:
                    print('\t\twarning: bibminer encountered a bad string at line {}. line skipped!'.format(n))
        tex2.close()

    print('done!')
    bib.close()

if len(sys.argv)==2: make_bib(tex=sys.argv[1])
if len(sys.argv)==3: make_bib(tex=sys.argv[1],new_tex=sys.argv[2])
