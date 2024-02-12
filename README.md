# AFSlogscan
Python utility for analysing QSO rate progress and QSO frequency using RSGB contest summary log files (available here: https://www.rsgbcc.org/hf/ - These log files contain all submitted QSOs for a contest). Presents a simple GUI interface allowing selection of a RSGB-format summary log file and the callsigns to analyse.

Usage:
`python3 logscan.py`

Libraries required (versions from Feb 2024 confirmed compatible): 
- pandas
- matplotlib
- tkinter
---
Image of GUI log file and callsign selection dialog. Select a CSV log file, then up to 5 callsigns for analysis:

![Image of GUI app](http://46.235.224.248/main/app1.png)

Image of example output (note: the real plot is interactive, zoom by clicking the magnifying glass icon then selecting an area):

![Image of example output](http://46.235.224.248/main/app2.png)
---
Concept inspired by MATLAB code performing similar analysis by Andy G4KNO
