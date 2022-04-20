# BiBminer 3000

```bibminer``` is a python module that extracts the citations keys from a LaTeX file and generates the corresponding BibTeX file automatically. 

To generate the *.bib* for a latex file ```main.tex``` simply run the code

```python
make_bibtex_file('path/to/file/main.tex')
 ```

Citations are automatically extracted from HEP inspires using the class ```bibtex```. 
For example, the input can be a bibtex PID:

```python
ref=bibtex('Camargo-Molina:2022ord')
print(ref.entry)
```

yields

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
ref=bibtex('hep-ph/9905221')
print(ref.entry)
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

Each citation will have unique Inspire keys that can be used: ```key```, ```eprint``` and ```id```. One can extract these as

```python
print(cite.inspire)
 ```
 outputs:
 
 ```
 {'eprint': 'hep-ph/9905221', 'key': 'Randall:1999ee', 'id': 499284}
 ```

