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
		#pdf_radio = QRadioButton("pdf")
		#docx_radio = QRadioButton("docx")
		status = QTextEdit()
		status.setReadOnly(True)

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
		#flow.addRow(QLabel("Select Extension"))
		#flow.addRow(pdf_radio)
		#flow.addRow(docx_radio)
		btn_strt.setEnabled(False)
		flow.addRow(btn_strt, btn_close)
		flow.addRow(status)
		input_loc.clicked.connect(lambda: self.b_clicked(img_loc, btn_strt))
		output_loc.clicked.connect(lambda: self.b1_clicked(save_loc, btn_strt))
		btn_strt.clicked.connect(lambda: self.start_clicked(btn_strt, status))
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
		if sys.platform.startswith('linux'):
			self.str1 = text1
		elif sys.platform.startswith('win'):
			self.str1 = text1.replace("/", "\\\\")
		e.setText(text1)
		if var0 == 0 and self.str1.strip():
			btn.setEnabled(True)
        
	
	def b1_clicked(self, e, btn):
		var1 = self.var1
		txt = QFileDialog.getExistingDirectory(None, \
                            "Save File", "")
		text1 = ''.join(txt)
		self.var1 = 1
		if sys.platform.startswith('linux'):
			self.str2 = text1
		elif sys.platform.startswith('win'):
			self.str2 = text1.replace("/", "\\\\")
		e.setText(text1)
	

	def start_clicked(self, btn, status_field):
		btn.setEnabled(False)
		self.var = 0
			
		GenerateOutput.started(self.str1, self.str2, status_field)
		self.str1 = ""
		
        
if __name__ == '__main__':
	myWindow = GUI()
