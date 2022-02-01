
def map_node_to_property(nodes, index):
    for i in range(len(nodes)):
        if nodes[i]['key'] == index:
            return nodes[i]['type'], nodes[i]['code']

def build_tree(edges, original_nodes):

    v = []
    for i in range(len(edges)):
        if edges[i]['type'] == 'IS_AST_PARENT':
            v.append((edges[i]['end'], edges[i]['start']))

    n = len(edges)
    i = 0

    forest = []
    nodes = {}

    id = 'id'
    children = 'children'
    node_type = 'type'
    code = 'code'
    has_child = 'has_child'

    for node_id, parent_id in v:
        # create current node if necessary
        if not node_id in nodes:
            t, c = map_node_to_property(original_nodes, node_id)
            node = {id: node_id, node_type: t, code: c, has_child: False}
            nodes[node_id] = node
        else:
            node = nodes[node_id]

        if node_id == parent_id:
            # add node to forrest
            forest.append(node)
        else:
            # create parent node if necessary
            if not parent_id in nodes:
                t, c = map_node_to_property(original_nodes, parent_id)
                parent = {id: parent_id, node_type: t,
                          code: c, has_child: False}
                nodes[parent_id] = parent
            else:
                parent = nodes[parent_id]
            # create children if necessary
            if not children in parent:
                parent[children] = []
            # add node to children of parent
            parent[children].append(node)
            parent[has_child] = True

    return parent, forest