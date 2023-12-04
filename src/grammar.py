import src.constants as const
from src.io_manager import Input, Output


class Grammar:
    def __init__(self,
                 other=None,
                 number_rules=None, number_term=None, number_non_term=None, start_non_terminal=None, rules=None,
                 terminals=None, non_terminals=None, input_manager=None, output_manager=None):
        if other:
            self.__copy_constructor(other)
        elif number_rules:
            self.__value_constructor(number_rules, number_term, number_non_term, start_non_terminal, rules, 
                                     terminals, non_terminals, input_manager, output_manager)
        else:
            self.__default_constructor(input_manager, output_manager)
        self._terminals.add('')

    def __copy_constructor(self, other):
        self._number_rules = other._number_rules
        self._number_term = other._number_term
        self._number_non_term = other._number_non_term
        self._start_non_terminal = other._start_non_terminal
        self._rules = other._rules
        self._terminals = other._terminals
        self._non_terminals = other._non_terminals
        self._input_manager = other._input_manager
        self._output_manager = other._output_manager

    def __value_constructor(self, number_rules, number_term, number_non_term, start_non_terminal, rules, 
                            terminals, non_terminals, input_manager, output_manager):
        self._number_rules = number_rules
        self._number_term = number_term
        self._number_non_term = number_non_term
        self._start_non_terminal = start_non_terminal
        self._rules = rules
        self._terminals = terminals
        self._non_terminals = non_terminals
        self._input_manager = input_manager
        self._output_manager = output_manager

    def __default_constructor(self, input_manager: Input, output_manager: Output):
        self._number_rules = 0
        self._number_term = 0
        self._number_non_term = 0
        self._start_non_terminal = ' '
        self._rules = dict()
        self._terminals = set()
        self._non_terminals = set()
        self._input_manager = input_manager
        self._output_manager = output_manager

    def _read(self) -> None:
        try:
            self._number_non_term, self._number_term, self._number_rules = (
                map(int, self._input_manager.get_line().split()))
        except Exception:
            raise Exception("Invalid type of ∣N∣/∣Σ∣/∣P∣!")
        raw_non_term = [x for x in self._input_manager.get_line()]
        for symb in raw_non_term:
            if symb not in const.CAPS_ALPHABET:
                raise Exception(symb + ": Invalid non-terminal symbol!")
        self._non_terminals = set(raw_non_term)
        raw_term = [x for x in self._input_manager.get_line()]
        for symb in raw_term:
            if symb not in const.ALPHABET:
                raise Exception(symb + ": Invalid terminal symbol!")
        self._terminals = set(raw_term)
        for i in range(self._number_rules):
            new_rule = self._input_manager.get_line()
            if new_rule.find('->') == -1:
                raise Exception("Rule must contain '->'!")
            left, right = new_rule.split('->')
            left = left.replace(' ', '')
            if left not in self._non_terminals:
                raise Exception("Left part of rule must be non-terminal symbol!")
            right = right.replace(' ', '')
            if left not in self._rules:
                self._rules[left] = [right]
            else:
                self._rules[left].append(right)
        self._start_non_terminal = self._input_manager.get_line()

    def info(self) -> list:
        information = [str(self._number_non_term) + ' ' + str(self._number_term) + ' ' + str(self._number_rules)]
        information.append(''.join(map(str, self._non_terminals)))
        information.append(''.join(map(str, self._terminals)))
        for key in self._rules.keys():
            for rhs in self._rules[key]:
                information.append(key + ' -> ' + rhs)
        information.append(self._start_non_terminal)
        return information


if __name__ == '__main__':
    pass
