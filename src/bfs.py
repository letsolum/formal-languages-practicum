from src.grammar import Grammar
import src.constants as const

class StupidAlgorithm(Grammar):
    def __init__(self, G: Grammar):
        super().__init__(other=G)

    def __get_real_string(self, now: str) -> str:
        cur = now
        for symbol in now:
            if symbol in self._rules and '' in self._rules[symbol]:
                cur = cur.replace(symbol, '')
        return cur

    def __minimal_len(self, now: str):
        cur = now
        for symbol in now:
            if symbol in self._rules:
                mi = self._rules[symbol][0]
                for rhs in self._rules[symbol]:
                    if len(rhs) < len(mi):
                        mi = rhs
                cur = cur.replace(symbol, mi)
        return len(cur)

    def predict(self, word: str) -> bool:
        queue = [self._start_non_terminal]
        used = {queue[0]}
        cnt = 0
        while len(queue) != 0:
            cnt += 1
            if cnt > const.STOP_STUPID:
                return False
            now = queue[0]
            queue.pop(0)
            now_without_non_term = self.__get_real_string(now)
            if now_without_non_term == word:
                return True
            if self.__minimal_len(now) > len(word) or len(now) > 5 * len(word):
                continue
            for i in range(len(now)):
                if now[i] not in self._rules:
                    continue
                for rhs in self._rules[now[i]]:
                    cur = now[:i] + rhs + now[i + 1:]
                    if cur in used:
                        continue
                    used.add(cur)
                    queue.append(cur)
        return False
