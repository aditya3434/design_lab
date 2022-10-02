from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap, QImage, QIntValidator, QGuiApplication, QDoubleValidator
import sys
import ray_tracer

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('interface.ui', self)

        self.display_button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.clear_button = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.defaults = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.output = self.findChild(QtWidgets.QLabel, 'label')

        self.b1_r = self.findChild(QtWidgets.QLineEdit, 'b1_r')
        self.b1_r.setValidator(QIntValidator(0, 255))
        self.b1_g = self.findChild(QtWidgets.QLineEdit, 'b1_g')
        self.b1_g.setValidator(QIntValidator(0, 255))
        self.b1_b = self.findChild(QtWidgets.QLineEdit, 'b1_b')
        self.b1_b.setValidator(QIntValidator(0, 255))
        self.b1_x = self.findChild(QtWidgets.QLineEdit, 'b1_x')
        self.b1_x.setValidator(QDoubleValidator(-10, 10, 2))
        self.b1_y = self.findChild(QtWidgets.QLineEdit, 'b1_y')
        self.b1_y.setValidator(QDoubleValidator(-10, 10, 2))
        self.b1_z = self.findChild(QtWidgets.QLineEdit, 'b1_z')
        self.b1_z.setValidator(QDoubleValidator(-10, 10, 2))

        self.b2_r = self.findChild(QtWidgets.QLineEdit, 'b2_r')
        self.b2_r.setValidator(QIntValidator(0, 255))
        self.b2_g = self.findChild(QtWidgets.QLineEdit, 'b2_g')
        self.b2_g.setValidator(QIntValidator(0, 255))
        self.b2_b = self.findChild(QtWidgets.QLineEdit, 'b2_b')
        self.b2_b.setValidator(QIntValidator(0, 255))
        self.b2_x = self.findChild(QtWidgets.QLineEdit, 'b2_x')
        self.b2_x.setValidator(QDoubleValidator(-10, 10, 2))
        self.b2_y = self.findChild(QtWidgets.QLineEdit, 'b2_y')
        self.b2_y.setValidator(QDoubleValidator(-10, 10, 2))
        self.b2_z = self.findChild(QtWidgets.QLineEdit, 'b2_z')
        self.b2_z.setValidator(QDoubleValidator(-10, 10, 2))

        self.b3_r = self.findChild(QtWidgets.QLineEdit, 'b3_r')
        self.b3_r.setValidator(QIntValidator(0, 255))
        self.b3_g = self.findChild(QtWidgets.QLineEdit, 'b3_g')
        self.b3_g.setValidator(QIntValidator(0, 255))
        self.b3_b = self.findChild(QtWidgets.QLineEdit, 'b3_b')
        self.b3_b.setValidator(QIntValidator(0, 255))
        self.b3_x = self.findChild(QtWidgets.QLineEdit, 'b3_x')
        self.b3_x.setValidator(QDoubleValidator(-10, 10, 2))
        self.b3_y = self.findChild(QtWidgets.QLineEdit, 'b3_y')
        self.b3_y.setValidator(QDoubleValidator(-10, 10, 2))
        self.b3_z = self.findChild(QtWidgets.QLineEdit, 'b3_z')
        self.b3_z.setValidator(QDoubleValidator(-10, 10, 2))

        self.l_r = self.findChild(QtWidgets.QLineEdit, 'l_r')
        self.l_r.setValidator(QIntValidator(0, 255))
        self.l_g = self.findChild(QtWidgets.QLineEdit, 'l_g')
        self.l_g.setValidator(QIntValidator(0, 255))
        self.l_b = self.findChild(QtWidgets.QLineEdit, 'l_b')
        self.l_b.setValidator(QIntValidator(0, 255))
        self.l_x = self.findChild(QtWidgets.QLineEdit, 'l_x')
        self.l_x.setValidator(QDoubleValidator(-10, 10, 2))
        self.l_y = self.findChild(QtWidgets.QLineEdit, 'l_y')
        self.l_y.setValidator(QDoubleValidator(-10, 10, 2))
        self.l_z = self.findChild(QtWidgets.QLineEdit, 'l_z')
        self.l_z.setValidator(QDoubleValidator(-10, 10, 2))

        self.amb = self.findChild(QtWidgets.QLineEdit, 'amb')
        self.amb.setValidator(QDoubleValidator(-10, 10, 2))
        self.diff = self.findChild(QtWidgets.QLineEdit, 'diff')
        self.diff.setValidator(QDoubleValidator(-10, 10, 2))
        self.s_c = self.findChild(QtWidgets.QLineEdit, 's_c')
        self.s_c.setValidator(QDoubleValidator(-10, 10, 2))
        self.s_k = self.findChild(QtWidgets.QLineEdit, 's_k')
        self.s_k.setValidator(QDoubleValidator(0, 99, 2))

        self.initialize()

        self.display_button.clicked.connect(self.display)
        self.clear_button.clicked.connect(self.clear)
        self.defaults.clicked.connect(self.set_defaults)

    def initialize(self):

        self.b1_r.setText("0")
        self.b1_g.setText("0")
        self.b1_b.setText("255")
        self.b1_x.setText("0.75")
        self.b1_y.setText("0.1")
        self.b1_z.setText("1.0")

        self.b2_r.setText("255")
        self.b2_g.setText("0")
        self.b2_b.setText("0")
        self.b2_x.setText("-0.75")
        self.b2_y.setText("0.2")
        self.b2_z.setText("2.25")

        self.b3_r.setText("0")
        self.b3_g.setText("180")
        self.b3_b.setText("0")
        self.b3_x.setText("-2.75")
        self.b3_y.setText("0.1")
        self.b3_z.setText("3.5")

        self.l_r.setText("255")
        self.l_g.setText("255")
        self.l_b.setText("255")
        self.l_x.setText("5")
        self.l_y.setText("5")
        self.l_z.setText("-10")

        self.amb.setText("0.05")
        self.diff.setText("1.0")
        self.s_c.setText("1.0")
        self.s_k.setText("50")

    def get_input(self, label):
        if label.text() == '':
            return 0
        
        val = float(label.text())

        return val

    def get_pos_input(self, label):
        if label.text() == '':
            return 0
        
        val = float(label.text())

        if val > 10:
            val = 10
        
        if val < -10:
            val = -10

        return val

    def get_color_input(self, label):
        if label.text() == '':
            return 0
        
        val = float(label.text())/255

        if val > 1:
            val = 1

        return val

    def display(self):
        
        self.output.setText("Loading image. Please wait.......")
        self.output.setAlignment(QtCore.Qt.AlignCenter)

        self.b1_pos = [self.get_pos_input(self.b1_x), self.get_pos_input(self.b1_y), self.get_pos_input(self.b1_z)]
        self.b2_pos = [self.get_pos_input(self.b2_x), self.get_pos_input(self.b2_y), self.get_pos_input(self.b2_z)]
        self.b3_pos = [self.get_pos_input(self.b3_x), self.get_pos_input(self.b3_y), self.get_pos_input(self.b3_z)]
        self.l_pos = [self.get_pos_input(self.l_x), self.get_pos_input(self.l_y), self.get_pos_input(self.l_z)]

        self.b1_color = [self.get_color_input(self.b1_r), self.get_color_input(self.b1_g), self.get_color_input(self.b1_b)]
        self.b2_color = [self.get_color_input(self.b2_r), self.get_color_input(self.b2_g), self.get_color_input(self.b2_b)]
        self.b3_color = [self.get_color_input(self.b3_r), self.get_color_input(self.b3_g), self.get_color_input(self.b3_b)]
        self.l_color = [self.get_color_input(self.l_r), self.get_color_input(self.l_g), self.get_color_input(self.l_b)]

        self.material = [self.get_input(self.amb), self.get_input(self.diff), self.get_input(self.s_c), self.get_input(self.s_k)]

        args = dict(b1_pos=self.b1_pos, b2_pos=self.b2_pos, b3_pos=self.b3_pos, l_pos=self.l_pos,
                    b1_color=self.b1_color, b2_color=self.b2_color, b3_color=self.b3_color, l_color=self.l_color, material=self.material)

        QGuiApplication.processEvents()

        img = ray_tracer.ray_tracer(args)
        qimage = QImage(img, img.shape[1], img.shape[0], img.shape[1]*3, QImage.Format_RGB888)

        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(800, 600)
        self.output.setPixmap(pixmap)

    def clear(self):
        self.output.setPixmap(QPixmap())

    def set_defaults(self):
        self.initialize()
        self.display()

app = QtWidgets.QApplication(sys.argv)
window = UI()
window.show()
app.processEvents()
app.exec_()