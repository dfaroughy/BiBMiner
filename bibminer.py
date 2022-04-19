import urllib3
import sys
import json
import random

class get_bibtex(object):

    def __init__(self,cite):
        
        self.ids={'bibtexid': None, 'eprint': None, 'inspireid':None} 
        self.bibtexid=False    #    bibtex identifier e.g. Witten:123abc  
        self.eprint=False      #    arxiv numbers e.g. 2022.12345 , hep-ph/123456 
        self.inspireid=False   #    hep inspire id e.g 1234567
        self.unknown=False      
        self.cite=str(cite) 
        http = urllib3.PoolManager()

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
            self.bibtex={"status": 404, "message": "PID does not exist"}
            self.ids={'bibtexid': None, 'eprint': None, 'inspireid':None}


def make_bib(tex, output=False, verbose=True):
    
    tex_cites={}
    if not output: output=tex.split('.')[0]+'.bib'    
    bib=open(output,'w')
    ran=hex(random.getrandbits(100))

    with open(tex,encoding="ascii", errors="surrogateescape") as latex:
        n=0
        for line in latex:
            n+=1
            line=line.replace(' ','')
            line=line.replace('\cite{',' {}'.format(ran))
            line=line.replace('}',' ')

            for l in line.split():         
                if str(ran) in l:
                    l=l.replace(str(ran),' ')
                    l=l.replace(',',' ')

                    for cite in l.split():
                        if cite not in tex_cites.keys(): tex_cites[cite]=[str(n)]
                        else: tex_cites[cite].append(str(n))

    for b in tex_cites.keys():
        cite=get_bibtex(b)
        if cite.unknown:
            print(u'l.{}| {} -----------<ERROR {}! {}> {}'.format(','.join(tex_cites[b]),b,cite.bibtex["status"],cite.bibtex["message"],'\u2717'))
        elif b!=cite.ids['bibtexid']:
            if verbose: print(u'l.{}| {} -----------<{}> {}'.format(','.join(tex_cites[b]), b,cite.ids['bibtexid'],'\u2714'))
            cite.bibtex=cite.bibtex.replace(cite.ids['bibtexid'],b)
            bib.write(cite.bibtex)
        else:
            if verbose: print(u'l.{}| {} {}'.format(','.join(tex_cites[b]),b,'\u2714'))
            bib.write(cite.bibtex)

    print('done!')
    bib.close()

if len(sys.argv)==2: make_bib(tex=sys.argv[1])
