import unittest
import os
from src.earley import Earley
from src.grammar import Grammar
from src.io_manager import Input, Output


class TestEarleyAlgo(unittest.TestCase):
    def test_input_correctness1(self):
        with open('input.txt', 'w') as file:
            file.write('1 2 s')
        with self.assertRaises(Exception) as context:
            algo = Earley(input_file='input.txt', output_file='')
        self.assertEqual(str(context.exception), "Invalid type of ∣N∣/∣Σ∣/∣P∣!")
        os.remove('input.txt')

    def test_input_correctness2(self):
        with open('input.txt', 'w') as file:
            file.write('1 2 2\nSaABC')
        with self.assertRaises(Exception) as context:
            algo = Earley(input_file='input.txt', output_file='')
        self.assertEqual(str(context.exception), "a: Invalid non-terminal symbol!")
        os.remove('input.txt')

    def test_input_correctness3(self):
        with open('input.txt', 'w') as file:
            file.write('1 2 2\nSABC\nabc3S56dfg')
        with self.assertRaises(Exception) as context:
            algo = Earley(input_file='input.txt', output_file='')
        self.assertEqual(str(context.exception), "S: Invalid terminal symbol!")
        os.remove('input.txt')

    def test_input_correctness4(self):
        with open('input.txt', 'w') as file:
            file.write('1 2 2\nSABC\nabc356dfg\nS -> a\nA - S')
        with self.assertRaises(Exception) as context:
            algo = Earley(input_file='input.txt', output_file='')
        self.assertEqual(str(context.exception), "Rule must contain '->'!")
        os.remove('input.txt')

    def test_input_correctness5(self):
        with open('input.txt', 'w') as file:
            file.write('1 2 2\nSABC\nabc356dfg\nS -> a\n3 -> S\n')
        with self.assertRaises(Exception) as context:
            algo = Earley(input_file='input.txt', output_file='')
        self.assertEqual(str(context.exception), "Left part of rule must be non-terminal symbol!")
        os.remove('input.txt')

    def test_true_predict(self):
        algo = Earley(G=Grammar(number_rules=2, number_term=2, number_non_term=1, start_non_terminal='S',
                                rules={'S': ['aSbS', '']}, non_terminals={'S'}, terminals={'a', 'b'}))
        self.assertEqual(algo.predict('aababb'), True)

    def test_false_predict(self):
        algo = Earley(G=Grammar(number_rules=2, number_term=2, number_non_term=1, start_non_terminal='S',
                                rules={'S': ['aSbS', '']}, non_terminals={'S'}, terminals={'a', 'b'}))
        self.assertEqual(algo.predict('aabbba'), False)

    def test_number_tests_correctness(self):
        input_manager = Input(test_mode=True, given_strings=['lol', 'aababb', 'aabbba'])
        algo = Earley(G=Grammar(number_rules=2, number_term=2, number_non_term=1, start_non_terminal='S',
                                rules={'S': ['aSbS', '']}, non_terminals={'S'}, terminals={'a', 'b'},
                                input_manager=input_manager))
        with self.assertRaises(Exception) as context:
            algo.test()
        self.assertEqual(str(context.exception), "Number of words to predict must be integer!")

    def test_multitest(self):
        input_manager = Input(test_mode=True, given_strings=['2', 'aababb', 'aabbba'])
        output_manager = Output(test_mode=True, file_mode=False)
        algo = Earley(G=Grammar(number_rules=2, number_term=2, number_non_term=1, start_non_terminal='S',
                                rules={'S': ['aSbS', '']}, non_terminals={'S'}, terminals={'a', 'b'},
                                input_manager=input_manager, output_manager=output_manager))
        self.assertEqual(algo.test(), 'Yes\nNo\n')

    def test_grammar_info(self):
        input_manager = Input(test_mode=True, given_strings=['2', 'aababb', 'aabbba'])
        algo = Earley(G=Grammar(number_rules=2, number_term=2, number_non_term=1, start_non_terminal='S',
                                rules={'S': ['aSbS', '']}, non_terminals={'S'}, terminals={'a', 'b'},
                                input_manager=input_manager))
        algo.info()


if __name__ == '__main__':
    unittest.main()
