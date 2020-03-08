import sys
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem


class MyTable(QTableWidget):
	def __init__(self, r, c):
		super().__init__(r, c)
		self.init_ui()

	def init_ui(self):
		self.cellChanged.connect(self.c_current)
		self.show()

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

		self.form_widget = MyTable(20, 7)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'Connection type', 'Axial load', 'Sher load', 'Bolt diameter', 'Bolt grade', 'Plate Thickness']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()

		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	FP = FinPlate()
	sys.exit(app.exec_())
