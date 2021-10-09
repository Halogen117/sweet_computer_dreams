from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class get_time(QDialog):
    def __init__(self):
        loadUi('get_time.ui',self)