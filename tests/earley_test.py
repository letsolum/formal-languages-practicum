from src.earley import Earley
from src.grammar import Grammar
from src.bfs import StupidAlgorithm
from random import randint, choice


class TestPrediction:
    def __init__(self, alphabet=('a', 'b', 'c'), length=6, count_words=100):
        self.__alphabet = alphabet
        self.__words = []
        self.__length = length
        self.__count_words = count_words
        self.__checker = None
        self.__algo = None

    def __set_grammar(self, G: Grammar) -> None:
        self.__algo = Earley(G=G)
        self.__checker = StupidAlgorithm(G=G)

    def __generate_grammar(self) -> Grammar:
        non_terminals = {'S'}
        if randint(0, 1):
            non_terminals.add('P')
        terminals = set(self.__alphabet)
        number_rules = randint(1, 10)
        number_non_terminals = len(non_terminals)
        number_terminals = len(terminals)
        rules = dict()
        for _ in range(number_rules):
            lhs = choice(list(non_terminals))
            if lhs not in rules:
                rules[lhs] = []
            rhs = ''
            while randint(0, 2):
                rhs += choice(list(non_terminals.union(terminals)))
            rules[lhs].append(rhs)
        start_non_terminal = choice(list(non_terminals))
        return Grammar(number_rules=number_rules, number_term=number_terminals, number_non_term=number_non_terminals,
                       start_non_terminal=start_non_terminal, rules=rules, terminals=terminals,
                       non_terminals=non_terminals)

    def __generate_words(self) -> None:
        for _ in range(self.__count_words):
            self.__words.append('')
            for i in range(self.__length):
                self.__words[-1] += chr(ord('a') + randint(0, 2))

    def __run_prediction_tests(self) -> None:
        for word in self.__words:
            fir, sec = self.__algo.predict(word), self.__checker.predict(word)
            if fir != sec:
                print(word, self.__algo.predict(word), self.__checker.predict(word))
                assert 1 == 0

    def run(self, cnt_tests=1000):
        for _ in range(cnt_tests):
            print('=========test info=========')
            self.__set_grammar(G=self.__generate_grammar())
            for row in self.__algo.info():
                print(row)
            self.__generate_words()
            self.__run_prediction_tests()


if __name__ == '__main__':
    test = TestPrediction()
    test.run()
