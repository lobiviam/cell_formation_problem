class Solution:
    def __init__(self, clusters_list, data_matrix):
        self.clusters = clusters_list
        self.data_matrix = data_matrix
        self.total_number_of_ones = self.get_total_number_of_ones()
        self.objectiveFunctionValue = self.get_obj_func_value()
        self.numberOfClusters = len(clusters_list)
        self.is_feasible = self.is_feasible_solution()
        assert self.is_feasible
        self.clusterDict = dict()

    def get_obj_func_value(self):
        ones_in_clusters = 0
        zeros_in_clusters = 0
        for cluster in self.clusters:
            ones_in_clusters += cluster.ones_number
            zeros_in_clusters += cluster.zeros_number
        return ones_in_clusters / (self.total_number_of_ones + zeros_in_clusters)

    def get_total_number_of_ones(self):
        return self.data_matrix.sum()

    def is_feasible_solution(self):
        #  each cluster must contain at least 1 machine and 1 detail
        for cluster in self.clusters:
            if len(cluster.machines) > 0 and len(cluster.details) > 0:
                pass
            else:
                return False
        #  each machine must be assigned to exactly 1 cluster
        for cluster_1 in self.clusters:
            for cluster_2 in self.clusters:
                if cluster_1 != cluster_2:
                    if len(set(cluster_1.machines) & set(cluster_2.machines)) > 0:
                        return False
        #  each detail must be assigned to exactly 1 cluster
        for cluster_1 in self.clusters:
            for cluster_2 in self.clusters:
                if cluster_1 != cluster_2:
                    if len(set(cluster_1.details) & set(cluster_2.details)) > 0:
                        return False
        return True



class Cluster:
    def __init__(self, machines, details, data_matrix):
        self.machines = set(machines)
        self.details = set(details)
        self.data_matrix = data_matrix
        self.ones_number, self.zeros_number = self.get_number_of_ones_and_zeroes()

    def get_number_of_ones_and_zeroes(self):
        number_of_cells = len(self.machines) * len(self.details)
        number_of_ones = 0
        for machine in self.machines:
            for detail in self.details:
                number_of_ones += self.data_matrix[machine - 1, detail - 1]
        return number_of_ones, number_of_cells - number_of_ones
