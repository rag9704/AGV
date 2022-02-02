import numpy as np
import time




def Q_dict(Q):

    keys = []
    QDist_list = []

    for i in range(len(Q[0])):
        for j in range(len(Q[0])):
            if Q[i][j] != 0:
                keys.append((i,j))
                QDist_list.append(Q[i][j])

    Qdict = {keys[i]: QDist_list[i] for i in range(len(keys))}

    return Qdict




def selection_rules(qb_solution, r):
    """takes the solution of QBSolve in dict form returns the selection rules telling which car takes which route"""

    one_solution_list = []
    solutions_list = []

    for i in range(len(qb_solution)):
        for j in range(len(qb_solution[i])):
            one_solution_list.append(qb_solution[i][j])
        solutions_list.append(one_solution_list)
        one_solution_list = []

    selections = []

    sliced_list_temp = []

    for i in range(len(solutions_list)):

        for j in range(0, len(solutions_list[i]), r):
            # sliced_list_temp.append([solutions_list[i][j]] + [solutions_list[i][j + 1]] + [solutions_list[i][j + 2]])

            big = []
            for k in range(r):
                big = big + [solutions_list[i][j+k]]

            sliced_list_temp.append(big)


        selections.append(sliced_list_temp)

        sliced_list_temp = []

    # print("sliced list: ", selection_rules)
    # print("sliced list len: ", len(selection_rules))

    return selections


def routes_from_selection_rule(root, selection_rules):
    """"This function takes the sliced list, aka selection rules for each car's routes,
    and then uses routes_pickle to find out the actual routes being proposed by looking at the selection rules."""

    all_roots_of_one_solution = []
    all_roots_of_all_solutions = []

    for number_of_solutions in range(len(selection_rules)):
        for i in range(0, len(selection_rules[number_of_solutions])):
            for j in range(0, len(selection_rules[number_of_solutions][i])):

                if (selection_rules[number_of_solutions][i][j]):
                    all_roots_of_one_solution.append(root[i][j])

        all_roots_of_all_solutions.append(all_roots_of_one_solution)
        all_roots_of_one_solution = []

    # length = 1

    count_list = []
    count = 0
    for i in range(len(all_roots_of_all_solutions)):
        for j in range(len(all_roots_of_all_solutions[i])):
            # for k in all_roots_of_all_solutions[i][j]:
            #     print("k: ", k)
            count = count+len(all_roots_of_all_solutions[i][j])
        count_list.append(count)
        count = 0

    argmin_count = np.argmin(count_list)

    return (all_roots_of_all_solutions[argmin_count])


def best_nodes(best_routes, sn_dict):
    """This function takes the best_routes in segments form and gives us the corresponding nodes"""

    nodes = []
    for i in range(len(best_routes)):
        small = []

        for j in best_routes[i]:
            # print("uh: ",inv_dict[j])
            small.append(sn_dict[j])

        nodes.append(small)

    return nodes


def best_routes(best_routes_nodes,sn_dict,source):    #routes
    nodes = []
    for i in range(len(best_routes_nodes)):
        small=[]
        small.append(source[i])
        for j in best_routes_nodes[i]:
            d=[i for i in sn_dict[j] if i not in small]
            small.append(d[0])
        nodes.append(small)
    return nodes
    



