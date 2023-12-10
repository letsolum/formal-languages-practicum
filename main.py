from src.earley import Earley

if __name__ == '__main__':
    algo_name = input("Chose algorithm, which you want to use [Earley (default), LR(1)]: ")
    input_file = input("Input name of file for input or press ENTER: ")
    output_file = input("Input name of file for output or press ENTER: ")
    algorithm = None
    if algo_name == 'LR1':
        pass  # TODO: change algorithm to LR(1), when it appears
    else:
        algorithm = Earley(input_file, output_file)
    algorithm.test()
