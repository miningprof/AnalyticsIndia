import sys, os
from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, 
                             QMessageBox, QTableView, QTextEdit, QSplitter, QPushButton, 
                             QComboBox, QLabel, QDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant

from src.utils.data_handler import load_data_from_file
from src.core.descriptive_stats import calculate_descriptive_stats
from src.ui.dialogs.help_dialog import HelpDialog
from src.utils.plotting import create_histogram_plot, save_plot_as_png
from src.utils.report_generator import generate_pdf_report

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

class PandasModel(QAbstractTableModel):
    def __init__(self, dataframe: pd.DataFrame, parent=None):
        super().__init__(parent)
        self._dataframe = dataframe

    def rowCount(self, parent=None):
        return self._dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._dataframe.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            value = self._dataframe.iloc[index.row(), index.column()]
            return "NA" if pd.isna(value) else str(value)
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal: return str(self._dataframe.columns[section])
            if orientation == Qt.Vertical: return str(self._dataframe.index[section])
        return QVariant()
    
    def update_data(self, dataframe: pd.DataFrame):
        self.beginResetModel()
        self._dataframe = dataframe
        self.endResetModel()

class MainWindow(QMainWindow):
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.current_dataframe = None
        self.current_file_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Data Analytics Software")
        self.setGeometry(50, 50, 1200, 800)
        # self.setWindowIcon(QIcon(os.path.join('src', 'ui', 'assets', 'icons', 'app_icon.png'))) # Add an icon file

        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.statusBar().showMessage("Ready")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        self.controls_panel = QWidget()
        self.controls_layout = QHBoxLayout(self.controls_panel)
        self.column_label = QLabel("Select Column for Analysis:")
        self.column_combo = QComboBox()
        self.column_combo.setMinimumWidth(200)
        self.run_desc_stats_button = QPushButton("Run Descriptive Stats")
        self.run_desc_stats_button.clicked.connect(self.run_descriptive_statistics)
        self.run_hist_button = QPushButton("Plot Histogram")
        self.run_hist_button.clicked.connect(self.plot_histogram)
        
        self.controls_layout.addWidget(self.column_label)
        self.controls_layout.addWidget(self.column_combo)
        self.controls_layout.addWidget(self.run_desc_stats_button)
        self.controls_layout.addWidget(self.run_hist_button)
        self.controls_layout.addStretch()
        main_layout.addWidget(self.controls_panel)

        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)

        self.table_view = QTableView()
        self.splitter.addWidget(self.table_view)

        self.right_panel_splitter = QSplitter(Qt.Vertical)
        self.results_text_edit = QTextEdit()
        self.results_text_edit.setReadOnly(True)
        self.right_panel_splitter.addWidget(self.results_text_edit)

        self.plot_canvas_widget = QWidget()
        self.plot_layout = QVBoxLayout(self.plot_canvas_widget)
        self.figure = Figure(figsize=(5,3), dpi=100)
        self.plot_canvas = FigureCanvas(self.figure)
        self.plot_layout.addWidget(self.plot_canvas)
        self.right_panel_splitter.addWidget(self.plot_canvas_widget)

        self.splitter.addWidget(self.right_panel_splitter)
        self.splitter.setSizes([700, 500])
        self.right_panel_splitter.setSizes([200,300])
        
        self.set_controls_enabled(False)

    def create_actions(self):
        self.open_action = QAction("&Open Data File...", self, shortcut='Ctrl+O', triggered=self.open_file_dialog)
        self.save_report_action = QAction("&Save Report as PDF...", self, triggered=self.save_pdf_report)
        self.save_plot_png_action = QAction("Save Plot as PNG...", self, triggered=self.save_current_plot_as_png)
        self.exit_action = QAction("E&xit", self, shortcut='Ctrl+Q', triggered=self.close)
        self.help_action = QAction("&View Help", self, triggered=self.open_help_dialog)
        self.about_action = QAction("&About", self, triggered=self.show_about_dialog)

    def create_menus(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_report_action)
        file_menu.addAction(self.save_plot_png_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        
        # Analysis Menu (Simplified)
        analysis_menu = menubar.addMenu("&Analysis")
        # Actions for specific analyses can be added here if not covered by buttons

        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self.help_action)
        help_menu.addAction(self.about_action)

    def create_toolbar(self):
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.addAction(self.open_action)
        # Add other common actions if needed

    def set_controls_enabled(self, enabled):
        self.column_combo.setEnabled(enabled)
        self.run_desc_stats_button.setEnabled(enabled)
        self.run_hist_button.setEnabled(enabled)
        self.save_report_action.setEnabled(enabled)
        self.save_plot_png_action.setEnabled(enabled)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 
                                                 "Open Data File", 
                                                 self.settings_manager.get_setting('last_opened_dir', os.path.expanduser("~")), 
                                                 "Data Files (*.csv *.xlsx *.ods);;CSV (*.csv);;Excel (*.xlsx);;OpenDocument Spreadsheet (*.ods)")
        if file_path:
            try:
                self.current_dataframe = load_data_from_file(file_path)
                self.current_file_path = file_path
                self.settings_manager.set_setting('last_opened_dir', os.path.dirname(file_path))
                self.statusBar().showMessage(f"Data loaded: {os.path.basename(file_path)}")
                
                model = PandasModel(self.current_dataframe)
                self.table_view.setModel(model)
                self.table_view.resizeColumnsToContents()

                self.column_combo.clear()
                self.column_combo.addItems(self.current_dataframe.columns)
                self.set_controls_enabled(True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not load the selected file:\n{str(e)}")
                self.current_dataframe = None
                self.current_file_path = None
                self.set_controls_enabled(False)
                self.column_combo.clear()
                if self.table_view.model(): self.table_view.model().update_data(pd.DataFrame())

    def get_selected_column_data(self):
        if self.current_dataframe is None or self.column_combo.count() == 0:
            QMessageBox.warning(self, "Warning", "No data loaded or no column available.")
            return None
        selected_column_name = self.column_combo.currentText()
        if not selected_column_name:
             QMessageBox.warning(self, "Warning", "Please select a column for analysis.")
             return None
        
        column_data = self.current_dataframe[selected_column_name]
        if not pd.api.types.is_numeric_dtype(column_data):
            QMessageBox.warning(self, "Warning", f"Column '{selected_column_name}' is not numeric and cannot be used for this analysis.")
            return None
        return column_data.dropna()

    def run_descriptive_statistics(self):
        column_data = self.get_selected_column_data()
        if column_data is None or column_data.empty:
            if column_data is not None: QMessageBox.information(self, "Information", "Selected column is empty after removing NA values.")
            return

        stats_results = calculate_descriptive_stats(column_data)
        results_str = f"Descriptive Statistics ({self.column_combo.currentText()}):\n"
        results_str += "-"*30 + "\n"
        for key, value in stats_results.items():
            if isinstance(value, (int, float)) and not np.isnan(value):
                results_str += f"  {key}: {value:.3f}\n"
            else:
                results_str += f"  {key}: {value}\n"
        self.results_text_edit.setText(results_str)

    def plot_histogram(self):
        column_data = self.get_selected_column_data()
        if column_data is None or column_data.empty:
            if column_data is not None: QMessageBox.information(self, "Information", "Selected column is empty after removing NA values.")
            return
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        plot_title = f"Histogram of {self.column_combo.currentText()}"
        create_histogram_plot(ax, column_data, title=plot_title, xlabel="Value", ylabel="Frequency")
        self.plot_canvas.draw()

    def save_current_plot_as_png(self):
        if not self.figure.get_axes():
            QMessageBox.information(self, "Information", "There is no plot to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Plot As PNG", 
                                                 self.settings_manager.get_setting('last_saved_plot_dir', os.path.expanduser("~")), 
                                                 "PNG (*.png)")
        if file_path:
            try:
                save_plot_as_png(self.figure, file_path)
                self.settings_manager.set_setting('last_saved_plot_dir', os.path.dirname(file_path))
                self.statusBar().showMessage(f"Plot saved: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save the plot:\n{str(e)}")

    def save_pdf_report(self):
        if self.current_dataframe is None:
            QMessageBox.warning(self, "Warning", "No data loaded to generate a report.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Report As PDF", 
                                                 self.settings_manager.get_setting('last_saved_report_dir', os.path.expanduser("~")), 
                                                 "PDF (*.pdf)")
        if file_path:
            report_data = {
                'title': "Data Analysis Report",
                'intro_text': "This document summarizes the results of the data analysis.",
                'results_summary': self.results_text_edit.toPlainText(),
                'plot_figure': self.figure if self.figure.get_axes() else None
            }
            try:
                from src.utils.report_generator import generate_pdf_report # Ensure fresh import
                generate_pdf_report(report_data, file_path)
                self.settings_manager.set_setting('last_saved_report_dir', os.path.dirname(file_path))
                self.statusBar().showMessage(f"Report saved: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save the report:\n{str(e)}")

    def open_help_dialog(self):
        dialog = HelpDialog(self)
        dialog.exec_()

    def show_about_dialog(self):
        QMessageBox.about(self, "About Data Analytics Software",
                          "Data Analytics Software for Students\nVersion: 0.1.0 (English Only)\n\nDeveloped to help learn probability and statistics.")
    
    def closeEvent(self, event):
        self.settings_manager.save_settings()
        super().closeEvent(event)
