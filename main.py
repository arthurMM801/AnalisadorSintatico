from Utils import read_program_from_file
from Compilador import Compile

def main():
    file_path = "Programa.txt"

    input_program = read_program_from_file(file_path)
    if input_program:
        Compile(input_program)


if __name__ == '__main__':
    main()



