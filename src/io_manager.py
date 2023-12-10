class Input:
    def __init__(self, file_mode=False, file_name='input.txt', test_mode=None, given_strings=None):
        self.__file_mode = False
        self.__test_mode = False
        if test_mode:
            self.__test_mode = True
            self.__lines = given_strings
        else:
            self.__file_mode = file_mode
            if self.__file_mode:
                with open(file_name, 'r') as f:
                    self.__lines = f.read().splitlines()
        self.__prev_line_in_file = -1

    def get_line(self) -> str:
        line = ''
        if self.__test_mode or self.__file_mode:
            self.__prev_line_in_file += 1
            return self.__lines[self.__prev_line_in_file]
        else:
            line = input()
        return line

class Output:
    def __init__(self, file_mode=False, file_name='output.txt', test_mode=None):
        self.__file_mode = False
        self.__test_mode = False
        if test_mode:
            self.__test_mode = True
        else:
            self.__file_mode = file_mode
            self.__file_name = file_name
    
    def output_line(self, line: str):
        if self.__file_mode:
            with open(self.__file_name, 'a') as f:
                f.write(line + '\n')
        elif self.__test_mode:
            return line
        else:
            print(line)
