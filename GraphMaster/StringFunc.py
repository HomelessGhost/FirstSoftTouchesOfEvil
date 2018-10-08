import math


class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.value = None
        self.operation = None


class StringFunction:

    operations = {'+': 1,
                  '-': 1,
                  '*': 2,
                  '/': 2,
                  '^': 3,
                  's': 4,
                  'S': 4,
                  'c': 4,
                  'C': 4,
                  't': 4,
                  'T': 4,
                  'l': 4,
                  'L': 4,
                  'a': 4,
                  'e': 4
                  }

    binary_operations = {'+', '-', '*', '/', '^'}

    def __init__(self, function_str):
        self.root = Node()
        self.func_str = self.refactor_func_str(function_str)
        self.x_nodes = []
        self.build_function(self.func_str, self.root)
        self.zero_division = False

    def build_function(self, func_str, node):
        depth, ind = 0, 0
        is_operation_found = False
        current_operation_ind = None
        current_priority = 9999999
        len_str = len(func_str)
        while ind != len_str:
            # Defining depth on the current step
            if func_str[ind] == '(':
                depth += 1
            if func_str[ind] == ')':
                depth -= 1

            if depth == 0:
                if func_str[ind] in StringFunction.operations and current_priority >= StringFunction.operations.get(func_str[ind], 999):
                    is_operation_found = True
                    current_priority = StringFunction.operations[func_str[ind]]
                    current_operation_ind = ind

            ind += 1

        if is_operation_found:
            operation = func_str[current_operation_ind]
            node.operation = operation

            if operation in StringFunction.binary_operations:
                node.right = Node()
                node.left = Node()

                self.build_function(func_str[0: current_operation_ind], node.left)
                self.build_function(func_str[current_operation_ind + 1: len_str + 1], node.right)

            else:
                node.right = Node()
                self.build_function(func_str[current_operation_ind + 2: len_str - 1], node.right)

        else:
            if func_str[0] == '(':
                self.build_function(func_str[1: len_str - 1], node)
            elif func_str == 'x':
                self.x_nodes.append(node)
            else:
                node.value = float(func_str)

    def calculate(self, root):
        if root.operation is None:
            return None
        if root.operation in StringFunction.binary_operations:
            self.calculate(root.left)
            self.calculate(root.right)
            if root.operation == '+': root.value = root.left.value + root.right.value
            if root.operation == '*': root.value = root.left.value * root.right.value
            if root.operation == '-': root.value = root.left.value - root.right.value
            if root.operation == '^': root.value = root.left.value ** root.right.value
            if root.operation == '/':
                if root.right.value == 0.0:
                    self.zero_division = True
                    return None
                else: root.value = root.left.value / root.right.value

        else:
            self.calculate(root.right)
            if root.operation == 's': root.value = math.sin(root.right.value)
            if root.operation == 'S': root.value = math.sinh(root.right.value)
            if root.operation == 'c': root.value = math.cos(root.right.value)
            if root.operation == 'C': root.value = math.cosh(root.right.value)
            if root.operation == 't': root.value = math.tan(root.right.value)
            if root.operation == 'T': root.value = math.tanh(root.right.value)
            if root.operation == 'l': root.value = math.log(root.right.value)
            if root.operation == 'L': root.value = math.log10(root.right.value)
            if root.operation == 'a': root.value = math.fabs(root.right.value)
            if root.operation == 'e': root.value = math.exp(root.right.value)

    def get_answer(self):
        if self.zero_division:
            self.zero_division = False
            return math.inf
        return self.root.value

    def calculate_f(self, x):
        for i in self.x_nodes:
            i.value = x
        self.calculate(self.root)
        return self.get_answer()

    def refactor_func_str(self, string):
        string = string.replace(' ', '')
        if string[0] == '-':
            string = '0' + string

        string = string.replace('sin', 's')
        string = string.replace('sinh', 'S')
        string = string.replace('sh', 'S')
        string = string.replace('cos', 's')
        string = string.replace('cosh', 'S')
        string = string.replace('ch', 'S')
        string = string.replace('tan', 't')
        string = string.replace('tanh', 'T')
        string = string.replace('tg', 't')
        string = string.replace('th', 'T')
        string = string.replace('ln', 'l')
        string = string.replace('log', 'L')
        string = string.replace('abs', 'a')
        string = string.replace('exp', 'e')

        len_str = len(string)
        ind = 0
        while ind < len_str - 1:
            if string[ind] == '(' and string[ind + 1] == '-':
                string = string[:ind + 1] + '0' + string[ind + 1:]
                len_str += 1
            ind += 1
        return string








