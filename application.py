import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QMainWindow, QTableWidgetItem, QDialog, QTabWidget, QDialogButtonBox, QTableWidget, QAction
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon


class App(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Application")
		self.tabs = Tab(self)
		self.btns = Buttons(self)
		self.msg = MessageBox(self)
		self.grid = QHBoxLayout(self)
		self.vbox = QVBoxLayout(self)
		self.vbox2 = QVBoxLayout(self)
		self.vbox.addWidget(self.tabs)
		self.vbox2.addWidget(self.btns)
		self.vbox2.addWidget(self.msg)
		self.vbox2.addStretch()
		self.grid.addItem(self.vbox)
		self.grid.addItem(self.vbox2)
		self.setLayout(self.grid)

		self.show()


class MessageBox(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)

		msg.setText("This is message box")
		msg.setInformativeText("This is additional information")
		msg.setDetailedText("The details are as follow")

		self.box = QVBoxLayout(self)
		self.box.addWidget(msg)
		self.setLayout(self.box)


class Buttons(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.load = QPushButton('Load')
		self.validate = QPushButton('Validate')
		self.submit = QPushButton('Submit')

		self.box = QVBoxLayout(self)
		self.box.addWidget(self.load)
		self.box.addWidget(self.validate)
		self.box.addWidget(self.submit)

		self.setLayout(self.box)


class Tab(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.vbox = QVBoxLayout(self)

		self.tabs = QTabWidget()

		self.tabs.addTab(FinPlate(), "Fin Plate")
		self.tabs.addTab(TensionMember(), "Tension Member")
		self.tabs.addTab(BCEndPlate(), "BC End Plate")
		self.tabs.addTab(CheatAngle(), "Cheat Angle")

		self.vbox.addWidget(self.tabs)
		self.setLayout(self.vbox)


class MyTable(QTableWidget):
	def __init__(self, r, c):
		super().__init__(r, c)
		self.cellChanged.connect(self.c_current)

	def c_current(self):
		self.resizeColumnsToContents()
		self.resizeRowsToContents()
		row = self.currentRow()
		col = self.currentColumn()
		value = self.item(row, col)
		value = value.text()
		print("The current cell is", row, ",", col)
		print("In this cell we have:", value)


class FinPlate(QMainWindow):
	def __init__(self):
		super().__init__()

		self.form_widget = MyTable(10, 7)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'Connection type', 'Axial load', 'Sher load', 'Bolt diameter', 'Bolt grade', 'Plate Thickness']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()


class TensionMember(QMainWindow):
	def __init__(self):
		super().__init__()

		self.form_widget = MyTable(10, 5)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'Member length', 'Tensile load', 'Support condition at End 1', 'Support condition at End 2']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()


class BCEndPlate(QMainWindow):
	def __init__(self):
		super().__init__()

		self.form_widget = MyTable(10, 8)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'End plate type', 'Sher load', 'Axial load', 'Maximum Load', 'Bolt diameter', 'Bolt grade', 'Plate thickness']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()


class CheatAngle(QMainWindow):
	def __init__(self):
		super().__init__()

		self.form_widget = MyTable(10, 7)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'Angle leg 1', 'Angle leg 2', 'Angle thickness', 'Sher load', 'Bolt diameter',
		               'Bolt grade']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	App = App()
	sys.exit(app.exec_())
