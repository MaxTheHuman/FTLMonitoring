from flask import Flask, request, jsonify
from PyQt6 import QtCore as core

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QTimer)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QListWidget,
    QMainWindow, QMenuBar, QStatusBar, QWidget)

import sys
import threading
import requests as req

import traceback
import logging

from sortedcontainers import SortedDict

from formula_parser import Parser
from formula import Eta


app = Flask(__name__)

server_configured = False
formulas = []
variables = dict()
acceptance_threshold = 0.0
evaluations = []

@app.route('/')
def index():
    return jsonify({'results': [{"formulas": formulas_results} for formulas_results in evaluations]})

@app.route('/debug', methods=['GET'])
def debug():
    global formulas
    global variables
    global acceptance_threshold

    print('formulas: ', end='')
    for formula in formulas:
        print(formula, end=', ')
    print('\nvariables: ', end='')
    for variable in variables:
        print(variable, end=', ')
    print('\nacceptance_threshold:', acceptance_threshold)
    
    formulas_strs = [str(formula) for formula in formulas]
    resp = req.get("http://127.0.0.1:5000/")
    return jsonify({'formulas':formulas_strs, 'variables': variables, 'acceptance_threshold': acceptance_threshold, 'resp': resp.text})

@app.route('/configure_and_start', methods=['POST'])
def configure():
    global formulas
    global variables
    global acceptance_threshold
    global server_configured
    avoiding_function_points = SortedDict()

    request_json = request.get_json()

    if 'acceptance_threshold' not in request_json:
        response = jsonify({'message': 'Configuration error: acceptance_threshold should be passed'})
        response.status_code = 400
        return response
    if 'avoiding_function_points' not in request_json:
        response = jsonify({'message': 'Configuration error: avoiding_function_points should be passed'})
        response.status_code = 400
        return response
    if 'formulas' not in request_json:
        response = jsonify({'message': 'Configuration error: formulas should be passed'})
        response.status_code = 400
        return response

    acceptance_threshold = request_json['acceptance_threshold']

    for avoidind_function_point in request_json['avoiding_function_points']:
        avoiding_function_points[avoidind_function_point['x']] = avoidind_function_point['value']
    eta = Eta(avoiding_function_points)
    parser = Parser(eta)
    for formula in request_json['formulas']:
        try:
            (formula, new_variables) = parser.parse(formula)
        except Exception as e:
            logging.error('error while parsing formula ' + formula + ': ' + traceback.format_exc())
            continue

        formulas.append(formula)
        for variable in new_variables:
            variables[variable] = 0

    if not len(formulas):
        response = jsonify({'message': 'Configuration error: all formulas failed to parse'})
        response.status_code = 400
        return response

    response = jsonify({'message': 'Server is configured and started'})
    response.status_code = 200
    server_configured = True
    return response

@app.route('/pass_variables', methods=['POST'])
def pass_variables():
    global formulas
    global variables
    global evaluations

    request_json = request.get_json()

    if 'variables' not in request_json:
        response = jsonify({'message': 'Error: variables should be passed'})
        response.status_code = 400
        return response

    for variable in request_json['variables']:
        variables[variable['name']] = variable['value']

    print('Проверяю все существующие формулы')
    evaluation_result = []
    for formula in formulas:
        result = formula.evaluate(variables)
        evaluation_str = '{}: {}'.format(str(formula), result)
        print(evaluation_str)
        evaluation_result.append(evaluation_str)
        if result < acceptance_threshold:
            print('Значение правила {} опустилось ниже порога: {} < {}'.format(formula, result, acceptance_threshold))
            continue
    print('Проверка завершена')

    response = jsonify({'message': 'Проверка завершена', 'results': evaluation_result})
    evaluations.append(evaluation_result)
    response.status_code = 200
    return response

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"background: rgb(209, 209, 209)")
    
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(16)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setStyleSheet(u"background: rgb(232, 232, 232)")

        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Система мониторинга FTL", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Результаты проверки правил:", None))

        QMetaObject.connectSlotsByName(MainWindow)
        self.timer = QTimer(self.centralwidget)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.show_results)

        self.events_shown = 0

    @core.pyqtSlot()
    def show_results(self):
        resp = req.get("http://127.0.0.1:5000/")
        results = resp.json()['results']
        new_size = len(results)
        for i in range(new_size - self.events_shown):
            self.listWidget.addItem(
                'Событие № '
                + str(self.events_shown + i + 1) + ': '
                + str.join(', ', results[self.events_shown + i]['formulas'])
            )
        self.events_shown = new_size
    
    def start(self):
        self.timer.start()
    
    def stop(self):
        self.timer.stop()

def run_pyqt6():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    ui.start()
    sys.exit(app.exec())

if __name__ == '__main__':
    # Start the Flask server in a separate thread
    kwargs = {
        'host': '127.0.0.1',
        'port': 5000 ,
        'threaded' : True,
        'use_reloader': False, 'debug':True
    }
    threading.Thread(target=app.run, daemon = False, kwargs=kwargs).start()

    run_pyqt6()
