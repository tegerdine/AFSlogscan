#!/usr/bin/env python
"""\
Read in a RSGB contest result CSV file and plot QSO count and freq vs. time

Usage: python logscan.py

G0LRD, 2024-02-04
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

NUM_CALLS_SELECTABLE = 8


def csv_read_call_list(filename):
    df = pd.read_csv(filename, skiprows=1)
    return list(df.Entrant.unique())


def csv_analyse(filename, wanted_calls):
    df = pd.read_csv(filename, skiprows=1)
    _, ax = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    for target in wanted_calls:
        df_call = df.loc[(df["Entrant"] == target)]
        times = pd.to_datetime(
            df_call["Date"] + " " + df_call["Time"], format="%d/%m/%y %H:%M"
        )
        ax[0].plot(times, df_call["SnTX"], label=target, marker=".", linewidth=1)
        ax[1].plot(times, df_call["Frequency"], label=target, marker=".", linewidth=1)

    ax[0].xaxis.set_major_formatter(DateFormatter("%H:%M"))
    ax[0].set_xlabel("Time")
    ax[0].set_title(f"{filename}", fontsize=8, wrap=True)
    ax[0].legend(loc="upper right", bbox_to_anchor=(1.21, 0.5))
    ax[0].set_ylabel("QSO count")
    ax[1].set_ylabel("Frequency / kHz")
    ax[0].grid()
    ax[1].grid()
    plt.tight_layout()
    plt.subplots_adjust(hspace=0)
    plt.show()
    return


def show_gui():
    global call_list
    root = tk.Tk()
    root.title("LogScan")
    root.geometry(f"320x{100+(NUM_CALLS_SELECTABLE*26)}")
    root.resizable(False, False)

    call_list = []

    def open_file():
        newfile = filedialog.askopenfile(
            initialdir=".",
            title="Select CSV file",
            filetypes=(("CSV files", "*.csv"), ("all files", "*.*")),
        )
        cur_filename.set(newfile.name)
        call_list = csv_read_call_list(newfile.name)
        call_list.insert(0, "")  # add a blank call to allow de-selection
        for i in range(NUM_CALLS_SELECTABLE):
            combo[i]["values"] = list(call_list)
            combo[i].set("")

    button = tk.Button(root, text="Select CSV File", command=open_file)
    button.pack(expand=True)

    cur_filename = tk.StringVar()
    cur_filename.set("<no file selected>")

    mylabel = tk.Label(
        root, textvariable=cur_filename, wraplength=290, justify="center"
    )
    mylabel.pack(expand=True)

    call_sel = []
    combo = []
    for i in range(NUM_CALLS_SELECTABLE):
        call_sel.append(tk.StringVar(root))
        call_sel[i].set("")
        combo.append(ttk.Combobox(root, textvariable=call_sel[i]))
        combo[i]["values"] = ""
        combo[i]["state"] = "readonly"
        combo[i].pack(expand=True)

    def ok():
        if cur_filename.get() == "<no file selected>":
            return
        calls = []
        for i in range(NUM_CALLS_SELECTABLE):
            calls.append(call_sel[i].get())
        calls = list(dict.fromkeys(calls))  # remove dups
        calls[:] = [item for item in calls if item != ""]  # remove blanks
        if len(calls) > 0:
            csv_analyse(cur_filename.get(), calls)

    button = tk.Button(root, text="Create Plot", command=ok)
    button.pack(expand=True)
    tk.mainloop()


if __name__ == "__main__":
    show_gui()
