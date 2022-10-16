from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap, QImage, QIntValidator, QGuiApplication, QDoubleValidator
import ray_tracer
import sys
import random

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('interface.ui', self)

        self.display_button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.remove_object_button = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.add_object_button = self.findChild(QtWidgets.QPushButton, 'pushButton_3')

        self.scroll_area = self.findChild(QtWidgets.QWidget, 'scrollAreaWidgetContents')
        self.gridLayout = QtWidgets.QGridLayout(self.scroll_area)
        self.gridLayout.setContentsMargins(40, 20, 0, 20)
        self.gridLayout.setVerticalSpacing(25)

        self.output = self.findChild(QtWidgets.QLabel, 'label')

        self.setWindowTitle("Ray Tracer")

        self.initialize()

        self.display_button.clicked.connect(self.display)
        self.remove_object_button.clicked.connect(self.remove_object)
        self.add_object_button.clicked.connect(self.add_object)

    def initialize(self):

        self.amb.setText("0.05")
        self.diff.setText("1.0")
        self.s_c.setText("1.0")
        self.s_k.setText("50")
        self.l_r.setText("255")
        self.l_g.setText("255")
        self.l_b.setText("255")
        self.l_x.setText("5")
        self.l_y.setText("5")
        self.l_z.setText("-10")

        self.n = 0
        self.x = 0
        self.y = 0

    def get_input(self, label):
        if label.text() == '':
            return 0
        
        val = float(label.text())

        return val

    def get_pos_input(self, label):

        val = self.get_input(label)

        if val > 10:
            val = 10
        
        if val < -10:
            val = -10

        return val

    def get_color_input(self, label):

        val = self.get_input(label)/255

        if val > 1:
            val = 1

        return val

    def display(self):

        data = {}
        data['objects'] = []

        for i in range(self.n):
            x = self.get_pos_input(self.findChild(QtWidgets.QLineEdit, f'X_{i+1}'))
            y = self.get_pos_input(self.findChild(QtWidgets.QLineEdit, f'Y_{i+1}'))
            z = self.get_pos_input(self.findChild(QtWidgets.QLineEdit, f'Z_{i+1}'))

            r = self.get_color_input(self.findChild(QtWidgets.QLineEdit, f'R_{i+1}'))
            g = self.get_color_input(self.findChild(QtWidgets.QLineEdit, f'G_{i+1}'))
            b = self.get_color_input(self.findChild(QtWidgets.QLineEdit, f'B_{i+1}'))

            rad = self.get_pos_input(self.findChild(QtWidgets.QLineEdit, f'radius_{i+1}'))

            data['objects'].append([[x, y, z], rad, [r, g, b]])

        data['material'] = [self.get_input(self.amb), self.get_input(self.diff), self.get_input(self.s_c), self.get_input(self.s_k)]
        data['l_pos'] = [self.get_pos_input(self.l_x), self.get_pos_input(self.l_y), self.get_pos_input(self.l_z)]
        data['l_color'] = [self.get_color_input(self.l_r), self.get_color_input(self.l_g), self.get_color_input(self.l_b)]

        self.output.setText("Loading image. Please wait.......")
        self.output.setAlignment(QtCore.Qt.AlignCenter)

        QGuiApplication.processEvents()

        img = ray_tracer.ray_tracer(data)
        qimage = QImage(img, img.shape[1], img.shape[0], img.shape[1]*3, QImage.Format_RGB888)

        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(800, 600)
        self.output.setPixmap(pixmap)

    def add_object(self):
        self.n += 1

        self.groupBox = QtWidgets.QGroupBox(self.scroll_area)
        self.groupBox.setObjectName(f"Object_{self.n}")
        self.groupBox.setTitle(f"Ball {self.n}")
        self.groupBox.setMinimumSize(QtCore.QSize(270, 160))

        self.radius = QtWidgets.QLineEdit(self.groupBox)
        self.radius.setObjectName(f"radius_{self.n}")
        self.radius.setGeometry(QtCore.QRect(130, 40, 40, 21))
        self.radius.setValidator(QDoubleValidator(0, 1, 2))
        font = self.radius.font()
        font.setPointSize(9)
        self.radius.setFont(font)
        self.radius.setText(str(round(random.random(), 2)))

        self.radius_label = QtWidgets.QLabel(self.groupBox)
        self.radius_label.setObjectName(u"radius_label")
        self.radius_label.setGeometry(QtCore.QRect(60, 40, 61, 21))
        self.radius_label.setText("Radius")

        self.R = QtWidgets.QLineEdit(self.groupBox)
        self.R.setObjectName(f"R_{self.n}")
        self.R.setGeometry(QtCore.QRect(50, 80, 40, 21))
        font = self.R.font()
        font.setPointSize(9)
        self.R.setFont(font)
        self.R.setValidator(QIntValidator(0, 255))
        self.R.setText(str(random.randint(0, 255)))

        self.R_label = QtWidgets.QLabel(self.groupBox)
        self.R_label.setObjectName(u"R_label")
        self.R_label.setGeometry(QtCore.QRect(30, 80, 16, 21))
        self.R_label.setText("R")

        self.G = QtWidgets.QLineEdit(self.groupBox)
        self.G.setObjectName(f"G_{self.n}")
        self.G.setGeometry(QtCore.QRect(130, 80, 40, 21))
        font = self.G.font()
        font.setPointSize(9)
        self.G.setFont(font)
        self.G.setValidator(QIntValidator(0, 255))
        self.G.setText(str(random.randint(0, 255)))

        self.G_label = QtWidgets.QLabel(self.groupBox)
        self.G_label.setObjectName(u"G_label")
        self.G_label.setGeometry(QtCore.QRect(110, 80, 16, 21))
        self.G_label.setText("G")

        self.B = QtWidgets.QLineEdit(self.groupBox)
        self.B.setObjectName(f"B_{self.n}")
        self.B.setGeometry(QtCore.QRect(210, 80, 40, 21))
        font = self.B.font()
        font.setPointSize(9)
        self.B.setFont(font)
        self.B.setValidator(QIntValidator(0, 255))
        self.B.setText(str(random.randint(0, 255)))

        self.B_label = QtWidgets.QLabel(self.groupBox)
        self.B_label.setObjectName(u"B_label")
        self.B_label.setGeometry(QtCore.QRect(190, 80, 16, 21))
        self.B_label.setText("B")

        self.X = QtWidgets.QLineEdit(self.groupBox)
        self.X.setObjectName(f"X_{self.n}")
        self.X.setGeometry(QtCore.QRect(50, 120, 40, 21))
        self.X.setValidator(QDoubleValidator(-10, 10, 2))
        font = self.X.font()
        font.setPointSize(9)
        self.X.setFont(font)
        self.X.setText(str(round(random.uniform(-2, 2), 2)))

        self.X_label = QtWidgets.QLabel(self.groupBox)
        self.X_label.setObjectName(u"X_label")
        self.X_label.setGeometry(QtCore.QRect(30, 120, 16, 21))
        self.X_label.setText("X")

        self.Y = QtWidgets.QLineEdit(self.groupBox)
        self.Y.setObjectName(f"Y_{self.n}")
        self.Y.setGeometry(QtCore.QRect(130, 120, 40, 21))
        self.Y.setValidator(QDoubleValidator(-10, 10, 2))
        font = self.Y.font()
        font.setPointSize(9)
        self.Y.setFont(font)
        self.Y.setText(str(round(random.uniform(0, 1.5), 2)))

        self.Y_label = QtWidgets.QLabel(self.groupBox)
        self.Y_label.setObjectName(u"Y_label")
        self.Y_label.setGeometry(QtCore.QRect(110, 120, 16, 21))
        self.Y_label.setText("Y")

        self.Z = QtWidgets.QLineEdit(self.groupBox)
        self.Z.setObjectName(f"Z_{self.n}")
        self.Z.setGeometry(QtCore.QRect(210, 120, 40, 21))
        self.Z.setValidator(QDoubleValidator(-10, 10, 2))
        font = self.Z.font()
        font.setPointSize(9)
        self.Z.setFont(font)
        self.Z.setText(str(round(random.uniform(0, 5), 2)))

        self.Z_label = QtWidgets.QLabel(self.groupBox)
        self.Z_label.setObjectName(u"Z_label")
        self.Z_label.setGeometry(QtCore.QRect(190, 120, 16, 21))
        self.Z_label.setText("Z")

        self.gridLayout.addWidget(self.groupBox, self.x, self.y, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        
        if self.y == 1:
            self.y = 0
            self.x += 1
        else:
            self.y += 1

    def remove_object(self):

        if self.n == 0:
            return

        self.last_object = self.findChild(QtWidgets.QGroupBox, f'Object_{self.n}')
        self.last_object.setParent(None)

        self.n -= 1

        if (self.y == 1):
            self.y -= 1
        else:
            self.y = 1
            self.x -= 1

app = QtWidgets.QApplication(sys.argv)
window = UI()
window.show()
app.processEvents()
app.exec_()