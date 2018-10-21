import re
import numpy as np


class Issue:
    def __init__(self, file_name):
        file = open('./cfp_data/' + file_name)
        self.data = file.read().split('\n')
        self.machines_number = int(re.findall('[0-9]+', self.data[0])[0])
        self.details_number = int(re.findall('[0-9]+', self.data[0])[1])
        self.data_dict = self.get_data_dict()
        self.data_matrix = self.get_matrix()

    def get_data_dict(self):
        data_dict = dict()
        for i in range(1, len(self.data)):
            machine_details_data = re.findall('[0-9]+', self.data[i])
            machine_id = int(machine_details_data[0])
            details_list = [int(i) for i in machine_details_data[1:]]
            data_dict[machine_id] = details_list
        return data_dict

    def get_matrix(self):
        matrix = np.zeros([self.machines_number, self.details_number],dtype=np.int)
        for key, values in self.data_dict.items():
            for value in values:
                matrix[key - 1, value - 1] = 1
        return matrix
