import math
from Pyro4 import expose


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        array_numbers = self.read_input()
        step = len(array_numbers) / len(self.workers)
        added_amount = 0
        workers_amount = len(self.workers)

        mapped = []
        for i in range(0, len(self.workers)):
            added_amount += step
            mapped.append(self.workers[i].mymap(array_numbers[i * step: i * step + step]))

        if added_amount != len(array_numbers):
            mapped.append(self.workers[workers_amount-1].mymap(array_numbers[len(array_numbers)-1:]))

        reduced = self.myreduce(mapped)
        self.write_output(reduced)

    @staticmethod
    @expose
    def mymap(arr):
        result = []
        for number in arr:
            reversed = 0
            while(number!=0):
                r=int(number%10)
                reversed = reversed*10 + r
                number=int(number/10)
                
            result.append(reversed)
        return result

    @staticmethod
    @expose
    def myreduce(mapped):
        to_return = []
        for num in mapped:
            to_return.append(num.value)
        return to_return

    def read_input(self):
        f = open(self.input_file_name, 'r')
        array = []
        for line in f:
            array.append(int(line))
        f.close()
        return array

    def write_output(self, output):
        f = open(self.output_file_name, 'a')
        f.write(str(sum(output, [])))
        f.write('\n')
        f.close()

        f.close()