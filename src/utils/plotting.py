import matplotlib.pyplot as plt
import numpy as np

def create_histogram_plot(ax, data, bins='auto', title="Histogram", xlabel="Value", ylabel="Frequency", color='skyblue', edgecolor='black'):
    if data is None or len(data) == 0:
        ax.text(0.5, 0.5, "No data to plot", ha='center', va='center', transform=ax.transAxes); ax.set_title(title); return
    ax.hist(data, bins=bins, color=color, edgecolor=edgecolor)
    ax.set_title(title); ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.grid(axis='y', alpha=0.75)

def save_plot_as_png(figure, output_path):
    if not figure or not output_path: raise ValueError("Figure and output path must be provided.")
    try: figure.savefig(output_path, format='png', dpi=300, bbox_inches='tight')
    except Exception as e: raise Exception(f"Error saving plot to {output_path}: {e}")
