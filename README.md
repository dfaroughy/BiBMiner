# BiBminer

```bibminer``` is a module that extracts the citations from a LaTeX file and generates the corresponding *.bib* file automatically. The citation identifiers inside ```\cite{...}``` in the *.tex* file must be in a format compatible with [**HEP Inspire**](https://inspirehep.net). The supported identifers are: [arxiv](https://arxiv.org) preprint number of the type ```2022.12345``` or ```hep-th/123456```, hep inspire id, or the bibtex PID of type ```Witten:123ab```. 

For example, to code to get the *bibtex* from a given bibtex PID is

```python
cite=get_bibtex('Camargo-Molina:2022ord')
print(cite.bibtex)
```

this outputs:

```
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

or from an arxiv preprint number:

```python
cite=get_bibtex('hep-ph/9905221')
print(cite.bibtex)
 ```

```
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

Each citation will have three unique identifier attributes: ```bibtexid```, ```eprint``` and ```inspireid```. One can extract these as

```python
print(cite.ids)
 ```
 outputs:
 
 ```
 {'bibtexid': 'Randall:1999ee', 'eprint': 'hep-ph/9905221', 'inspireid': 499284}
 ```
 
To generate the *.bib* for a latex file ```main.tex``` simply run

```python
make_bib('path/to/file/main.tex')
 ```
