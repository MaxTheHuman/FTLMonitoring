import requests as req
import random

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

def checkAlways():
    reset_server()

    formulas = ['Gx']
    configure_server(formulas)

    minimum = 1
    for _ in range(10):
        value = random.uniform(0, 1)
        minimum = min(minimum, value)
        variables = {'x': value}
        resp = pass_variables(variables)
        assert(resp['results'][-1] == 'Gx: {}'.format(minimum))

    print('operator Always PASSED')

def checkUntil():
    reset_server()

    formulas = ['(xUy)']
    configure_server(formulas)

    prev_x_minimum = 1
    for _ in range(10):
        x_value = random.uniform(0, 1)
        y_value = random.uniform(0, 1)
        variables = {'x': x_value, 'y': y_value}

        resp = pass_variables(variables)
        
        result = max(min(prev_x_minimum, x_value), min(prev_x_minimum, y_value))
        prev_x_minimum = min(prev_x_minimum, x_value)
        assert(resp['results'][-1] == 'xUy: {}'.format(result))
    print('operator Until PASSED')

def checkAlmostAlways():
    reset_server()

    formulas = ['AGx']
    avoiding_function_points = {0: 1, 2: 0.5, 3: 0.1, 5: 0}
    configure_server(formulas, avoiding_function_points)

    resp = pass_variables({'x': 1})
    assert(resp['results'][-1] == 'AGx: 1')
    # then pass only 0's - AG will copy avoiding function
    resp = pass_variables({'x': 0})
    assert(resp['results'][-1] == 'AGx: 0.75')  # eta(1) = 0.75 - between 1 and 0.5
    resp = pass_variables({'x': 0})
    assert(resp['results'][-1] == 'AGx: 0.5')
    resp = pass_variables({'x': 0})
    assert(resp['results'][-1] == 'AGx: 0.1')
    resp = pass_variables({'x': 0})
    assert(resp['results'][-1] == 'AGx: 0.05') # eta(4) = 0.05 - between 0.1 and 0
    resp = pass_variables({'x': 0})
    assert(resp['results'][-1] == 'AGx: 0')

    reset_server()

    formulas = ['AGx']
    avoiding_function_points = {0: 1, 4: 0}  # maximum 3 avoidings
    configure_server(formulas, avoiding_function_points)

    resp = pass_variables({'x': 1})
    assert(resp['results'][-1] == 'AGx: 1')
    resp = pass_variables({'x': 0.001})
    assert(resp['results'][-1] == 'AGx: 0.75')  # avoid 1 event
    resp = pass_variables({'x': 1})
    assert(resp['results'][-1] == 'AGx: 0.75')
    resp = pass_variables({'x': 0.006})
    assert(resp['results'][-1] == 'AGx: 0.5')  # avoid 2 events
    resp = pass_variables({'x': 0.005})
    assert(resp['results'][-1] == 'AGx: 0.25')  # avoid 3 events
    resp = pass_variables({'x': 1})
    assert(resp['results'][-1] == 'AGx: 0.25')
    resp = pass_variables({'x': 0.004})
    assert(resp['results'][-1] == 'AGx: 0.003')  # = 0.004 * 0.75; avoid 1 minimal
    resp = pass_variables({'x': 0.003})
    assert(resp['results'][-1] == 'AGx: 0.0022500000000000003')
    resp = pass_variables({'x': 1})
    assert(resp['results'][-1] == 'AGx: 0.0022500000000000003')
    resp = pass_variables({'x': 0.002})
    assert(resp['results'][-1] == 'AGx: 0.0015')
    resp = pass_variables({'x': 0.001})
    assert(resp['results'][-1] == 'AGx: 0.001')
    resp = pass_variables({'x': 0})
    assert(resp['results'][-1] == 'AGx: 0.00075')  # do not avoid at all
    
    print('operator Almost Always PASSED')

def checkAlmostUntil():
    reset_server()

    formulas = ['(xAUy)']
    avoiding_function_points = {0: 1, 4: 0}
    configure_server(formulas, avoiding_function_points)

    resp = pass_variables({'x': 1, 'y': 0})
    assert(resp['results'][-1] == 'xAUy: 1')
    # then pass only 0's - AG will copy avoiding function
    resp = pass_variables({'x': 0, 'y': 0})
    assert(resp['results'][-1] == 'xAUy: 0.75')
    resp = pass_variables({'x': 0, 'y': 0})
    assert(resp['results'][-1] == 'xAUy: 0.5')
    resp = pass_variables({'x': 0, 'y': 0})
    assert(resp['results'][-1] == 'xAUy: 0.25')
    resp = pass_variables({'x': 0, 'y': 1})
    assert(resp['results'][-1] == 'xAUy: 0.25')

    print('operator Almost Until PASSED')

def checkAlmostAlwaysInsideAlmostAlways():
    reset_server()

    formulas = ['AG((x\/y)->AG(z))']  # 'AG((x/\!y)->(xAUz))'
    avoiding_function_points = {0: 1, 4: 0}
    configure_server(formulas, avoiding_function_points)

    resp = pass_variables({'x': 0, 'y': 0, 'z': 0})
    assert(resp['results'][-1] == 'AG((xVy)→AGz): 1')
    resp = pass_variables({'x': 1, 'y': 0, 'z': 0})
    assert(resp['results'][-1] == 'AG((xVy)→AGz): 0.75')
    resp = pass_variables({'x': 0, 'y': 1, 'z': 0})
    assert(resp['results'][-1] == 'AG((xVy)→AGz): 0.5')
    resp = pass_variables({'x': 1, 'y': 0, 'z': 1})
    assert(resp['results'][-1] == 'AG((xVy)→AGz): 0.25')
    resp = pass_variables({'x': 0, 'y': 1, 'z': 1})
    assert(resp['results'][-1] == 'AG((xVy)→AGz): 0.125')
    resp = pass_variables({'x': 0, 'y': 1, 'z': 1})
    assert(resp['results'][-1] == 'AG((xVy)→AGz): 0.125')

    print('operator Almost Until inside Almost Until PASSED')

def checkAlmostUntilInsideAlmostAlways():
    reset_server()

    formulas = ['AG((x/\!y)->(xAUz))']
    avoiding_function_points = {0: 1, 4: 0}
    configure_server(formulas, avoiding_function_points)

    resp = pass_variables({'x': 0, 'y': 0, 'z': 0})
    assert(resp['results'][-1] == 'AG((x∧¬y)→xAUz): 1')
    resp = pass_variables({'x': 1, 'y': 0, 'z': 0})
    assert(resp['results'][-1] == 'AG((x∧¬y)→xAUz): 0.75')
    resp = pass_variables({'x': 0, 'y': 1, 'z': 0})
    assert(resp['results'][-1] == 'AG((x∧¬y)→xAUz): 0.75')
    resp = pass_variables({'x': 1, 'y': 0, 'z': 1})
    assert(resp['results'][-1] == 'AG((x∧¬y)→xAUz): 0.5625')
    resp = pass_variables({'x': 0, 'y': 1, 'z': 1})
    assert(resp['results'][-1] == 'AG((x∧¬y)→xAUz): 0.5625')

    print('operator Almost Until inside Almost Until PASSED')

if __name__ == '__main__':
    checkAlways()
    checkUntil()
    checkAlmostAlways()
    checkAlmostUntil()
    checkAlmostAlwaysInsideAlmostAlways()
    checkAlmostUntilInsideAlmostAlways()
