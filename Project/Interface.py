import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import GenerateOutput


# TODO: Make widget size dynamic and auto adjusting
# TODO: Merge the codes
class GUI:
    def __init__(self):
        self.initUI()

    global var
    str1 = ""

    def initUI(self):
        app = QApplication(sys.argv)
        window = QDialog()
        flow = QFormLayout()
        # screen_center = lambda widget: QApplication.desktop().screen().rect().center() - widget.rect().center()
        # flow.setAlignment(Qt.AlignHCenter)
        e1 = QLineEdit()
        e1.setMinimumWidth(500)
        e1.setPlaceholderText("Image Location")

        # e1.move(QApplication.desktop().screen().rect().center() - e1.rect().center())

        e2 = QLineEdit()
        e2.setPlaceholderText("Save Location")
        e2.setMinimumWidth(500)
        b = QPushButton("Browse")
        b.setFixedWidth(100)
        b1 = QPushButton("Browse")
        b1.setFixedWidth(100)
        btn_strt = QPushButton("Start")
        btn_strt.setFixedWidth(100)
        btn_cncl = QPushButton("Close")
        btn_cncl.setFixedWidth(100)
        flow.addRow(QLabel("Select Input Image"))
        flow.addRow(e1, b)
        flow.addRow(QLabel("Select Destination"))
        flow.addRow(e2, b1)
        flow.addRow(QLabel("Select Extension"))
        flow.addRow(QRadioButton("pdf"))
        flow.addRow(QRadioButton("docx"))
        flow.addRow(btn_strt, btn_cncl)
        b.clicked.connect(lambda: self.b_clicked(e1))
        b1.clicked.connect(lambda: self.b1_clicked(e2))
        btn_strt.clicked.connect(self.start_clicked)
        btn_cncl.clicked.connect(quit)
        window.setLayout(flow)
        window.setWindowTitle("OCR")
        window.show()
        sys.exit(app.exec_())

    def b_clicked(self, e):
        txt = QFileDialog.getOpenFileName(None, "Open File", "C:\\", "Images (*.png, *.jpg)")
        text1 = ''.join(txt)
        text1 = text1[0:(text1.find("Images"))]
        self.str1 = text1.replace("/", "\\\\")
        e.setText(text1)
        print(self.str1)
        print(text1)

    def b1_clicked(self, e):
        e_2 = QFileDialog()
        txt = e_2.getSaveFileName()
        text1 = ''.join(txt)
        e.setText(text1)

    def start_clicked(self):
        GenerateOutput.start(self.str1)
        # foo.Test().bar()

        # var = 1

if __name__ == '__main__':
    myWindow = GUI()
