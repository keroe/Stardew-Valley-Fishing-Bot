from PyQt4 import QtGui, QtCore
import sys, os
import shutil
import numpy as np

class Window(QtGui.QMainWindow):


	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50, 50, 500, 300)
		self.setWindowTitle("Stardew Valley Fishing Bot v0.1")
		self.setWindowIcon(QtGui.QIcon('Images\\fish.png'))


		saveAction = QtGui.QAction("&Save", self)
		saveAction.setShortcut('Ctrl + S')
		saveAction.setStatusTip('Saves the training data')
		#saveAction.triggered.connect(self.save_data)


		sendAction = QtGui.QAction('&Send data', self)
		sendAction.setStatusTip('Automatically sends the training data and your score to the fantastic dev')
		#sendAction.triggered.connect(self.send_data)


		delDataAction = QtGui.QAction('&Delete all data', self)
		delDataAction.setStatusTip('Deletes all the data you gathered. Only do it if you really messed up when collecting data')
		delDataAction.triggered.connect(self.del_data)


		delLastDataAction = QtGui.QAction('&Delete last data', self)
		delLastDataAction.setStatusTip('Deletes the data from your last fishing session')
		delLastDataAction.triggered.connect(self.del_last_data)


		self.statusBar()

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu("&File")
		deleteMenu = mainMenu.addMenu('&Delete')
		fileMenu.addAction(saveAction)
		fileMenu.addAction(sendAction)
		deleteMenu.addAction(delDataAction)
		deleteMenu.addAction(delLastDataAction)

		self.home()

	def del_last_data(self):

		choice = QtGui.QMessageBox.question(self, "Warning!", "Are you sure you want to delete the data from your last fishing?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

		if choice == QtGui.QMessageBox.Yes:

			try:

				file_name = 'Data\\training_data.npy'
				frames_file = 'Data\\frames.npy'

				training_data = list(np.load(file_name))
				frames = list(np.load(frames_file))
				frames = [x - y for x, y in zip(frames[1:], frames)] #dont need after new trainig data

				before_score = sum(frames)

				print(len(frames))
				print(frames)
				print(len(training_data))

				if len(frames) == 1: #if there is only 1 fishing session, delete all

					data_folder = os.getcwd()
					data_folder_path = os.path.join(data_folder, 'Data')

					for file in os.listdir(data_folder_path):

						file_path = os.path.join(data_folder_path, file)
						print(file, ' removed')
						os.remove(file_path)
				
				else:

					del frames[-1]
					del training_data[-frames[-1]:]

					np.save(file_name, training_data)
					np.save(frames_file, frames)

					after_score = sum(frames)

					string = 'Last data was removed successfully!\n\n\tScore before deletion:\t' + str(before_score) + '\n\tYour score now:\t' + str(after_score)
					print(string)
					QtGui.QMessageBox.information(self, "Success", string)
				
			except Exception as e:
				print(e)
				QtGui.QMessageBox.information(self, "Oops!", "Could not delete the Data")


	def del_data(self):

		choice = QtGui.QMessageBox.question(self, "Warning!", "Are you sure you want to delete all data you gathered? Remember: you can delete just the last one!", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

		if choice == QtGui.QMessageBox.Yes:

			try:
				data_folder = os.getcwd()
				data_folder_path = os.path.join(data_folder, 'Data')

				for file in os.listdir(data_folder_path):

					file_path = os.path.join(data_folder_path, file)
					print(file, ' removed')
					os.remove(file_path)

			except Exception as e:

				print(e)
				QtGui.QMessageBox.information(self, "Oops!", "Could not delete the Data")


	def close_application(self):

		choice = QtGui.QMessageBox.question(self, "Quit?", "Are you sure you want to exit? Don't forget to save and send!", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

		if choice == QtGui.QMessageBox.Yes:
			sys.exit()


	def home(self):

		btn = QtGui.QPushButton('Save and Quit', self)
		btn.clicked.connect(self.close_application)
		btn.resize(btn.sizeHint())
		btn.move(422, 275)
		self.show()


def run():

	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

run()