from src.grammar import Grammar
from src.io_manager import Input, Output
import src.constants as const
from copy import deepcopy as copy


class Configuration:
    def __init__(self, rule, next_smb, pnt_pos):
        self.rule = rule
        self.next_smb = next_smb
        self.pnt_pos = pnt_pos

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return ((self.rule == other.rule) and
                    (self.next_smb == other.next_smb) and
                    (self.pnt_pos == other.pnt_pos))
        return False

    def __hash__(self):
        return hash((self.rule, self.next_smb, self.pnt_pos))


class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        if isinstance(other, Rule):
            return (self.left == other.left) and (self.right == other.right)
        return False

    def __hash__(self):
        return hash((self.left, self.right))


class Node:
    def __init__(self):
        self.children = {}
        self.confs = set()

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.confs == other.confs
        return False

    def __hash__(self):
        return hash(tuple(self.confs))


class Shift:
    def __init__(self, to):
        self.to = to


class Reduce:
    def __init__(self, rule):
        self.rule = rule


class LR1(Grammar):
    def __init__(self, input_file=None, output_file=None, G=None):
        if G:
            super().__init__(other=G)
        else:
            super().__init__(input_manager=Input(file_mode=input_file != '', file_name=input_file, test_mode=False),
                             output_manager=Output(file_mode=output_file != '', file_name=output_file, test_mode=False))

    def fit(self):
        self.nodes = [Node()]
        self.nodes[0].confs.add(Configuration(Rule(const.S_, self._start_non_terminal),
                                              const.END, 0))
        self.nodes[0] = self.closure(self.nodes[0])
        self.start_node = {self.nodes[0]}
        i = 0
        while i < len(self.nodes):
            processed = set()
            for conf in self.nodes[i].confs:
                if ((len(conf.rule.right) > conf.pnt_pos) and
                        (conf.rule.right[conf.pnt_pos] not in processed)):
                    self.goto(i, conf.rule.right[conf.pnt_pos])
                    processed.add(conf.rule.right[conf.pnt_pos])
            i += 1
        self.table = [{} for _ in range(len(self.nodes))]
        self.fill_table(0, set())

    def predict(self, word):
        word += const.END
        stack = [0]
        i = 0
        while i < len(word):
            alpha = word[i]
            stack_back = stack[-1]
            if alpha not in self.table[stack_back]:
                return False
            if isinstance(self.table[stack_back][alpha], Reduce):
                if self.table[stack_back][alpha].rule == Rule(const.S_, self._start_non_terminal):
                    if i == (len(word) - 1):
                        return True
                    return False
                if (len(self.table[stack_back][alpha].rule.right) * 2) >= len(stack):
                    return False
                next_stack_elem = self.table[stack_back][alpha].rule.left
                rule_len = len(self.table[stack_back][alpha].rule.right)
                stack = stack[:len(stack) - (rule_len * 2)]
                stack_back = stack[-1]
                stack.append(next_stack_elem)
                stack.append(self.table[stack_back][next_stack_elem].to)

            elif isinstance(self.table[stack_back][alpha], Shift):
                stack.append(alpha)
                stack.append(self.table[stack_back][alpha].to)
                i += 1
        return False

    def closure(self, node):
        change = True
        while change:
            new_node = copy(node)
            change = False
            for conf in node.confs:
                for left in self._rules.keys():
                    for right in self._rules[left]:
                        rule = Rule(left, right)
                        if ((len(conf.rule.right) <= conf.pnt_pos) or
                                (conf.rule.right[conf.pnt_pos] != rule.left)):
                            continue
                        for next_smb in self.first(conf.rule.right[conf.pnt_pos + 1:] +
                                                   conf.next_smb, set()):
                            if Configuration(rule, next_smb, 0) not in new_node.confs:
                                new_node.confs.add(Configuration(rule, next_smb, 0))
                                change = True
            node = new_node

        return node

    def goto(self, i, symbol):
        new_node = Node()
        for conf in self.nodes[i].confs:
            if ((len(conf.rule.right) > conf.pnt_pos) and
                    (conf.rule.right[conf.pnt_pos] == symbol)):
                new_node.confs.add(Configuration(conf.rule,
                                                 conf.next_smb,
                                                 conf.pnt_pos + 1))
        new_node = self.closure(new_node)
        if new_node not in self.start_node:
            self.nodes.append(new_node)
            self.start_node.add(new_node)
        if symbol in self.nodes[i].children:
            raise Exception('Not LR(1) grammar!')
        self.nodes[i].children[symbol] = self.nodes.index(new_node)

    def fill_table(self, i, used):
        if i in used:
            return
        for symbol in self.nodes[i].children:
            self.table[i][symbol] = Shift(self.nodes[i].children[symbol])
        for conf in self.nodes[i].confs:
            if len(conf.rule.right) == conf.pnt_pos:
                if conf.next_smb in self.table[i]:
                    raise Exception('Not LR(1) grammar!')
                self.table[i][conf.next_smb] = Reduce(conf.rule)
        used.add(i)
        for symbol in self.nodes[i].children:
            self.fill_table(self.nodes[i].children[symbol], used)

    def first(self, w, cur_opened):
        if w in cur_opened:
            return set()
        cur_opened.add(w)
        if len(w) == 0:
            return set()
        res = [w[0]]
        res_set = {w[0]}
        if w in self._terminals:
            return res_set
        change = True
        while change:
            change = False
            u_index = 0
            while u_index < len(res):
                alpha = res[u_index]
                if alpha in self._terminals:
                    break
                change = change or self.add_not_term_first(alpha, res, res_set)
                u_index += 1

        if '' in res_set:
            res_set.remove('')
            res_set.update(self.first(w[1:], cur_opened))
        return res_set

    def add_not_term_first(self, alpha, res, res_set):
        change = False
        for left in self._rules:
            right = self._rules[left]
            if left != alpha:
                continue
            if alpha in res_set:
                change = True
                res_set.discard(alpha)
            if ((alpha != right[:1]) and
                    (right[:1] not in res_set)):
                change = True
                res_set.add(right[:1])
                res.append(right[:1])
        return change

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
