import issue
import solution
import general_vns


def print_solution_if_file(file_name, solution, machines_number, details_niumber):
    with open(file_name + '.sol', 'w') as out_file:
        cluster_id = 0
        machine_result_dict = dict()
        details_result_dict = dict()
        for cluster in solution.clusters:
            cluster_id += 1
            for machine in cluster.machines:
                machine_result_dict[machine] = cluster_id
            for detail in cluster.details:
                details_result_dict[detail] = cluster_id
        for i in range(1, machines_number + 1):
            out_file.write(str('m') + str(i) + '_' + str(machine_result_dict[i]) + ' ')
        out_file.write('\n')
        for i in range(1, details_number + 1):
            out_file.write(str('p') + str(i) + '_' + str(details_result_dict[i]) + ' ')


if __name__ == '__main__':
    file_name = '24x40'
    _issue = issue.Issue(file_name + '.txt')
    data_dict = _issue.data_dict
    machines_number = _issue.machines_number
    details_number = _issue.details_number
    solver = general_vns.GeneralVNS(_issue.data_matrix, _issue.machines_number, _issue.details_number)
    solution = solver.solution
    print_solution_if_file(file_name, solution, machines_number, details_number)

