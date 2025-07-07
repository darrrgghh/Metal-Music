import pandas as pd
import numpy as np
from scipy.stats import f_oneway, ttest_ind
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk, scrolledtext

# loading metalvox
df = pd.read_csv('metal_vox.tsv', sep='\t', encoding='utf-8')
df['Spectral_Centroid'] = pd.to_numeric(df['Spectral_Centroid'], errors='coerce')

def group_technique(t):
    t = str(t).lower().strip()
    if t.startswith('clean'):
        return 'Clean'
    elif t.startswith('growl'):
        return 'Growling'
    elif t.startswith('scream'):
        return 'Screaming'
    else:
        return 'Other'

df['Technique_Grouped'] = df['Technique'].apply(group_technique)
df = df[df['Technique_Grouped'].isin(['Clean', 'Growling', 'Screaming'])]
df = df.dropna(subset=['Spectral_Centroid'])

# Descriptive statistics
stats = df.groupby('Technique_Grouped')['Spectral_Centroid'].agg(['mean','std','count','min','max'])
growl = df[df['Technique_Grouped']=='Growling']['Spectral_Centroid']
scream = df[df['Technique_Grouped']=='Screaming']['Spectral_Centroid']
clean = df[df['Technique_Grouped']=='Clean']['Spectral_Centroid']
f_stat, p_anova = f_oneway(growl, scream, clean)
t_stat, p_ttest = ttest_ind(growl, scream)
tukey = pairwise_tukeyhsd(df['Spectral_Centroid'], df['Technique_Grouped'])

# plots' window settings
root = tk.Tk()
root.title("Spectral Centroid Analysis (METALVOX)")
tab_parent = ttk.Notebook(root)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="Boxplot")
tab_parent.add(tab2, text="Histogram")
tab_parent.pack(expand=1, fill='both')

# box plot
fig1, ax1 = plt.subplots(figsize=(7, 5))
data = [clean, growl, scream]
labels = ['Clean', 'Growling', 'Screaming']
ax1.boxplot(data, tick_labels=labels, patch_artist=True)
ax1.set_ylabel("Spectral Centroid (Hz)")
ax1.set_title("Spectral Centroid by Technique (METALVOX)")
canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
canvas1.draw()
canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=1)
toolbar_frame1 = tk.Frame(tab1)
toolbar_frame1.pack()
toolbar1 = NavigationToolbar2Tk(canvas1, toolbar_frame1)
toolbar1.update()

# histogram
fig2, ax2 = plt.subplots(figsize=(7, 5))
bins = np.linspace(df['Spectral_Centroid'].min(), df['Spectral_Centroid'].max(), 30)
ax2.hist([clean, growl, scream], bins=bins, label=labels, alpha=0.7, stacked=False)
ax2.set_xlabel("Spectral Centroid (Hz)")
ax2.set_ylabel("Count")
ax2.set_title("Histogram of Spectral Centroid (METALVOX)")
ax2.legend()
canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
canvas2.draw()
canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=1)
toolbar_frame2 = tk.Frame(tab2)
toolbar_frame2.pack()
toolbar2 = NavigationToolbar2Tk(canvas2, toolbar_frame2)
toolbar2.update()

# statistics' window settings
output = ""
output += "Descriptive statistics by technique:\n"
output += stats.to_string()
output += "\n\n"
output += f"ANOVA:\nF = {f_stat:.3f}, p = {p_anova:.3g}\n"
output += "\n"
output += f"T-test Growling vs Screaming:\nt = {t_stat:.3f}, p = {p_ttest:.3g}\n"
output += "\n"
output += "Tukey HSD post-hoc test:\n"
output += str(tukey.summary())
output += "\n"

def copy_selection(event):
    try:
        stats_text.event_generate("<<Copy>>")
    except:
        pass

def popup_menu(event):
    menu = tk.Menu(stats_win, tearoff=0)
    menu.add_command(label="Copy", command=lambda: stats_text.event_generate("<<Copy>>"))
    menu.tk_popup(event.x_root, event.y_root)

stats_win = tk.Toplevel(root)
stats_win.title("Statistical Results")
stats_text = scrolledtext.ScrolledText(stats_win, width=90, height=30, wrap="word")
stats_text.pack(fill=tk.BOTH, expand=1)
stats_text.insert(tk.END, output)
stats_text.config(state=tk.NORMAL)
stats_text.bind("<Button-3>", popup_menu)
stats_text.bind("<Control-Button-1>", popup_menu)
root.mainloop()