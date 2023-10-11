import pandas as pd
import chardet
import tkinter as tk
from tkinter import filedialog


def calculate(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())

    df = pd.read_csv(file_path, delimiter=";", encoding=result["encoding"])

    df['Year'] = pd.to_datetime(df['Dato']).dt.year

    # Add new column with every second year
    dates = pd.date_range(start=df['Dato'].min(), end=df['Dato'].max(), freq='2Y')
    df['Year2'] = pd.DatetimeIndex(df['Dato']).year.maDDp(lambda x: dates[(dates.year >= x)].min().year)

    maxflow = df['Vandføring'].max()
    meanflow = df['Vandføring'].mean()
    absminflow = df['Vandføring'].min()
    yearly_minflow_mean = df.groupby('Year')['Vandføring'].min().mean()
    yearly_maxflow_mean = df.groupby('Year')['Vandføring'].max().mean()
    yearly_minflow_mean_2year = df.groupby('Year2')['Vandføring'].min().mean()
    yearly_maxflow_mean_2year = df.groupby('Year2')['Vandføring'].max().mean()

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Maksimum vandføring: {maxflow:.2f} l/s\n\n")
    result_text.insert(tk.END, f"Gennemsnitlig vandføring: {meanflow:.2f} l/s\n\n")
    result_text.insert(tk.END, f"Absolut minimum vandføring: {absminflow:.2f} l/s\n\n")
    result_text.insert(tk.END, f"Gennemsnitlig minimumsvandføring pr. år: {yearly_minflow_mean:.2f} l/s\n\n")
    result_text.insert(tk.END, f"Gennemsnitlig maksimum vandføring pr. år: {yearly_maxflow_mean:.2f} l/s\n\n")
    result_text.insert(tk.END, f"Gennemsnitlig minimum vandføring for hvert andet år: {yearly_minflow_mean_2year:.2f} l/s\n\n")
    result_text.insert(tk.END, f"Gennemsnitlig maksimum vandføring for hvert andet år: {yearly_maxflow_mean_2year:.2f} l/s\n\n")


def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        calculate(file_path)


# Create GUI
root = tk.Tk()
root.title("Vandføring")
root.geometry("500x500")

# Create title label
title_label = tk.Label(root, text="Resultater", font=("Helvetica", 20, "bold"))
title_label.pack(pady=10)

# Create button
calculate_button = tk.Button(root, text="Vælg fil og beregn", command=open_file, font=("Helvetica", 14))
calculate_button.pack(pady=10)

# Create result text
result_text = tk.Text(root, height=20, width=50, font=("Helvetica", 12))
result_text.pack(padx=10, pady=10)

root.mainloop()
