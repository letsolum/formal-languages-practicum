from src.grammar import Grammar
import src.constants as const
from src.io_manager import Input, Output

class Earley(Grammar):
    def __init__(self, input_file=None, output_file=None, G=None):
        if G:
            super().__init__(other=G)
        else:
            super().__init__(input_manager=Input(file_mode=input_file != '', file_name=input_file, test_mode=False),
                             output_manager=Output(file_mode=output_file != '', file_name=output_file, test_mode=False))

    def fit(self, G: Grammar) -> None:  # should not be implemented
        pass

    def predict(self, word: str) -> bool:
        self._rules[const.S_] = [self._start_non_terminal]  # create S' -> S
        self._non_terminals.add(const.S_)
        length = len(word)
        indicator = [[] for _ in range(length + 1)]
        indicator[0].append((const.S_, const.DOT + self._start_non_terminal, 0))
        self.__iteration_complete_predict(0, indicator, word)
        for right in range(1, length + 1):
            self.__iteration_scan(indicator, right - 1, word)
            self.__iteration_complete_predict(right, indicator, word)
        self._rules.pop(const.S_)
        self._non_terminals.remove(const.S_)
        return (const.S_, self._start_non_terminal + const.DOT, 0) in indicator[-1]

    def __iteration_complete_predict(self, right, indicator, word):
        changed = self.__iteration_complete(indicator, right, word)
        changed |= self.__iteration_predict(indicator, right, word)
        while changed:
            changed = self.__iteration_complete(indicator, right, word)
            changed |= self.__iteration_predict(indicator, right, word)

    def __iteration_predict(self, indicator: list, right: int, word: str) -> bool:
        changed = False
        for lhs, rhs, left in indicator[right]:
            dot_index = rhs.find(const.DOT)
            if dot_index != len(rhs) - 1 and rhs[dot_index + 1] in self._rules:
                for rule in self._rules[rhs[dot_index + 1]]:
                    changed |= self.__add(indicator[right], (rhs[dot_index + 1], const.DOT + rule, right))
        return changed

    def __iteration_complete(self, indicator: list, right: int, word: str) -> bool:
        changed = False
        for lhs, rhs, left in indicator[right]:
            dot_index = rhs.find(const.DOT)
            if dot_index == len(rhs) - 1:
                for prev_lhs, prev_rhs, prev_left in indicator[left]:
                    prev_dot_index = prev_rhs.find(const.DOT + lhs)
                    if prev_dot_index != -1:
                        changed |= self.__add(indicator[right],
                                              (prev_lhs, prev_rhs[:prev_dot_index] + lhs + const.DOT
                                               + prev_rhs[prev_dot_index + 2:], prev_left))
        return changed

    def __iteration_scan(self, indicator: list, right: int, word: str):
        for lhs, rhs, left in indicator[right]:
            dot_index = rhs.find(const.DOT)
            if (dot_index != len(rhs) - 1 and rhs[dot_index + 1] in self._terminals and right != len(word) and
                    word[right] == rhs[dot_index + 1]):
                self.__add(indicator[right + 1],
                           (lhs, rhs[:dot_index] + word[right] + const.DOT + rhs[dot_index + 2:], left))

    @staticmethod
    def __add(situations: list, obj: tuple):
        if obj in situations:
            return False
        situations.append(obj)
        return True

    def input(self) -> None:
        self._read()

    def test(self):
        number_words = 0
        try:
            number_words = int(self._input_manager.get_line())
        except Exception:
            raise Exception("Number of words to predict must be integer!")
        answer = ''
        for test in range(number_words):
            word = self._input_manager.get_line()
            result = self.predict(word)
            answer += 'Yes' * result + 'No' * (not result) + '\n'
        return self._output_manager.output_line(answer)
