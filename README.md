# BiBminer

A module that extracts the citations from a LaTeX file and generates the corresponding *.bib* file automatically. The citation id inside *\cite{...}* in the .tex must be in a format compatible with **HEP Inspire**. The supported identifers are: arxiv preprint number (e.g. *2022.1234* or *hep-th/123456*, ... ), hep inspire id, or the bibtex id (e.g. *Witten:123ab*). 
