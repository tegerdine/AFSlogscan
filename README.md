# AFSlogscan
Python utility for analysing RSGB contest log files (available here: https://www.rsgbcc.org/hf/). These contain all submitted QSOs for a contest.

Usage: python logscan.py \<filename of CSV\> \<list of entrant callsigns\>

e.g. python logscan.py RSGB_AFS_80m-40m_Contests_Phone_240120_80m-40m_OpenLogQSOs.csv M4T G4PIQ G4BUO G5PI G4KNO
 
If you only provide the CSV filename then it lists all the unique entrant callsigns. If you provide one or more entrant callsigns as well, it produces plots showing QSO count and QSO Frequency vs. Time. I tried it on the RSGB SSB, CW and DATA results files and it seems to work fine on them all. It produces an interactive plot that you can zoom and pan as you see fit using the controls at the bottom, for example to zoom click the magnifying glass then select an area of either upper or lower plot.
