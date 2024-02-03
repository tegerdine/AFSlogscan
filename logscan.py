#!/usr/bin/env python
"""\
Read in a RSGB AFS contest result CSV file and plot QSO count and freq vs. time

Usage: python logscan.py [CSV filename] callsign1 callsign2 ... callsignN

G0LRD, 2024-02-03
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def csv_print_callsigns(filename):
    df = pd.read_csv(filename, skiprows = 1)
    call_list = df.Entrant.unique()
    print(str(call_list))
    return

def csv_analyse(filename, wanted_calls):
    df = pd.read_csv(filename, skiprows = 1)
    _, ax = plt.subplots(2, 1, figsize=(9, 6), sharex = True)
    for target in wanted_calls:
        df_call = df.loc[(df["Entrant"] == target)]
        if len(df_call) == 0: 
            sys.exit(f'Callsign {target} not found in file')
        times = pd.to_datetime(df_call["Date"] + " " + df_call["Time"], format = "%d/%m/%y %H:%M")
        ax[0].plot(times, df_call["SnTX"], label = target, marker = ".", linewidth = 1)
        ax[1].plot(times, df_call["Frequency"], label = target, marker = ".", linewidth = 1)

    ax[0].xaxis.set_major_formatter(DateFormatter("%H:%M"))
    ax[0].set_xlabel("Time")
    ax[0].set_title(f"{filename}")
    ax[0].legend(loc="upper right", bbox_to_anchor = (1.21, 0.5))
    ax[0].set_ylabel("QSO count")
    ax[1].set_ylabel("Frequency / kHz")
    ax[0].grid()
    ax[1].grid()
    plt.tight_layout()
    plt.subplots_adjust(hspace = 0)
    plt.show()
    return


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage 1: python logscan.py [RSGB csv filename]")
        print("Prints a list of all entrant callsigns in CSV file\n")
        print("Usage 2: python logscan.py [RSGB csv filename] callsign1 callsign2 ... callsignN")
        print("Creates plot of QSO count and frequency for chosen callsigns\n")
    elif len(sys.argv) == 2:
        csv_print_callsigns(sys.argv[1])
    elif len(sys.argv) > 2:
        filename = sys.argv[1]
        wanted_calls = []
        for i in range(2, len(sys.argv)):
            wanted_calls.append(sys.argv[i].upper())
        csv_analyse(filename, wanted_calls)
