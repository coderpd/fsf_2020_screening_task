import sys
import csv
import xlrd
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QWidget, QTableWidgetItem, QSpinBox, QMessageBox, QFileDialog, QComboBox, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QTabWidget, QTableWidget


class App(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Application")
		self.tabs = Tab(self)
		self.btns = Buttons(self)
		self.msg = MessageBox(self)
		self.grid = QGridLayout(self)
		self.grid.addWidget(self.tabs, 0, 0, 10, 7)
		self.grid.addWidget(self.btns, 0, 7, 1, 3)
		self.grid.addWidget(self.msg, 2, 7, 7, 3)
		self.grid.setContentsMargins(7, 7, 7, 7)
		self.setLayout(self.grid)

		self.show()

		self.errors = {}
		self.count_errors = {}
		self.data = {}

	def load(self, table):
		for i in range(table.rowCount()):
			table.removeRow(0)
		self.append(table)

	def append(self, table):
		for d in self.data:
			table.insertRow(table.rowCount())
			for i in range(len(d)):
				if type(d[i]) is float: d[i] = int(d[i])
				table.setItem(table.rowCount()-1, i, QTableWidgetItem(str(d[i])))

	def readFile(self):
		file = QFileDialog.getOpenFileName(self, 'Open file', '.', "Excel/CSV File (*.csv *.xls *.xlsx)")
		if file[0] == '' or None: return False
		print('extension',file[0][-3:])
		if file[0][-3:] == 'csv':
			with open(file[0], 'r', newline = '') as csvfile:
				reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
				self.data = list(reader)
		elif file[0][-3:] == 'xls' or file[0][-4:] =='xlsx':
			self.data = []
			wb = xlrd.open_workbook(file[0])
			sheet = wb.sheet_by_index(0)
			for i in range(sheet.nrows):
				self.data.append(sheet.row_values(i))
		print(self.data)
		return True

	def validate(self, table):
		count = 0
		e = {}
		d = {}
		for i in range(table.rowCount()):
			e[i] = {}
			d[i] = {}
			for j in range(table.rowCount()):
				if table.item(i, 0) is None or table.item(j, 0) is None or i == j:
					continue
				try:
					if table.item(i, 0).text() == table.item(j, 0).text() and table.item(i, 0).text() != '':
						count = count + 1
						e[i][0] = 'id of ' + str(i + 1) + ' data similar to ' + str(j + 1) + ' data'
				except ValueError:
					continue
			for j in range(table.columnCount()):
				value = table.item(i, j)
				if value is None or value.text() == '':
					e[i][j] = 'No value in the cell ' + str(i + 1) + ', ' + str(j + 1)
					count = count + 1
					d[i][table.horizontalHeaderItem(j).text()] = None
				else:
					try:
						d[i][table.horizontalHeaderItem(j).text()] = int(value.text())
					except ValueError:
						e[i][j] = 'Value is not Int in the cell ' + str(i + 1) + ', ' + str(j + 1)
						d[i][table.horizontalHeaderItem(j).text()] = value.text()
						print(e[i][j])
						count = count + 1
		self.errors[id(table)] = e
		self.count_errors[id(table)] = count
		self.data[id(table)] = d

	def setMessageBox(self):
		self.detailedError = ""
		for id in self.errors:
			if self.count_errors[id]:
				self.detailedError = self.detailedError + "Errors in tab " + self.tabs.id[id] + ":\n"
				for row in self.errors[id]:
					for col in self.errors[id][row]:
						self.detailedError = self.detailedError + self.errors[id][row][col] + '\n'
		self.informativeError = ""
		for id in self.count_errors:
			if self.count_errors[id]:
				self.informativeError = self.informativeError + str(self.count_errors[id]) + " error found in tab " + self.tabs.id[id] + '\n'
		if sum(self.count_errors.values()):
			self.textError = "Total " + str(sum(self.count_errors.values())) + " errors found"
			self.msg.msg.setIcon(QMessageBox.Warning)
		else:
			self.textError = "No error"
			self.informativeError = "Everything all right"
			self.msg.msg.setIcon(QMessageBox.Information)
		self.msg.msg.setText(self.textError)
		self.msg.msg.setInformativeText(self.informativeError)
		self.msg.msg.setDetailedText(self.detailedError)

	def confirmWarning(self):
		wbox = QMessageBox()
		wbox.addButton("Force Submit", QMessageBox.AcceptRole)
		wbox.addButton("Discard Submit", QMessageBox.RejectRole)
		wbox.setText(self.textError + ". Do you want to force save?")
		wbox.setInformativeText(self.informativeError)
		wbox.setDetailedText(self.detailedError)
		return wbox.exec_()

	def submit(self):
		if (sum(self.count_errors.values())) > 0:
			if self.confirmWarning(): return
		directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		for id in self.data:
			for d in self.data[id].values():
				if d['ID'] is None: continue
				print(directory + '/' + self.tabs.id[id] + '_' + str(d['ID']) + '.txt')
				with open(directory + '/' + self.tabs.id[id] + '_' + str(d['ID']) + '.txt', 'w') as file:
					file.write(str(d))
					print(d)


class MessageBox(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.label = QLabel('Error Status:')
		self.msg = QMessageBox()
		self.msg.setIcon(QMessageBox.Information)

		self.msg.setText("No error")
		self.msg.setInformativeText("Everything all right")
		#		self.msg.setStandardButtons(QMessageBox.NoButton)
		self.msg.addButton("Close App", QMessageBox.ResetRole)
		self.msg.buttonClicked.connect(self.close)

		self.box = QVBoxLayout(self)
		self.box.addWidget(self.label)
		self.box.addWidget(self.msg)
		self.box.addStretch()
		self.setLayout(self.box)

	@pyqtSlot()
	def close(self):
		exit(0)


class Buttons(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.dropdown = QComboBox()
		self.load = QPushButton('Load')
		self.load.clicked.connect(self.load_action)
		self.validate = QPushButton('Validate')
		self.validate.clicked.connect(self.validate_action)
		self.submit = QPushButton('Submit')
		self.submit.clicked.connect(self.submit_action)
		self.validateall = QPushButton('Validate All')
		self.validateall.clicked.connect(self.validateall_action)
		self.submitall = QPushButton('Submit All')
		self.submitall.clicked.connect(self.submitall_action)
		self.dropdown.addItems(["FinPlate", "TensionMember", "BCEndPlate", "CheatAngle"])

		self.vbox = QVBoxLayout(self)
		self.hbox = QHBoxLayout(self)
		self.hbox.addWidget(self.load)
		self.hbox.addWidget(self.validate)
		self.hbox.addWidget(self.submit)

		self.hbox2 = QHBoxLayout(self)
		self.hbox2.addWidget(self.validateall)
		self.hbox2.addWidget(self.submitall)

		self.vbox.addSpacing(40)
		self.vbox.addWidget(self.dropdown)
		self.vbox.addLayout(self.hbox)
		self.vbox.addSpacing(50)
		self.vbox.addLayout(self.hbox2)
		self.setLayout(self.vbox)

	@pyqtSlot()
	def load_action(self):
		if App.readFile():
			table = self.getDropDown()
			App.load(table)

	@pyqtSlot()
	def append_action(self):
		if App.readFile():
			table = self.getDropDown()
			App.append(table)


	@pyqtSlot()
	def validate_action(self):
		App.errors = {}
		App.count_errors = {}
		App.data = {}
		table = self.getDropDown()
		App.validate(table)
		App.setMessageBox()
		print(App.count_errors)
		print(App.errors)
		print(App.data)

	@pyqtSlot()
	def validateall_action(self):
		App.errors = {}
		App.count_errors = {}
		App.data = {}
		App.validate(App.tabs.finplate)
		App.validate(App.tabs.tensionmember)
		App.validate(App.tabs.bcendplate)
		App.validate(App.tabs.cheatangle)
		App.setMessageBox()
		print(App.count_errors)
		print(App.errors)
		print(App.data)

	@pyqtSlot()
	def submit_action(self):
		self.validate_action()
		App.submit()

	@pyqtSlot()
	def submitall_action(self):
		self.validateall_action()
		App.submit()

	def getDropDown(self):
		index = self.dropdown.currentIndex()
		if index == 0:
			return App.tabs.finplate
		if index == 1:
			return App.tabs.tensionmember
		if index == 2:
			return App.tabs.bcendplate
		return App.tabs.cheatangle


class Tab(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.vbox = QVBoxLayout(self)

		self.tabs = QTabWidget()
		self.finplate = Table(
			['ID', 'Connection type', 'Axial load', 'Sher load', 'Bolt diameter', 'Bolt grade', 'Plate Thickness'])
		self.tensionmember = Table(
			['ID', 'Member length', 'Tensile load', 'Support condition at End 1', 'Support condition at End 2'])
		self.bcendplate = Table(
			['ID', 'End plate type', 'Sher load', 'Axial load', 'Maximum Load', 'Bolt diameter', 'Bolt grade',
			 'Plate thickness'])
		self.cheatangle = Table(
			['ID', 'Angle leg 1', 'Angle leg 2', 'Angle thickness', 'Sher load', 'Bolt diameter', 'Bolt grade'])
		self.id = {id(self.finplate): 'Fin Plate', id(self.tensionmember): 'Tension Member', id(self.cheatangle): 'Cheat Angle', id(self.bcendplate): 'BC End Plate'}
		self.tabs.addTab(self.finplate, "Fin Plate")
		self.tabs.addTab(self.tensionmember, "Tension Member")
		self.tabs.addTab(self.bcendplate, "BC End Plate")
		self.tabs.addTab(self.cheatangle, "Cheat Angle")

		self.spinbox = QSpinBox()
		self.spinbox.setValue(1)
		self.insert_btn = QPushButton('Insert Rows')
		self.insert_btn.clicked.connect(self.insert_btn_action)
		self.delete_btn = QPushButton('Delete Rows')
		self.delete_btn.clicked.connect(self.delete_btn_action)

		self.hbox = QHBoxLayout(self)
		self.hbox.addWidget(self.spinbox)
		self.hbox.addWidget(self.insert_btn)
		self.hbox.addWidget(self.delete_btn)

		self.vbox.addWidget(self.tabs)
		self.vbox.addLayout(self.hbox)
		self.setLayout(self.vbox)

	@pyqtSlot()
	def insert_btn_action(self):
		if self.tabs.currentIndex() == 0:
			table = self.finplate
		elif self.tabs.currentIndex() == 1:
			table = self.tensionmember
		elif self.tabs.currentIndex() == 2:
			table = self.bcendplate
		else:
			table = self.cheatangle
		for i in range(self.spinbox.value()):
			table.insertRow(table.rowCount())
		table.resizeColumnsToContents()
		table.resizeRowsToContents()

	@pyqtSlot()
	def delete_btn_action(self):
		if self.tabs.currentIndex() == 0:
			table = self.finplate
		elif self.tabs.currentIndex() == 1:
			table = self.tensionmember
		elif self.tabs.currentIndex() == 2:
			table = self.bcendplate
		else:
			table = self.cheatangle
		for i in range(self.spinbox.value()):
			table.removeRow(table.rowCount() - 1)


class Table(QTableWidget):
	def __init__(self, col_headers):
		super().__init__(0, len(col_headers))
		self.cellChanged.connect(self.c_current)
		self.setMinimumSize(1300, 600)
		self.setHorizontalHeaderLabels(col_headers)
		self.resizeColumnsToContents()
		self.resizeRowsToContents()

	def c_current(self):
		self.resizeColumnsToContents()
		self.resizeRowsToContents()
		row = self.currentRow()
		col = self.currentColumn()
		value = self.item(row, col)
		if value is None: return
		value = value.text()
		print("The current cell is", row, ",", col)
		print("In this cell we have:", value)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	App = App()
	sys.exit(app.exec_())
