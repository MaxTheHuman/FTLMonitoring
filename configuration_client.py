import sys

import requests as req
from flask import jsonify

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QListView,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSplitter, QStatusBar, QTextBrowser, QWidget)


class Ui_MainWindow(object):
    def __init__(self):
        self.formulas = []
        self.avoiding_function_points = dict()
        self.avoiding_function_points[0] = 1
        self.threshold = 0.8

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(797, 652)
        MainWindow.setStyleSheet(u"background: rgb(225, 225, 225)")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_subtitle = QLabel(self.centralwidget)
        self.label_subtitle.setObjectName(u"label_subtitle")
        self.label_subtitle.setGeometry(QRect(180, 10, 403, 24))
        font = QFont()
        font.setPointSize(20)
        font.setBold(False)
        self.label_subtitle.setFont(font)
        self.configurePush = QPushButton(self.centralwidget)
        self.configurePush.setObjectName(u"configurePush")
        self.configurePush.setGeometry(QRect(250, 540, 271, 71))
        font1 = QFont()
        font1.setPointSize(16)
        self.configurePush.setFont(font1)
        self.label_avoiding_output = QLabel(self.centralwidget)
        self.label_avoiding_output.setObjectName(u"label_avoiding_output")
        self.label_avoiding_output.setGeometry(QRect(80, 150, 631, 111))
        self.label_avoiding_output.setFont(font1)
        self.label_avoiding_output.setMidLineWidth(14)
        self.label_avoiding_output.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_avoiding_output.setMargin(5)
        self.label_formulas = QLabel(self.centralwidget)
        self.label_formulas.setObjectName(u"label_formulas")
        self.label_formulas.setGeometry(QRect(80, 320, 621, 191))
        self.label_formulas.setFont(font1)
        self.label_formulas.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_formulas.setMargin(5)
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(80, 120, 619, 24))
        self.splitter.setOrientation(Qt.Horizontal)
        self.label_avoiding = QLabel(self.splitter)
        self.label_avoiding.setObjectName(u"label_avoiding")
        self.label_avoiding.setFont(font1)
        self.splitter.addWidget(self.label_avoiding)
        self.label_X = QLabel(self.splitter)
        self.label_X.setObjectName(u"label_X")
        self.label_X.setFont(font1)
        self.splitter.addWidget(self.label_X)
        self.lineEdit_X = QLineEdit(self.splitter)
        self.lineEdit_X.setObjectName(u"lineEdit_X")
        self.splitter.addWidget(self.lineEdit_X)
        self.label_Y = QLabel(self.splitter)
        self.label_Y.setObjectName(u"label_Y")
        self.label_Y.setFont(font1)
        self.splitter.addWidget(self.label_Y)
        self.lineEdit_Y = QLineEdit(self.splitter)
        self.lineEdit_Y.setObjectName(u"lineEdit_Y")
        self.splitter.addWidget(self.lineEdit_Y)
        self.addAvoidingPointPush = QPushButton(self.splitter)
        self.addAvoidingPointPush.setObjectName(u"addAvoidingPointPush")
        self.splitter.addWidget(self.addAvoidingPointPush)
        self.splitter_2 = QSplitter(self.centralwidget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setGeometry(QRect(81, 71, 454, 22))
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.lable_threshold = QLabel(self.splitter_2)
        self.lable_threshold.setObjectName(u"lable_threshold")
        self.lable_threshold.setFont(font1)
        self.splitter_2.addWidget(self.lable_threshold)
        self.lineEdit_threshold = QLineEdit(self.splitter_2)
        self.lineEdit_threshold.setObjectName(u"lineEdit_threshold")
        self.lineEdit_threshold.setFont(font1)
        self.lineEdit_threshold.setDragEnabled(False)
        self.splitter_2.addWidget(self.lineEdit_threshold)
        self.splitter_3 = QSplitter(self.centralwidget)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setGeometry(QRect(80, 280, 621, 21))
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.label_formula = QLabel(self.splitter_3)
        self.label_formula.setObjectName(u"label_formula")
        self.label_formula.setFont(font1)
        self.splitter_3.addWidget(self.label_formula)
        self.lineEdit_formula = QLineEdit(self.splitter_3)
        self.lineEdit_formula.setObjectName(u"lineEdit_formula")
        self.splitter_3.addWidget(self.lineEdit_formula)
        self.addFormulaPush = QPushButton(self.splitter_3)
        self.addFormulaPush.setObjectName(u"addFormulaPush")
        self.splitter_3.addWidget(self.addFormulaPush)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 797, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.addAvoidingPointPush.clicked.connect(self.addAvoidingPoint)
        self.addFormulaPush.clicked.connect(self.addFormula)
        self.configurePush.clicked.connect(self.configure)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Конфигурация сервиса мониторинга", None))
        self.label_subtitle.setText(QCoreApplication.translate("MainWindow", u"Введите параметры сервера мониторинга", None))
        self.label_avoiding.setText(QCoreApplication.translate("MainWindow", u"Точки функции штрафа за пропуски:", None))
        self.label_X.setText(QCoreApplication.translate("MainWindow", u"X:", None))
        self.label_Y.setText(QCoreApplication.translate("MainWindow", u"Y:", None))
        self.addAvoidingPointPush.setText(QCoreApplication.translate("MainWindow", u"Добавить", None))
        self.lable_threshold.setText(QCoreApplication.translate("MainWindow", u"Порог допустимой выполнимости правил:", None))
        # self.lineEdit_threshold.setInputMask(QCoreApplication.translate("MainWindow", u"0-1", None))
        # self.lineEdit_threshold.setText(QCoreApplication.translate("MainWindow", u"0-1", None))
        # self.lineEdit_threshold.setPlaceholderText("0.8")
        self.lineEdit_threshold.setText("0.8")
        self.label_formula.setText(QCoreApplication.translate("MainWindow", u"Правило для проверки:", None))
        self.addFormulaPush.setText(QCoreApplication.translate("MainWindow", u"Добавить", None))
        self.configurePush.setText(QCoreApplication.translate("MainWindow", u"Отправить конфигурацию сервера", None))
        self.label_avoiding_output.setText(QCoreApplication.translate("MainWindow", u"(0;1)", None))
        self.label_formulas.setText("")
    # retranslateUi

    def addAvoidingPoint(self):
        self.avoiding_function_points[float(self.lineEdit_X.text())] = float(self.lineEdit_Y.text())
        current_output_text = self.label_avoiding_output.text()
        self.label_avoiding_output.setText(current_output_text + ', ' + '({};{})'.format(self.lineEdit_X.text(), self.lineEdit_Y.text()))
        self.lineEdit_X.setText('')
        self.lineEdit_Y.setText('')
    
    def addFormula(self):
        new_formula = self.lineEdit_formula.text()
        self.formulas.append(new_formula)
        current_output_text = self.label_formulas.text()
        self.label_formulas.setText(current_output_text + (', ' if len(current_output_text) else '') + new_formula)
        self.lineEdit_formula.setText('')
    
    def configure(self):
        resp = req.post("http://127.0.0.1:5000/configure_and_start", json={
            "acceptance_threshold": float(self.lineEdit_threshold.text()),
            "avoiding_function_points": [
                {
                    "x": x,
                    "value": y
                } for x, y in self.avoiding_function_points.items()
            ],
            "formulas": self.formulas
        })
        result = resp.text
        print(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec())
