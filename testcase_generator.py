import os
import time
import random
import inquirer
import subprocess
import numpy as np
from random_word import RandomWords

class IOFile:
    def __init__(self, file_name, input_data, limit_time=1000):
        self.file_name = file_name
        self.input_data = input_data
        self.limit_time = limit_time

    @staticmethod
    def make_binary(path):
        os.system(f"g++ -std=c++17 {path}.cpp -o {path}")

    def run_binary_with_input(self):
        start_time = time.time()
        process = subprocess.Popen(self.file_name, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate(self.input_data)

        if stderr:
            print(f"Error: {stderr}")
            exit()

        time_complexity = time.time() - start_time

        if time_complexity > self.limit_time:
            print(f"Time complexity exceeded: {time_complexity} > {self.limit_time}")
        
        print("Time complexity: ", time_complexity)

        return stdout

    @staticmethod
    def make_io_file(dir_name, input_data, output_data, file_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        open(f"{dir_name}/{file_name}.in", "w").write(input_data)
        open(f"{dir_name}/{file_name}.out", "w").write(output_data)


class TestcaseGenerator:
    def __init__(self):
        pass

    @staticmethod
    def join_input(args, is_inline=False):
        if is_inline:
            return " ".join(args)
        return "\n".join(args)

    def random_number(self, n, start_number=1, end_number=100, is_inline=False):
        testcase = [str(random.randint(start_number, end_number)) for _ in range(n)]
        return self.join_input(testcase, is_inline=is_inline)
        
    def random_string(self, n, is_inline=False):
        r = RandomWords()
        testcase = [r.get_random_word() for _ in range(n)]
        return self.join_input(testcase, is_inline=is_inline)

    def random_pair(self, n, range_number=100):
        testcase = [f"{random.randint(1, range_number)} {random.randint(1, range_number)}" for _ in range(n)]
        return self.join_input(testcase)
    
    def random_cube(self, row, col, range_number=100):
        testcase = [[random.randint(1, range_number) for _ in range(col)] for _ in range(row)]
        return self.join_input([" ".join(map(str, i)) for i in testcase])


questions = [
    inquirer.Text('n', message="Enter number of testcase", validate=lambda _, x: x.isdigit(),),
]

answers = inquirer.prompt(questions)
n = int(answers['n'])

testcaseObj = TestcaseGenerator()

idx = 0
accepted_testcase = 0
while idx < n:
    # {testcaseObj.random_number(n=10,range_number=1000000,is_inline=True)}
    # {testcaseObj.random_string(n=10,is_inline=True)}
    # {testcaseObj.random_pair(n=10,range_number=1000000)}

    _n = np.linspace(1, 1e4, n, dtype=int)[idx]
    _target = random.randint(1, 100)

    input_data = f"""
{_n}
{testcaseObj.random_number(n=_n, start_number=0, end_number=1e4, is_inline=True)}
    """.strip()

    file_name = "./longestMoutain"
    limit_time = 0.5

    iOFileObj = IOFile(file_name, input_data, limit_time)

    iOFileObj.make_binary(file_name)
    output_data = iOFileObj.run_binary_with_input()

#     not_except_case = """
# -1 -1
# """.strip()
#     if output_data.strip() in not_except_case:
#         accepted_testcase += 1
#         if accepted_testcase > 5:
#             continue

#         print("Accepted testcase: ", accepted_testcase)

    iOFileObj.make_io_file(f'{file_name}_dir', input_data, output_data, f"{idx+1}")
    idx += 1
