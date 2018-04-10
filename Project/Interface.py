import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import GenerateOutput

class GUI:
	def __init__(self):
		self.var = 0
		self.var1 = 0
		self.str1 = ""
		self.str2 = ""
		self.initUI()
        

    
	def initUI(self):
		app = QApplication(sys.argv)
		window = QDialog()
		flow = QFormLayout()
		img_loc = QLineEdit()
		img_loc.setMinimumWidth(500)
		img_loc.setPlaceholderText("Image Location")
		pdf_radio = QRadioButton("pdf")
		docx_radio = QRadioButton("docx")

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
		flow.addRow(pdf_radio)
		flow.addRow(docx_radio)
		btn_strt.setEnabled(False)
		flow.addRow(btn_strt, btn_close)
		input_loc.clicked.connect(lambda: self.b_clicked(img_loc, btn_strt))
		output_loc.clicked.connect(lambda: self.b1_clicked(save_loc, btn_strt))
		btn_strt.clicked.connect(lambda: self.start_clicked(btn_strt, pdf_radio, docx_radio))
		btn_close.clicked.connect(quit)
		window.setLayout(flow)
		window.setWindowTitle("OCR")
		window.show()
		sys.exit(app.exec_())

	def b_clicked(self, e, btn):
		var0 = self.var
		txt = QFileDialog.getOpenFileName(None, \
                            "Open File", "", "Images (*.png *.jpg)")
		text1 = ''.join(txt)
		self.var = 1
		text1 = text1[0:(text1.find("Images (*.png *.jpg)"))]
		self.str1 = text1.replace("/", "\\\\")
		e.setText(text1)
        

	def b1_clicked(self, e, btn):
		var1 = self.var1
		txt = QFileDialog.getSaveFileName(None, \
                            "Save File", "", "Documents (*.docx *.pdf)")
		text1 = ''.join(txt)
		self.var1 = 1
		text1 = text1[0:(text1.find("Documents (*.docx *.pdf)"))]
		self.str2 = text1.replace("/", "\\\\")
		e.setText(text1)
		if var1 == 0 and self.str2.strip():
			btn.setEnabled(True)

	def start_clicked(self, btn, rad_1, rad_2):
		check = -1
		if self.var == 1 and self.var1 == 1:
			if rad_1.isChecked():
				check = 0
			elif rad_2.isChecked():
				check = 1
			btn.setEnabled(False)
			self.var = 0
			self.var1 = 0
			GenerateOutput.started(self.str1, self.str2, check)
		self.str1 = ""
		self.str2 = ""
        
if __name__ == '__main__':
	myWindow = GUI()
