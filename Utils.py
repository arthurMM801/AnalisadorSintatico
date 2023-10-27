def read_program_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            program_text = file.read()
        return program_text
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
