import heapq

from sortedcontainers import SortedList

n_eta = 1

def t_norm(a, b):
    return min(a, b)

def t_conorm(a, b):
    return max(a, b)

class Formula:
    formula1 = None
    formula2 = None
    
    def __init__(self):
        raise NotImplementedError
    
    def __repr__(self):
        return str(self.formula1)
    
    # variables is a dict (variable name)->(value)
    def evaluate(self, variables):
        raise NotImplementedError

class Conjunction(Formula):
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2
    
    def __repr__(self):
        return "({}∧{})".format(str(self.formula1), str(self.formula2))
    
    def evaluate(self, variables):
        return min(self.formula1.evaluate(variables), self.formula2.evaluate(variables))

class Disjunction(Formula):
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def __repr__(self):
        return "({}v{})".format(str(self.formula1), str(self.formula2))

    def evaluate(self, variables):
        return max(self.formula1.evaluate(variables), self.formula2.evaluate(variables))

class Implication(Formula):
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def __repr__(self):
        return "({}→{})".format(str(self.formula1), str(self.formula2))
        
    def evaluate(self, variables):
        return max(1 - self.formula1.evaluate(variables), self.formula2.evaluate(variables))

class Negation(Formula):
    def __init__(self, formula):
        self.formula1 = formula
    
    def __repr__(self):
        return "¬{}".format(str(self.formula1))
        
    def evaluate(self, variables):
        return 1 - self.formula1.evaluate(variables)

class Variable(Formula):
    def __init__(self, variable):
        self.formula1 = variable
    
    def evaluate(self, variables):
        return variables[self.formula1]

class Always(Formula):
    def __init__(self, formula, accumulated_result = 1):
        self.formula1 = formula
        self.accumulated_result = accumulated_result
    
    def __repr__(self):
        return "G{}".format(str(self.formula1))
        
    def evaluate(self, variables):
        result = t_norm(self.accumulated_result, self.formula1.evaluate(variables))
        self.accumulated_result = result
        return result

class WeakUntil(Formula):
    def __init__(self, formula1, formula2, always_step_before = 1):
        self.formula1 = formula1
        self.formula2 = formula2
        self.always_step_before = always_step_before
        self.max = 0
    
    def __repr__(self):
        return "{}U{}".format(str(self.formula1), str(self.formula2))
        
    def evaluate(self, variables):
        condition = self.formula2.evaluate(variables)
        current_always = t_norm(self.always_step_before, self.formula1.evaluate(variables))
        current_max = max(t_norm(self.always_step_before, condition), current_always)
        self.max = max(self.max, current_max)
        self.always_step_before = current_always
        return self.max

class Eta():
    def __init__(self, avoiding_function_points):
        self.avoiding_function_points = avoiding_function_points
    def n_eta(self):
        return self.avoiding_function_points.peekitem()[0]
    def evaluate(self, n):
        if n == 0:
            return 1
        if n >= self.n_eta():
            return 0
        left_key = next(self.avoiding_function_points.irange(maximum=n, reverse=True))
        left_value = self.avoiding_function_points[left_key]
        if n == left_key:
            return left_value
        right_key = next(self.avoiding_function_points.irange(minimum=n))
        right_value = self.avoiding_function_points[right_key]
        return left_value + (right_value - left_value) / (right_key - left_key) * (n - left_key)

class AlmostAlways(Formula):
    def __init__(self, formula, eta):
        self.formula1 = formula
        self.minheap = []
        self.accumulated_result = 1
        self.min_eta = SortedList()
        self.eta = eta
        self.n_eta = eta.n_eta()

    def __repr__(self):
        return "AG{}".format(str(self.formula1))

    def evaluate(self, variables):
        formula_result = self.formula1.evaluate(variables)
        heapq.heappush(self.minheap, formula_result)
        heap_len = len(self.minheap)
        current_minheap = self.minheap.copy()
        current_max = 0
        if (heap_len < self.n_eta):
            self.min_eta.add(formula_result)
            accumulated = 1
            for i in range(1, heap_len + 1):
                current_min_value = self.min_eta[heap_len - i]
                accumulated = t_norm(accumulated, current_min_value)
                current_max = max(current_max, accumulated * self.eta.evaluate(heap_len - i))
        else:
            new_min_eta = SortedList()
            for i in range(self.n_eta - 1):
                new_min_eta.add(heapq.heappop(current_minheap))
            if (new_min_eta != self.min_eta):
                self.accumulated_result = t_norm(self.accumulated_result, heapq.heappop(current_minheap))
                self.min_eta = new_min_eta
            else:
                self.accumulated_result = t_norm(self.accumulated_result, formula_result)
            current_max = max(current_max, self.accumulated_result * self.eta.evaluate(self.n_eta - 1))
            accumulated_copy = self.accumulated_result
            i = 0
            for curr_min in reversed(new_min_eta):
                accumulated_copy = t_norm(accumulated_copy, curr_min)
                current_max = max(current_max, accumulated_copy * self.eta.evaluate(self.n_eta - 2 - i))
                i += 1
        return current_max

class AlmostWeakUntil(Formula):
    def __init__(self, formula1, formula2, eta):
        self.formula1 = formula1
        self.formula2 = formula2
        self.minheap = []
        self.accumulated_result = 1
        self.min_eta = SortedList()
        self.always_step_before = 1
        self.eta = eta
        self.n_eta = eta.n_eta()
    
    def __repr__(self):
        return "{}AU{}".format(str(self.formula1),str(self.formula2))
        
    def evaluate(self, variables):
        formula_result = self.formula1.evaluate(variables)
        condition_result = self.formula2.evaluate(variables)
        heapq.heappush(self.minheap, formula_result)
        heap_len = len(self.minheap)
        current_minheap = self.minheap.copy()
        current_always_max = 0
        if (heap_len < self.n_eta):
            self.min_eta.add(formula_result)
            accumulated = 1
            for i in range(1, heap_len + 1):
                current_min_value = self.min_eta[heap_len - i]
                accumulated = t_norm(accumulated, current_min_value)
                current_always_max = max(current_always_max, current_min_value * self.eta.evaluate(heap_len - i))
        else:
            new_min_eta = SortedList()
            for i in range(self.n_eta - 1):
                new_min_eta.add(heapq.heappop(current_minheap))
            if (new_min_eta != self.min_eta):
                self.accumulated_result = t_norm(self.accumulated_result, heapq.heappop(current_minheap))
                self.min_eta = new_min_eta
            else:
                self.accumulated_result = t_norm(self.accumulated_result, formula_result)
            current_always_max = max(current_always_max, self.accumulated_result * self.eta.evaluate(self.n_eta - 1))
            accumulated_copy = self.accumulated_result
            i = 0
            for curr_min in reversed(new_min_eta):
                accumulated_copy = t_norm(accumulated_copy, curr_min)
                current_always_max = max(current_always_max, accumulated_copy * self.eta.evaluate(self.n_eta - 2 - i))
                i += 1
        current_max = max(current_always_max, t_norm(self.always_step_before, condition_result))
        self.always_step_before = current_always_max
        return current_max
