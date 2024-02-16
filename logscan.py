#!/usr/bin/env python3
"""
Read in a RSGB contest result CSV file and plot QSO count and freq vs. time
for selected callsigns.

Usage: python3 logscan.py

G0LRD, 2024-02-04
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# define the number of callsign drop-down boxes to appear in the UI
NUM_CALLS_SELECTABLE = 5

# define the width in pixels of UI
GUI_WIDTH = 320

# function to analyse a CSV logfile for a list of callsigns
def csv_analyse(filename, wanted_calls):
    df = pd.read_csv(filename, skiprows = 1)
    _, ax = plt.subplots(2, 1, figsize=(9, 6), sharex = True)
    
    for target in wanted_calls:
        df_call = df.loc[(df["Entrant"] == target)]
        times = pd.to_datetime(df_call["Date"] + " " + df_call["Time"], format = "%d/%m/%y %H:%M")
        ax[0].plot(times, df_call["SnTX"], label = target, marker = "D", ms = 3, linewidth = 0.5)
        if "Frequency" in df_call.columns: # hack to make RSGB VHF logs sort-of work too
            Freq_field="Frequency"
            y_label = "Frequency / kHz"
        else:
            Freq_field="Band"
            y_label = "Band / m"
        ax[1].plot(times, df_call[Freq_field], label = target, marker = "D", ms = 3, linewidth = 0.5)
    
    ax[0].xaxis.set_major_formatter(DateFormatter("%H:%M"))
    ax[0].set_xlabel("Time")
    ax[0].set_title(f"{filename}", fontsize = 8, wrap = True)
    ax[0].legend(loc="upper right", bbox_to_anchor=(1.21, 0.5))
    ax[0].set_ylabel("QSO count")
    ax[0].yaxis.get_major_locator().set_params(integer=True)
    ax[0].grid()
    ax[1].grid()
    ax[1].set_ylabel(y_label)
    
    if Freq_field == "Frequency": # colour and label amateur HF contest bands
        ham_bands=[[1800,1999,'160m'], [3500,3799,'80m'], [7000,7199,'40m'], [14000,14349,'20m'], [21000,21449,'15m'], [28000,28999,'10m']]
        for band in ham_bands:
            ax[1].axhspan(band[0], band[1], facecolor='green', alpha=0.25)
            _, xmax = ax[1].get_xlim()
            ax[1].text(xmax, band[0], band[2], fontsize=11, va='center')
   
    plt.tight_layout()
    plt.subplots_adjust(hspace = 0.1)
    plt.show()
    return

# function to manage the tkinter GUI
def show_gui():
    root = tk.Tk()
    root.title("LogScan")
    root.geometry(f"{GUI_WIDTH}x{100+(NUM_CALLS_SELECTABLE*26)}")
    root.resizable(False, False)

    def open_file():
        newfile = filedialog.askopenfile(
            initialdir=".",
            title="Select CSV file",
            filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
        if newfile != None:
            cur_filename.set(newfile.name)
            df = pd.read_csv(newfile.name, skiprows = 1)
            call_list = list(df.Entrant.unique())
            call_list.insert(0, "")  # add a blank call to allow de-selection in UI
            for i in range(NUM_CALLS_SELECTABLE):
                combo[i]["values"] = call_list
                combo[i].set("")
        return

    def close_all():
        plt.close('all')
        root.destroy()

    button = tk.Button(root, text="Select CSV File", command = open_file)
    button.pack(expand = True)

    cur_filename = tk.StringVar()
    cur_filename.set("<no file selected>")

    mylabel = tk.Label(root, textvariable = cur_filename, wraplength = GUI_WIDTH - 20, justify = "center")
    mylabel.pack(expand = True)

    call_sel = []
    combo = []
    for i in range(NUM_CALLS_SELECTABLE):
        call_sel.append(tk.StringVar(root))
        call_sel[i].set("")
        combo.append(ttk.Combobox(root, textvariable = call_sel[i]))
        combo[i]["values"] = ""
        combo[i]["state"] = "readonly"
        combo[i].pack(expand = True)

    def plot():
        if cur_filename.get() == "<no file selected>": return
        calls = []
        for i in range(NUM_CALLS_SELECTABLE): calls.append(call_sel[i].get())
        calls = list(dict.fromkeys(calls))  # remove dups
        calls[:] = [item for item in calls if item != ""]  # remove blanks
        if len(calls) > 0: csv_analyse(cur_filename.get(), calls)

    button = tk.Button(root, text="Create Plot", command = plot)
    button.pack(expand = True)
    root.protocol("WM_DELETE_WINDOW", close_all)
    tk.mainloop()


if __name__ == "__main__":
    show_gui()
