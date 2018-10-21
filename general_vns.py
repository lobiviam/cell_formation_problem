import random
from solution import Solution
from solution import Cluster
from copy import deepcopy


class GeneralVNS:
    def __init__(self, data_matrix, machines_num, details_num):
        self.data_matrix = data_matrix
        self.machines_number = machines_num
        self.details_number = details_num
        self.solution = self.vns()

    def getInitialSolution(self):
        rand_machines = random.sample(range(1, self.machines_number), 10)
        rand_details = random.sample(range(1, self.details_number), 10)
        cluster_1 = Cluster(rand_machines, rand_details, self.data_matrix)
        other_machines = set(list(range(1, self.machines_number + 1))) - set(rand_machines)
        other_details = set(list(range(1, self.details_number + 1))) - set(rand_details)
        cluster_2 = Cluster(other_machines, other_details, self.data_matrix)
        init_solution = Solution([cluster_1, cluster_2], self.data_matrix)
        return init_solution

    def shaking(self, solution):
        if len(solution.clusters) == 1:
            new_solution = self.divide(solution)
        else:
            merge_or_divide = random.randint(0, 1)
            if merge_or_divide == 0:
                new_solution = self.divide(solution)
            else:
                new_solution = self.merge(solution)
        return new_solution

    def vns(self):
        initial_solution = self.getInitialSolution()
        init_obj_func = initial_solution.objectiveFunctionValue
        curr_solution = self.divide(initial_solution)

        for i in range(50):
            shaking_result = self.shaking(curr_solution)
            new_solution = self.local_serch(shaking_result)
            if new_solution.objectiveFunctionValue > curr_solution.objectiveFunctionValue:
                curr_solution = new_solution
        return curr_solution

        return shaking_result

    def local_serch(self, solution):
        solution_after_relocate_machine = self.relocate_machine(solution)
        if solution_after_relocate_machine.objectiveFunctionValue > solution.objectiveFunctionValue:
            return self.local_serch(solution_after_relocate_machine)
        else:
            solution_after_relocate_detail = self.relocate_detail(solution)
            if solution_after_relocate_detail.objectiveFunctionValue > solution.objectiveFunctionValue:
                return self.local_serch(solution_after_relocate_detail)
        return solution

    def divide(self, solution):
        cluster_to_divide_id = random.randint(0, len(solution.clusters) - 1)
        cluster_to_divide = solution.clusters[cluster_to_divide_id]
        if len(cluster_to_divide.machines) == 1 or len(cluster_to_divide.details) == 1:
            return solution

        machine_id_to_divide = random.randint(1, len(cluster_to_divide.machines) - 1)
        detail_id_to_divide = random.randint(1, len(cluster_to_divide.details) - 1)
        machines_subcluster_first = set(list(cluster_to_divide.machines)[:machine_id_to_divide])
        details_subcluster_first = set(list(cluster_to_divide.details)[:detail_id_to_divide])
        first_new_cluster = Cluster(machines_subcluster_first, details_subcluster_first, self.data_matrix)
        machines_subcluster_second = cluster_to_divide.machines - machines_subcluster_first
        details_subcluster_second = cluster_to_divide.details - details_subcluster_first
        second_new_cluster = Cluster(machines_subcluster_second, details_subcluster_second, self.data_matrix)

        new_cluster_list = deepcopy(solution.clusters)
        new_cluster_list.pop(cluster_to_divide_id)
        new_cluster_list.extend([first_new_cluster, second_new_cluster])
        new_solution = Solution(new_cluster_list, self.data_matrix)
        return new_solution

    def merge(self, solution):
        clusters_to_merge = random.sample(range(len(solution.clusters)), 2)
        new_machines_subcluster = list(solution.clusters[clusters_to_merge[0]].machines) + list(
            solution.clusters[clusters_to_merge[1]].machines)
        new_details_subcluster = list(solution.clusters[clusters_to_merge[0]].details) + list(solution.clusters[
                                                                                                  clusters_to_merge[
                                                                                                      1]].details)
        newCluster = Cluster(new_machines_subcluster, new_details_subcluster, self.data_matrix)
        new_clusters_list = deepcopy(solution.clusters)
        if clusters_to_merge[0] < clusters_to_merge[1]:
            new_clusters_list.pop(clusters_to_merge[1])
            new_clusters_list.pop(clusters_to_merge[0])
            new_clusters_list.append(newCluster)
        else:
            new_clusters_list.pop(clusters_to_merge[0])
            new_clusters_list.pop(clusters_to_merge[1])
            new_clusters_list.append(newCluster)
        newSolution = Solution(new_clusters_list, self.data_matrix)
        return newSolution

    def relocate_machine(self, solution):
        clusters_list = deepcopy(solution.clusters)
        clusters_pairs = []
        for i in range(len(clusters_list)):
            for j in range(len(clusters_list)):
                if i != j:
                    clusters_pairs.append([i, j])
        solutions_list = [solution]
        for pair in clusters_pairs:
            cluster_id_1 = pair[0]
            cluster_id_2 = pair[1]
            solutions_list.extend(self.relocate_machine_helper(deepcopy(clusters_list), cluster_id_1, cluster_id_2))
        return max(solutions_list, key=lambda x: x.objectiveFunctionValue)

    def relocate_machine_helper(self, clusters_list, cluster_id_from, cluster_id_to):
        inner_cluster_list = deepcopy(clusters_list)
        if cluster_id_to > cluster_id_from:
            cluster_to = inner_cluster_list.pop(cluster_id_to)
            cluster_from = inner_cluster_list.pop(cluster_id_from)
        else:
            cluster_from = inner_cluster_list.pop(cluster_id_from)
            cluster_to = inner_cluster_list.pop(cluster_id_to)
        solutions_list = []
        if len(cluster_from.machines) == 1:
            return solutions_list

        for machine_to_relocate in cluster_from.machines:
            buff_clusters_list = deepcopy(inner_cluster_list)
            new_cluster_from = Cluster((cluster_from.machines - {machine_to_relocate}), cluster_from.details,
                                       self.data_matrix)
            new_cluster_to = Cluster((cluster_to.machines | {machine_to_relocate}), cluster_to.details,
                                     self.data_matrix)
            buff_clusters_list.append(new_cluster_from)
            buff_clusters_list.append(new_cluster_to)
            new_solution = Solution(buff_clusters_list, self.data_matrix)
            solutions_list.append(new_solution)
        return solutions_list

    def relocate_detail(self, solution):
        clusters_list = deepcopy(solution.clusters)
        clusters_pairs = []
        for i in range(len(clusters_list)):
            for j in range(len(clusters_list)):
                if i != j:
                    clusters_pairs.append([i, j])
        solutions_list = [solution]
        for pair in clusters_pairs:
            cluster_id_1 = pair[0]
            cluster_id_2 = pair[1]
            solutions_list.extend(self.relocate_detail_helper(deepcopy(clusters_list), cluster_id_1, cluster_id_2))
        return max(solutions_list, key=lambda x: x.objectiveFunctionValue)

    def relocate_detail_helper(self, clusters_list, cluster_id_from, cluster_id_to):
        inner_cluster_list = deepcopy(clusters_list)
        if cluster_id_to > cluster_id_from:
            cluster_to = inner_cluster_list.pop(cluster_id_to)
            cluster_from = inner_cluster_list.pop(cluster_id_from)
        else:
            cluster_from = inner_cluster_list.pop(cluster_id_from)
            cluster_to = inner_cluster_list.pop(cluster_id_to)

        solutions_list = []
        if len(cluster_from.details) == 1:
            return solutions_list
        for detail_to_relocate in cluster_from.details:
            buff_clusters_list = deepcopy(inner_cluster_list)
            new_cluster_from = Cluster(cluster_from.machines, cluster_from.details - {detail_to_relocate},
                                       self.data_matrix)
            new_cluster_to = Cluster(cluster_to.machines, cluster_to.details | {detail_to_relocate}, self.data_matrix)
            buff_clusters_list.append(new_cluster_from)
            buff_clusters_list.append(new_cluster_to)
            new_solution = Solution(buff_clusters_list, self.data_matrix)
            solutions_list.append(new_solution)
        return solutions_list
