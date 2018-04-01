import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import GenerateOutput

class GUI:
    def __init__(self):
        self.initUI()

    var = 0
    str1 = ""

    def initUI(self):
        app = QApplication(sys.argv)
        window = QDialog()
        flow = QFormLayout()
        img_loc = QLineEdit()
        img_loc.setMinimumWidth(500)
        img_loc.setPlaceholderText("Image Location")

        save_loc = QLineEdit()
        save_loc.setPlaceholderText("Save Location")
        save_loc.setMinimumWidth(500)
        input_loc = QPushButton("Browse")
        input_loc.setFixedWidth(100)
        output_loc = QPushButton("Browse")
        output_loc.setFixedWidth(100)
        btn_strt = QPushButton("Start")
        btn_strt.setFixedWidth(100)
        btn_close = QPushButton("Close")
        btn_close.setFixedWidth(100)
        flow.addRow(QLabel("Select Input Image"))
        flow.addRow(img_loc, input_loc)
        flow.addRow(QLabel("Select Destination"))
        flow.addRow(save_loc, output_loc)
        flow.addRow(QLabel("Select Extension"))
        flow.addRow(QRadioButton("pdf"))
        flow.addRow(QRadioButton("docx"))
        btn_strt.setEnabled(False)
        flow.addRow(btn_strt, btn_close)
        input_loc.clicked.connect(lambda: self.b_clicked(img_loc, btn_strt))
        output_loc.clicked.connect(lambda: self.b1_clicked(save_loc))
        btn_strt.clicked.connect(lambda: self.start_clicked(btn_strt))
        btn_close.clicked.connect(quit)
        window.setLayout(flow)
        window.setWindowTitle("OCR")
        window.show()
        sys.exit(app.exec_())

    def b_clicked(self, e, btn):
        var = self.var
        txt = QFileDialog.getOpenFileName(None, \
                            "Open File", "", "Images (*.png *.jpg)")
        text1 = ''.join(txt)
        self.var = 1
        text1 = text1[0:(text1.find("Images (*.png *.jpg)"))]
        self.str1 = text1.replace("/", "\\\\")
        e.setText(text1)
        if var == 0 and self.str1.strip():
            btn.setEnabled(True)

    def b1_clicked(self, e):
        e_2 = QFileDialog()
        txt = e_2.getSaveFileName()
        self.var = 1
        text1 = ''.join(txt)
        e.setText(text1)

    def start_clicked(self, btn):
        if self.var == 1:
            btn.setEnabled(False)
            self.var = 0
            GenerateOutput.started(self.str1)
        self.str1 = ""
        
if __name__ == '__main__':
    myWindow = GUI()
