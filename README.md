# BiBminer

A module that extracts the citations from a LaTeX file and generates the corresponding *.bib* file automatically. The citation id inside *\cite{...}* in the *.tex* file must be in a format compatible with [**HEP Inspire**](https://inspirehep.net). The supported identifers are: arxiv preprint number (e.g. *2022.1234* or *hep-th/123456*, ... ), hep inspire id, or the bibtex id (e.g. *Witten:123ab*). 

 For example, bibtex from the bibtex id:

```python
cite=get_bibtex('Camargo-Molina:2022ord')
print(cite.bibtex)
```

outputs:

```python
@article{Camargo-Molina:2022ord,
    author = "Camargo-Molina, Jos\'e Eliel and Rajantie, Arttu",
    title = "{Phase transitions in de Sitter: The stochastic formalism}",
    eprint = "2204.02875",
    archivePrefix = "arXiv",
    primaryClass = "gr-qc",
    month = "4",
    year = "2022"
}
```

or bibtex from the arxiv preprint number:

```python
cite=get_bibtex('hep-ph/9905221')
print(cite.bibtex)
 ```
yields:
```python
@article{Randall:1999ee,
    author = "Randall, Lisa and Sundrum, Raman",
    title = "{A Large mass hierarchy from a small extra dimension}",
    eprint = "hep-ph/9905221",
    archivePrefix = "arXiv",
    reportNumber = "MIT-CTP-2860, PUPT-1860, BUHEP-99-9",
    doi = "10.1103/PhysRevLett.83.3370",
    journal = "Phys. Rev. Lett.",
    volume = "83",
    pages = "3370--3373",
    year = "1999"
}
```

One can also extract the other identifiers from one of them:

```python
cite=get_bibtex('hep-ph/9905221')
print(cite.ids)
 ```
 outputs:
 
 ```python
 {'bibtexid': 'Randall:1999ee', 'eprint': 'hep-ph/9905221', 'inspireid': 499284}
 ```
