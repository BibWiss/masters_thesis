[![DOI](https://zenodo.org/badge/511910541.svg)](https://zenodo.org/badge/latestdoi/511910541)

# Master's Thesis Sophie Schneider (Supplementary Material) 

## Description

This repository contains supplementary material (research data) to the master's thesis "Wie entsteht 'Stellenwert'? Eine Analyse zur Charakterisierung von Schlüsselstellen in der Literatur" ("How is key value created? Characterizing key passages in literature - an analysis"). The thesis is closely associated with the project [Was ist wichtig? Schlüsselstellen in der Literatur](https://www.projekte.hu-berlin.de/de/schluesselstellen). 

## Content

* The folder [0_extraction](0_extraction) contains two python scripts ([extract_passages.py](0_extraction/extract_passages.py), [group_passages.py](0_extraction/group_passages.py)) that need to be called from the command line in order to extract all passages to a <code>.pkl</code> file. This file can be used for the additional steps below.
* Then there are four [Jupyter Notebooks](https://jupyter.org/), one for each step in the analysis ([1_text-stats.ipynb](1_text-stats.ipynb), [2_pos.ipynb](2_pos.ipynb), [3_sentiment.ipynb](3_sentiment.ipynb), [4_summary.ipynb](4_summary.ipynb)). These notebooks access [data](data) and [functions](functions) from other files, so that the corresponding folders and their file structure must be maintained in order to work properly. More details on this can be found in the [documentation](documentation.md).
* Finally, the [vis](vis) folder contains a prototype for visualizing the measures calculated via the different notebooks. It can be downloaded individually, since everything needed for this application is contained within this folder. However, an internet connection is required, since some frameworks are called via content delivery networks.

## Credits 
* For the extraction of key passages from the provided text and data files, larger parts from the [Schlüsselstellen](https://scm.cms.hu-berlin.de/schluesselstellen) repository by [Frederik Arnold](https://scm.cms.hu-berlin.de/arnolfre) were reused.