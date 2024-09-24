from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog,
    QMessageBox,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QGridLayout,
    QLabel,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from pdf_scrape import PdfScraper


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My PDF Scaper")

        self.resize(640, 600)
        self.setMinimumWidth(600)

        self.create_ui_widgets()

        self.create_ui_elements()

    def create_ui_widgets(self):
        """Creates the main widgets for the layout of the app"""

        # self.setStyleSheet("border: 1px solid white;")

        # Create the central widget
        self.central_widget = QWidget()
        self.central_widget_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_widget_layout)

        # Create main widget
        self.main_widget = QWidget()
        self.main_widget_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_widget_layout)
        self.central_widget_layout.addWidget(self.main_widget)

        # Create top widget
        self.top_widget = QWidget()
        self.top_widget.setMaximumHeight(100)
        self.top_widget_layout = QVBoxLayout()
        self.top_widget.setLayout(self.top_widget_layout)
        self.main_widget_layout.addWidget(self.top_widget)

        # Create middle widget
        self.middle_widget = QWidget()
        self.middle_widget_layout = QGridLayout()
        self.middle_widget.setLayout(self.middle_widget_layout)
        self.main_widget_layout.addWidget(self.middle_widget)

        # Create bottom widget
        self.bottom_widget = QWidget()
        self.bottom_widget.setMinimumHeight(400)
        self.bottom_widget_layout = QVBoxLayout()
        self.bottom_widget.setLayout(self.bottom_widget_layout)
        self.main_widget_layout.addWidget(self.bottom_widget)

        self.setCentralWidget(self.central_widget)

    def create_ui_elements(self):
        """Create the ui elements (controls etc )"""

        # Create top widget label
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignCenter)
        # Info string
        info_string = "Scrape order numbers from two pdfs (accounting report & schedule report)\nthen output missings orders below."
        # Set the info string to label text
        self.info_label.setText(info_string)
        # Add widget to layout
        self.top_widget_layout.addWidget(self.info_label)

        # Create middle widget controls
        self.pdf_1_label = QLabel("Accounting report:")
        self.pdf_2_label = QLabel("Schedule report:")
        self.pdf_1_filepath = QLineEdit()
        self.pdf_2_filepath = QLineEdit()
        self.pdf_1_button = QPushButton("Select")
        self.pdf_2_button = QPushButton("Select")
        self.scrape_button = QPushButton("Scrape")
        self.copy_clipboard_button = QPushButton("Copy to Clipboard")
        # Add widgets to layout
        # File path 1
        self.middle_widget_layout.addWidget(self.pdf_1_label, 0, 0)
        self.middle_widget_layout.addWidget(self.pdf_1_filepath, 1, 0)
        self.middle_widget_layout.addWidget(self.pdf_1_button, 1, 1)
        # File path 2
        self.middle_widget_layout.addWidget(self.pdf_2_label, 2, 0)
        self.middle_widget_layout.addWidget(self.pdf_2_filepath, 3, 0)
        self.middle_widget_layout.addWidget(self.pdf_2_button, 3, 1)
        # Scrape button
        self.middle_widget_layout.addWidget(self.scrape_button, 4, 0, 1, 2)
        # Clipboard button
        self.middle_widget_layout.addWidget(self.copy_clipboard_button, 5, 0, 1, 2)

        # Set button click events
        self.pdf_1_button.clicked.connect(self.click_pdf_1_button)
        self.pdf_2_button.clicked.connect(self.click_pdf_2_button)
        self.scrape_button.clicked.connect(self.click_scrape_button)
        self.copy_clipboard_button.clicked.connect(self.copy_to_clipboard)

        # Create bottom widget label
        self.output_label = QLabel("Output will generate here")
        self.output_label.setWordWrap(True)
        self.output_label.setAlignment(Qt.AlignCenter)
        self.bottom_widget_layout.addWidget(self.output_label)

    def click_pdf_1_button(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select a PDF File",
            "",
            "PDF Files (*.pdf);;All Files (*)",
            options=options,
        )
        if file_name:
            self.pdf_1_filepath.setText(file_name)

    def click_pdf_2_button(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select a PDF File",
            "",
            "PDF Files (*.pdf);;All Files (*)",
            options=options,
        )
        if file_name:
            self.pdf_2_filepath.setText(file_name)

    def click_scrape_button(self):
        filepath_1 = self.pdf_1_filepath.text()
        filepath_2 = self.pdf_2_filepath.text()
        if filepath_1 == "" or filepath_2 == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("One or more file path's have not been selected")
            msg.setIcon(QMessageBox.Warning)
            msg.ButtonRole(QMessageBox.Ok)
            msg.exec_()
        else:
            try:
                pdf_scrape = PdfScraper(filepath_1, filepath_2)
                output = pdf_scrape.out_put_text()
                self.output_label.setText(output)

            except:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Srcape failed, please check file paths are correct")
                msg.setIcon(QMessageBox.Warning)
                msg.ButtonRole(QMessageBox.Ok)
                msg.exec_()

    def copy_to_clipboard(self):
        if self.output_label.text() == "Output will generate here":
            msg = QMessageBox()
            msg.setWindowTitle("Clipboard error")
            msg.setText("There is nothing to copy to the clipboard.")
            msg.setIcon(QMessageBox.Warning)
            msg.ButtonRole(QMessageBox.Ok)
            msg.exec_()
        else:
            clipboard = QApplication.clipboard()

            clipboard.setText(self.output_label.text())
