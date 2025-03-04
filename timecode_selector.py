#!/usr/bin/env python3
"""
This app is a random timecode selector used to choose a timecode from a song in our table of musical examples for research purposes.
It randomly selects an excerpt within a specified time range.
The ui is simple and consist of several rows.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random

class TimecodeSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Timecode Selector")
        # Main window. Feel free to adjust any of these parameters.
        self.geometry("375x205")
        self.resizable(True, True)
        self.label_font = ("Arial", 13, "bold")
        self.entry_font = ("Arial", 13)
        self.button_font = ("Arial", 14, "bold")
        self.result_font = ("Arial", 16, "bold")
        self._create_widgets()

    def _create_widgets(self):
        # Row 1: "Enter the duration" label
        duration_label = tk.Label(self, text="Enter the duration:", font=self.label_font, fg='green')
        duration_label.grid(row=2, column=0, sticky="w", padx=(10, 5))

        # Row 2: Minutes, Seconds fields
        # Minutes
        self.minutes_var = tk.StringVar(value="03")
        minutes_entry = tk.Entry(self, textvariable=self.minutes_var, width=3, font=self.entry_font, justify="center")
        minutes_entry.grid(row=2, column=1, padx=(10,5), sticky="w")
        minutes_label = tk.Label(self, text="mins", font=self.label_font, fg='green')
        minutes_label.grid(row=2, column=2, sticky="w")
        # Seconds
        self.seconds_var = tk.StringVar(value="25")
        seconds_entry = tk.Entry(self, textvariable=self.seconds_var, width=3, font=self.entry_font, justify="center")
        seconds_entry.grid(row=2, column=3, padx=(10,5), sticky="w")
        seconds_label = tk.Label(self, text="sec", font=self.label_font, fg='green')
        seconds_label.grid(row=2, column=4, sticky="w")

        # Row 3: skip first % label + entry
        skip_label = tk.Label(self, text="skip first", font=self.label_font, fg='green')
        skip_label.grid(row=3, column=0, sticky="e", padx=(10,5))
        self.skip_percent_var = tk.StringVar(value="30")
        skip_entry = tk.Entry(self, textvariable=self.skip_percent_var, width=3, font=self.entry_font, justify="center")
        skip_entry.grid(row=3, column=1, sticky="w")
        skip_label2 = tk.Label(self, text="% of the track", font=self.label_font, fg='green')
        skip_label2.grid(row=3, column=2, columnspan=2, sticky="w")

        # Row 4: required length label + length entry + time units
        length_label = tk.Label(self, text="required length", font=self.label_font, fg='green')
        length_label.grid(row=4, column=0, sticky="e", padx=(10,5))
        self.length_var = tk.StringVar(value="12")
        length_entry = tk.Entry(self, textvariable=self.length_var, width=4, font=self.entry_font, justify="center")
        length_entry.grid(row=4, column=1, sticky="w")
        self.unit_var = tk.StringVar(value="sec")
        unit_choices = ["min", "sec"]
        unit_menu = ttk.OptionMenu(self, self.unit_var, "sec", *unit_choices)
        unit_menu.config(width=4)
        unit_menu.grid(row=4, column=2, sticky="w", padx=(10,0))

        # Row 5: "Request Timecode" button
        request_btn = tk.Button(self, text="Request timecode", font=self.button_font, command=self._calculate_timecode)
        request_btn.grid(row=5, column=0, columnspan=5, pady=(10,5))

        # Row 6: "Your timecode selection" label
        self.result_label = tk.Label(self, text="Your timecode selection:", font=self.result_font, fg="red")
        self.result_label.grid(row=6, column=0, columnspan=5, pady=(5,5))
        self.columnconfigure(5, weight=1)
    def _calculate_timecode(self):
        # this function generates a random timecode range based on the user inputs (minutes, seconds, skip %, excerpt length)
        try:
            # total duration from minutes, seconds to total_seconds
            mins = int(self.minutes_var.get())
            secs = int(self.seconds_var.get())
            total_seconds = mins * 60 + secs
            if total_seconds <= 0:
                messagebox.showwarning("Invalid Duration", "Please enter a valid total duration.")
                return
            # skip percentage
            skip_percent = float(self.skip_percent_var.get())
            if not (1 <= skip_percent <= 100):
                messagebox.showwarning("Invalid Percent", "Skip percent must be between 1 and 100.")
                return
            skip_time = (skip_percent / 100.0) * total_seconds
            # required length + unit
            length_val = float(self.length_var.get())
            unit = self.unit_var.get()
            # convert excerpt length into seconds
            if unit == "min":
                excerpt_length = length_val * 60
            else:  # "sec"
                excerpt_length = length_val
            if excerpt_length <= 0:
                messagebox.showwarning("Invalid Length", "Required length must be greater than 0.")
                return
            # get random start time within the allowed range
            max_start = total_seconds - excerpt_length
            if skip_time >= max_start:
                messagebox.showwarning("Invalid Range",
                                       "Skipping too much or excerpt too long to fit in the track.")
                return
            start_time = random.uniform(skip_time, max_start)
            end_time = start_time + excerpt_length
            # Convert start and end times to minutes and seconds
            start_minutes = int(start_time // 60)
            start_seconds = int(start_time % 60)
            end_minutes = int(end_time // 60)
            end_seconds = int(end_time % 60)
            # preparing output
            start_str = f"{start_minutes}:{start_seconds:02d}"
            end_str = f"{end_minutes}:{end_seconds:02d}"
            self.result_label.config(text=f"Your timecode selection:\n{start_str} - {end_str}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for minutes, seconds, etc.")

def main():
    app = TimecodeSelector()
    app.mainloop()
if __name__ == "__main__":
    main()