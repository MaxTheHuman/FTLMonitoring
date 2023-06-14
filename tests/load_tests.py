import requests as req
import random
import time

import numpy as np
import matplotlib.pyplot as plt

def configure_server(formulas, avoiding_function_points = {0: 1, 10: 0}, acceptance_threshold = 0.5):
    resp = req.post("http://127.0.0.1:5000/configure_and_start", json={
        "acceptance_threshold": acceptance_threshold,
        "avoiding_function_points": [
            {
                "x": x,
                "value": y
            } for x, y in avoiding_function_points.items()
        ],
        "formulas": formulas
    })
    assert(resp.status_code == 200)

def reset_server():
    req.get("http://127.0.0.1:5000/reset")

def pass_variables(variables):
    resp = req.post("http://127.0.0.1:5000/pass_variables", json={
        "variables": [
            {
                "name": name,
                "value": value
            } for name, value in variables.items()
        ]
    })
    assert(resp.status_code == 200)
    return resp.json()

def measureDiffentRulesNumber():
    print("Measure different formulas number")
    formulas_set = [
        'AGx', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        '(yAUx)', 'AG(x/\z)', 'G(x\/(y->z))', '((x->y)U(x->z))', 'AG(x\/!y)',
        'AGy', 'G(!x\/y)', '(xAUy)', '(z->Gy)', '(!yU(z->x))',
        'AGz', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        'G(x\/(y->z))', '((x->y)U(x->z))', 'AG(x\/!y)', '(yAUx)', 'AG(x/\z)',
        'AG(x\/!y)', '(yAUx)', 'AG(x/\z)', '((x->y)U(x->z))', 'AG(x\/!y)',
        'AGz', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        'AGy', 'G(!x\/y)', '(xAUy)', '(z->Gy)', '(!yU(z->x))',
        'G(x\/(y->z))', '((x->y)U(x->z))', '(yAUx)', 'AG(x/\z)', 'G(x\/(y->z))',
        'AGx', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        'AGx', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        '(yAUx)', 'AG(x/\z)', 'G(x\/(y->z))', '((x->y)U(x->z))', 'AG(x\/!y)',
        'AGy', 'G(!x\/y)', '(xAUy)', '(z->Gy)', '(!yU(z->x))',
        'AGz', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        'G(x\/(y->z))', '((x->y)U(x->z))', 'AG(x\/!y)', '(yAUx)', 'AG(x/\z)',
        'AG(x\/!y)', '(yAUx)', 'AG(x/\z)', '((x->y)U(x->z))', 'AG(x\/!y)',
        'AGz', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        'AGy', 'G(!x\/y)', '(xAUy)', '(z->Gy)', '(!yU(z->x))',
        'G(x\/(y->z))', '((x->y)U(x->z))', '(yAUx)', 'AG(x/\z)', 'G(x\/(y->z))',
        'AGx', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        'AGx', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        '(yAUx)', 'AG(x/\z)', 'G(x\/(y->z))', '((x->y)U(x->z))', 'AG(x\/!y)',
        'AGy', 'G(!x\/y)', '(xAUy)', '(z->Gy)', '(!yU(z->x))',
        'AGz', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        'G(x\/(y->z))', '((x->y)U(x->z))', 'AG(x\/!y)', '(yAUx)', 'AG(x/\z)',
        'AG(x\/!y)', '(yAUx)', 'AG(x/\z)', '((x->y)U(x->z))', 'AG(x\/!y)',
        'AGz', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        'AGy', 'G(!x\/y)', '(xAUy)', '(z->Gy)', '(!yU(z->x))',
        'G(x\/(y->z))', '((x->y)U(x->z))', '(yAUx)', 'AG(x/\z)', 'G(x\/(y->z))',
        'AGx', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        'AGx', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        '(yAUx)', 'AG(x/\z)', 'G(x\/(y->z))', '((x->y)U(x->z))', 'AG(x\/!y)',
        'AGy', 'G(!x\/y)', '(xAUy)', '(z->Gy)', '(!yU(z->x))',
        'AGz', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        'G(x\/(y->z))', '((x->y)U(x->z))', 'AG(x\/!y)', '(yAUx)', 'AG(x/\z)',
        'AG(x\/!y)', '(yAUx)', 'AG(x/\z)', '((x->y)U(x->z))', 'AG(x\/!y)',
        'AGz', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        'AGy', 'G(!x\/y)', '(xAUy)', '(z->Gy)', '(!yU(z->x))',
        'G(x\/(y->z))', '((x->y)U(x->z))', '(yAUx)', 'AG(x/\z)', 'G(x\/(y->z))',
        'AGx', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))'
    ]

    measurements = []
    
    def measure_n_formulas(n):
        reset_server()
        configure_server(formulas_set[0:n])

        start = time.time()
        for _ in range(10000):
            variables = {'x': random.uniform(0, 1), 'y': random.uniform(0, 1), 'z': random.uniform(0, 1)}
            pass_variables(variables)
        end = time.time()
        print('{} formulas time: {} sec'.format(n, end - start))
        measurements.append(end - start)
    
    n_formulas = [2, 10, 25, 50, 100, 150, 200]
    for n in n_formulas:
        measure_n_formulas(n)
    
    plt.plot(n_formulas, measurements)
    plt.xlabel('Количество формул')
    plt.ylabel('Время вычисления правил на 1000 состояний, секунды')
    plt.show()

def measureDiffentNEta():
    print("Measure different n_eta")
    formulas = [
        'AGx', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        '(yAUx)', 'AG(x/\z)', 'G(x\/(y->z))', '((x->y)U(x->z))', 'AG(x\/!y)'
    ]

    measurements = []
    
    def measure_n_eta(n):
        reset_server()
        configure_server(formulas, {0:1, n: 0})

        start = time.time()
        for _ in range(10000):
            variables = {'x': random.uniform(0, 1), 'y': random.uniform(0, 1), 'z': random.uniform(0, 1)}
            pass_variables(variables)
        end = time.time()
        print('n_eta {}, time: {} sec'.format(n, end - start))
        measurements.append(end - start)
    
    n_eta = [1, 10, 50, 100, 250, 500, 750, 1000]
    for n in n_eta:
        measure_n_eta(n)
    
    plt.plot(n_eta, measurements)
    plt.xlabel('$n_\\eta$')
    plt.ylabel('Время вычисления правил на 1000 состояний, секунды')
    plt.show()

def measureManyEvents():
    print("Measure events evaluation from 1 to 1.000.000")
    formulas = [
        'AGx', 'G(x\/y)', '(xUy)', '(x->Gy)', '(yU(z\/!x))',
        '(yAUx)', 'AG(x/\z)', 'G(x\/(y->z))', '((x->y)U(x->z))', 'AG(x\/!y)'
    ]

    measurements = []
    total_measurements = []

    reset_server()
    configure_server(formulas, {0:1, 100: 0})

    common_start = time.time()
    for i in range(1, 1000001):
        variables = {'x': random.uniform(0, 1), 'y': random.uniform(0, 1), 'z': random.uniform(0, 1)}
        start = time.time()
        pass_variables(variables)
        end = time.time()
        if i % 1000 == 0:
            print('event {}, time: {} sec'.format(i, end - start))
            print('total 1000 events time: {} sec'.format(end - common_start))
            total_measurements.append(end - common_start)
            measurements.append(end - start)
            common_start = end

    with open("total_measurements.txt", "w") as txt_file1:
        for value in total_measurements:
            txt_file1.write(str(value) + ', ')
    with open("measurements.txt", "w") as txt_file2:
        for value in measurements:
            txt_file2.write(str(value) + ', ')

    plt.plot(np.arange(1, 1000001, 1000), total_measurements)
    plt.xlabel('Количество состояний')
    plt.ylabel('Время вычисления правил на 1000 состояний, секунды')
    plt.show()

if __name__ == '__main__':
    measureDiffentRulesNumber()
    measureDiffentNEta()
    measureManyEvents()
