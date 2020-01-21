import networkx as nx
import matplotlib.pyplot as plt
from networkx_viewer import Viewer
from pyvis import network as net

def plot_graph(G):
    plt.figure(figsize=(20,8))
    edge_labels = nx.get_edge_attributes(G,'depth')
    # pos = nx.spring_layout(G) # circularspring_layout, scale=1., center=None
    pos = nx.nx_agraph.graphviz_layout(G)
    nx.draw_networkx_edge_labels(G,pos, edge_labels = edge_labels, font_size=10, font_color='k')
    nx.draw_networkx(G, pos,with_labels=True,
                    cmap=plt.cm.seismic, font_size =10, arrows = True) # 
    plt.axis('off')
    # plt.tight_layout()
    # plt.show()

def draw_graph3(networkx_graph,notebook=False,output_filename='graph.html',show_buttons=True,only_physics_buttons=False):
    """
    This function accepts a networkx graph object,
    converts it to a pyvis network object preserving its node and edge attributes,
    and both returns and saves a dynamic network visualization.
    
    Valid node attributes include:
        "size", "value", "title", "x", "y", "label", "color".
        
        (For more info: https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_node)
        
    Valid edge attributes include:
        "arrowStrikethrough", "hidden", "physics", "title", "value", "width"
        
        (For more info: https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_edge)
        
    
    Args:
        networkx_graph: The graph to convert and display
        notebook: Display in Jupyter?
        output_filename: Where to save the converted network
        show_buttons: Show buttons in saved version of network?
        only_physics_buttons: Show only buttons controlling physics of network?
    """
    
    # make a pyvis network
    pyvis_graph = net.Network(notebook=notebook,directed=True, width="100%", height="100%")
    
    # for each node and its attributes in the networkx graph
    for node,node_attrs in networkx_graph.nodes(data=True):
        node_attrs['title'] = node
        pyvis_graph.add_node(node,**node_attrs)
        
    # for each edge and its attributes in the networkx graph
    for source,target,edge_attrs in networkx_graph.edges(data=True):
        title = ""
        data = pyvis_graph.get_edges()
        print("source {}, target {}, edge_attrs {}".format(source, target, edge_attrs))
        # if value/width not specified directly, and weight is specified, set 'value' to 'weight'
        if not 'value' in edge_attrs and not 'width' in edge_attrs and 'depth' in edge_attrs:
            # place at key 'value' the weight of the edge
            # edge_attrs['title']= "From {} to {} {}".format(source, target, edge_attrs['depth'])
            title = "From {} to {} {}".format(source, target, edge_attrs['depth'])
        # add the edge
        for d in data:
            if d['from'] == target and d['to'] == source:
                # Found a direction thingy
                title += "<br>" + d['title']
                break
        edge_attrs['title']= title
        pyvis_graph.add_edge(source,target,**edge_attrs)
    
        
    # turn buttons on

    # if show_buttons:
    #     if only_physics_buttons:
    #         pyvis_graph.show_buttons(filter_=['physics'])
    #     else:
    #         pyvis_graph.show_buttons()

    options = """
        var options = {
            "nodes": {
                "physics": false,
                "size": 12
            },
            "edges": {
                "arrowStrikethrough": false,
                "color": {
                    "inherit": true
                },
                "physics": false,
                "smooth": false
            },
            "physics": {
                "minVelocity": 0.75
            }
        }
        """
    pyvis_graph.set_options(options)
    # return and also save
    return pyvis_graph.show(output_filename)