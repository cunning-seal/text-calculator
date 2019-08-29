import math
import re
import subprocess

# классы для выражения (алгоритмическая реализация)


class Expr:
    def __init__(self, priority, op_type):
        self.priority = priority
        self.operation_type = op_type

    def eval(self):
        pass


class Num(Expr):
    """
    Число
    """
    operator_regexp = "\d+\.\d+|\d+"

    def __init__(self, value: float):
        super().__init__(0, "NONE")
        self.value = value

    def eval(self) -> float:
        return self.value


class Add(Expr):
    """
    Сложение
    """
    operator_regexp = "[+]"

    def __init__(self, left: Expr, right: Expr):
        super().__init__(1, "BINAR")
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() + self.right.eval()


class Subtract(Expr):
    """
    Вычитание
    """
    operator_regexp = "[\-]"

    def __init__(self, left: Expr, right: Expr):
        super().__init__(1, "BINAR")
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() - self.right.eval()


class Multiply(Expr):
    """
    Умножение
    """
    operator_regexp = "[*]"

    def __init__(self, left: Expr, right: Expr):
        super().__init__(2, "BINAR")
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() * self.right.eval()


class Division(Expr):
    """
    Деление
    """
    operator_regexp = "[/]"

    def __init__(self, left: Expr, right: Expr):
        super().__init__(2, "BINAR")
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() / self.right.eval()


class Power(Expr):
    """
    Возведение в степень
    """
    operator_regexp = "[\^]"

    def __init__(self, left: Expr, right: Expr):
        super().__init__(3, "BINAR")
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() ** self.right.eval()


class Sin(Expr):
    """
    Синус
    """
    operator_regexp = "sin"

    # TODO какой правильный приоритет для синуса и косинуса?
    def __init__(self, expr: Expr):
        super().__init__(4, "UNAR")
        self.expr = expr

    def eval(self):
        return math.sin(self.expr.eval())


class Cos(Expr):
    """
    Косинус
    """
    operator_regexp = "cos"

    def __init__(self, expr: Expr):
        super().__init__(4, "UNAR")
        self.expr = expr

    def eval(self):
        return math.cos(self.expr.eval())


class LeftParentheses(Expr):
    """
    Левая скобка
    """
    operator_regexp = "[(]"

    def __init__(self):
        super().__init__(0, "NONE")

    def eval(self):
        pass


class RightParentheses(Expr):
    """
    Левая скобка
    """
    operator_regexp = "[)]"

    def __init__(self):
        super().__init__(0, "NONE")

    def eval(self):
        pass


class Parser:

    legal_operators = [Num, Add, Subtract, Multiply, Division, Power, Sin, Cos]

    def __init__(self):
        self.expr_list = []
        regexp = "[()]|" + "|".join([x.operator_regexp for x in self.legal_operators])
        self.regexp = re.compile(regexp)

    def _parse(self, data: str):
        self.expr_list = re.findall(self.regexp, data)

    def _check_parentheses(self):
        return self.expr_list.count('(') == self.expr_list.count(')')

    def _check_illegal_characters(self, data):
        return len("".join(self.expr_list)) == len(data)

    @staticmethod
    def _calculate(data: str) -> str:

        # алгоритмическая реализация
        #
        # empty_expr = Expr(-1, "NONE")
        # empty_expr_2 = Expr(-1, "NONE")
        # operations_stack = []
        # values_stack = []
        #
        #
        # for e in self.expr_list:
        #     try:
        #         tmp = float(e)
        #         values_stack.append(Num(tmp))
        #         continue
        #     except ValueError:
        #         pass
        #
        #     if e == "+":
        #         op_obj = Add(empty_expr, empty_expr_2)
        #     elif e == "*":
        #         op_obj = Multiply(empty_expr, empty_expr_2)
        #     elif e == "-":
        #         op_obj = Subtract(empty_expr, empty_expr_2)
        #     elif e == "/":
        #         op_obj = Division(empty_expr, empty_expr_2)
        #     elif e == "sin":
        #         op_obj = Sin(empty_expr)
        #     elif e == "(":
        #         op_obj = LeftParenthes()
        #     elif e == ")":
        #         op_obj = RightParenthes()
        #     else:
        #         pass
        #
        #     if len(operations_stack) > 0:
        #         tmp_op = operations_stack[-1]
        #         if op_obj.priority > tmp_op.priority:
        #             if tmp_op.operation_type != "NONE":
        #                 operations_stack.append(op_obj)
        #                 continue
        #             else:
        #                 operations_stack.pop()
        #                 continue
        #         else:
        #             tmp_op = operations_stack.pop()
        #
        #             op_type = tmp_op.operation_type
        #             if op_type == "UNAR":
        #                 arg = values_stack.pop()
        #                 tmp_op.expr = arg
        #                 res = tmp_op.eval()
        #                 values_stack.append(Num(res))
        #             elif op_type == "BINAR":
        #                 arg2 = values_stack.pop()
        #                 arg1 = values_stack.pop()
        #                 tmp_op.left = arg1
        #                 tmp_op.right = arg2
        #                 try:
        #                     res = tmp_op.eval()
        #                 except ZeroDivisionError:
        #                     return "Zero devision"
        #                 values_stack.append(Num(res))
        #             else:
        #                 pass
        #
        #     operations_stack.append(op_obj)
        #
        # for op in range(len(operations_stack)):
        #     tmp_op = operations_stack.pop()
        #     op_type = tmp_op.operation_type
        #     if op_type == "UNAR":
        #         arg = values_stack.pop()
        #         tmp_op.expr = arg
        #         res = tmp_op.eval()
        #         values_stack.append(Num(res))
        #     elif op_type == "BINAR":
        #         arg2 = values_stack.pop()
        #         arg1 = values_stack.pop()
        #         tmp_op.left = arg1
        #         tmp_op.right = arg2
        #         try:
        #             res = tmp_op.eval()
        #         except ZeroDivisionError:
        #             return "Zero devision"
        #         values_stack.append(Num(res))
        #
        # result = values_stack[0].value
        # return str(result)

        operations = {
            r'sin': 'math.sin',
            r'cos': 'math.cos',
            r'\^': '**'
        }

        for regexp, repl in operations.items():
            data = re.sub(regexp, repl, data)

        x = """
import math
print({})
exit()
            """.format(data)
        cmd = "{}".format(x)
        p = subprocess.Popen(['python3', '-c {}'.format(cmd)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = p.communicate()

        p.wait()

        if out is not None and out != b'':
            return out.decode()
        if err is not None and err != b'':
            e = err.decode()
            if len(re.findall(r'ZeroDivisionError', e)) > 0:
                return "Zero Division"
            else:
                return e
        else:
            return "Unhandled problem"

    def process(self, data) -> str:
        """

        :param data:
        :return:
        """
        error_response = ""
        success_check = True
        self._parse(data)
        if not self._check_parentheses():
            error_response += "Unpaired brackets\n"
            success_check = False
        if not self._check_illegal_characters(data):
            error_response += "Illegal symbols\n"
            success_check = False

        if success_check:
            resp = self._calculate(data)
            return resp
        else:
            return error_response
