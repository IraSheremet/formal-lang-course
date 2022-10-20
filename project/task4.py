from scipy.sparse import block_diag, vstack

from project.task3 import *


def rpq(
    graph: MultiDiGraph,
    regex,
    mtx_type_matrix=lil_matrix,
    start_states: Set[int] = None,
    final_states: Set[int] = None,
    is_for_each_node: bool = False,
) -> Set:
    """Perform a regular query to the graph using multiple source bfs.

    Parameters
    ----------
    graph: MultiDiGraph
    regex
    start_states: Set[int]
    final_states: Set[int]
    is_for_each_node: bool
    mtx_type_matrix

    Returns
    -------
     reachable_nodes: Set[Union[tuple[State, State], State]]
    """
    graph_bool_decomposition = BoolDecomposition(
        create_nfa_for_graph(graph, start_states, final_states),
        mtx_type_for_construction=mtx_type_matrix,
    )
    regex_bool_decomposition = BoolDecomposition(
        create_minimal_dfa_for_regex(regex), mtx_type_for_construction=mtx_type_matrix
    )
    return sync_bfs(
        graph_bool_decomposition, regex_bool_decomposition, is_for_each_node
    )


def sync_bfs(
    graph: BoolDecomposition, regex: BoolDecomposition, is_for_each_node: bool = False
) -> Set:
    """Executes sync bfs on the automatons represented by bool matrices.

    Parameters
    ----------
    graph: BoolDecomposition
    regex: BoolDecomposition
    is_for_each_node: bool

    Returns
    -------
     reachable_nodes: Set[Union[tuple[State, State], State]]
    """

    def transform_rows(step1, regex_states1, is_for_each_node1):
        result = graph.mtx_type_for_construction(step.shape, dtype=bool)
        for row1, col1 in zip(*step1.nonzero()):
            if col1 < regex_states1:
                right_row_part = step1[row1, regex_states1:]
                if right_row_part.nnz != 0:
                    if not is_for_each_node1:
                        result[col1, col1] = True
                        result[col1, regex_states1:] += right_row_part
                    else:
                        node_number = row1 // regex_states1
                        result[node_number * regex_states1 + col1, col1] = True
                        result[
                            node_number * regex_states1 + col1, regex_states1:
                        ] += right_row_part
        return result

    direct_sum = {}
    for label in graph.bool_matrix.keys() & regex.bool_matrix.keys():
        direct_sum[label] = block_diag(
            (regex.bool_matrix[label], graph.bool_matrix[label])
        )
    front = (
        vstack([create_front(graph, regex, {st}) for st in graph.start_states])
        if is_for_each_node
        else create_front(graph, regex, graph.start_states)
    )

    visited = graph.mtx_type_for_construction(front.shape, dtype=bool)
    is_first_step = True
    while True:
        old_visited_nnz = visited.nnz
        for mtx in direct_sum.values():
            step = front @ mtx if is_first_step else visited @ mtx
            visited += transform_rows(step, regex.all_states, is_for_each_node)
        is_first_step = False
        if old_visited_nnz == visited.nnz:
            break

    reachable_nodes = set()
    regex_states = list(regex.state_to_index.keys())
    graph_states = list(graph.state_to_index.keys())
    for row, col in zip(*visited.nonzero()):
        if (
            not col < regex.all_states
            and regex_states[row % regex.all_states] in regex.final_states
        ):
            state_index = col - regex.all_states
            if graph_states[state_index] in graph.final_states:
                if is_for_each_node:
                    reachable_nodes.add(
                        (State(row // regex.all_states), State(state_index))
                    )
                else:
                    reachable_nodes.add(State(state_index))
    return reachable_nodes


def create_front(graph: BoolDecomposition, regex: BoolDecomposition, start_states):
    front = graph.mtx_type_for_construction(
        (regex.all_states, regex.all_states + graph.all_states), dtype=bool
    )

    for st in regex.start_states:
        i = regex.state_to_index[State(st)]
        front[i, i] = True
        for graph_st in start_states:
            front[i, regex.all_states + graph_st.value] = True
    return front
