import re
import subprocess


class Parser:
    """
    Класс для обработки и вычисления выражения
    """
    def __init__(self):
        self.expr_list = []
        regexp = "[()]|\d+\.\d+|\d+|[+]|[\-]|[*]|[/]|[\^]|sin|cos"
        self.regexp = re.compile(regexp)

    def _parse(self, data: str):
        """
        Парсинг выражения для проверки
        :param data: выражение
        :type data: str
        :return: None
        """
        self.expr_list = re.findall(self.regexp, data)

    def _check_parentheses(self) -> bool:
        """
        Проверка на скобки
        :return: результат проверки
        :rtype: bool
        """
        return self.expr_list.count('(') == self.expr_list.count(')')

    def _check_illegal_characters(self, data):
        """
        Проверка на посторонние символы
        :param data: выражение
        :return: результат проверки
        :rtype: bool
        """
        return len("".join(self.expr_list)) == len(data)

    @staticmethod
    def _calculate(data: str) -> str:
        """
        Вычисление проверенного выражения
        :param data: выражение
        :type data: str
        :return: строковое представление результата
        :rtype: str
        """
        operations = {
            r'sin': 'math.sin',
            r'cos': 'math.cos',
            r'\^': '**'
        }
        # производим подстановку выражений
        for regexp, repl in operations.items():
            data = re.sub(regexp, repl, data)

        x = """
import math
print({})
exit()
            """.format(data)
        cmd = "{}".format(x)
        # создаем процесс python для вычисления выражения
        p = subprocess.Popen(['python3', '-c {}'.format(cmd)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        p.wait()

        # обработка результатов работы процесса
        if out is not None and out != b'':
            return out.decode()
        if err is not None and err != b'':
            e = err.decode()
            if len(re.findall(r'ZeroDivisionError', e)) > 0:
                return "Zero Division"
            if len(re.findall(r'Syntax Error', e)) > 0:
                return "Zero Division"
            else:
                return e
        else:
            return "Unhandled problem"

    def process(self, data) -> str:
        """
        Обработка данных на сервере
        :param data: полученное выражение
        :type data: str
        :return: текст ошибки или вычисленное значение
        :rtype: str
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
