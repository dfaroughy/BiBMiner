# HEP BiBminer

```bibminer``` is a python module that extracts the citations from a LaTeX file and generates the corresponding *.bib* file automatically. The citation identifiers inside ```\cite{...}``` in the *.tex* file must be in a format compatible with [**HEP Inspire**](https://inspirehep.net). The supported identifers are: [arxiv](https://arxiv.org) preprint number of the type ```2022.12345``` or ```hep-th/123456```, hep inspire id, or the bibtex PID of type ```Witten:123ab```. 

To generate the *.bib* for a latex file ```main.tex``` simply run the code

```python
make_bib('path/to/file/main.tex')
 ```

Citations are automatically extracted from HEP inspires using: ```get_bibtex()```. 
For example, the input can be a bibtex PID:

```python
cite=get_bibtex('Camargo-Molina:2022ord')
print(cite.bibtex)
```

with output

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

or a arxiv preprint number:

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

