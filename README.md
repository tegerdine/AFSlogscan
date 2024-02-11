# AFSlogscan
Python utility for analysing QSO rate progress and QSO frequency using RSGB contest summary log files (available here: https://www.rsgbcc.org/hf/ - These log files contain all submitted QSOs for a contest). Presents a simple GUI interface allowing selection of a RSGB-format summary log file and the callsigns to analyse.

Usage:
`python3 logscan.py`

Libraries required (versions from Feb 2024 confirmed compatible): 
- pandas
- matplotlib
- tkinter
---
GUI log file and callsign selection:

![Image of GUI app](http://46.235.224.248/main/app1.png)

Example output:

![Image of example output](http://46.235.224.248/main/app2.png)
---
Concept inspired by MATLAB code performing similar analysis by Andy G4KNO
