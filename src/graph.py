from models import *
import networkx as nx
import uuid
import matplotlib.pyplot as plt
from typing import List
import random


class Graph:
    """Graph class"""

    def __init__(self):
        self.G = nx.Graph()

    def clear(self):
        """Removes all edges and nodes from graph"""
        self.G.clear()

    def valid_edge(self, node_1, node_2, key_tolerance: int = 1):
        """Decides if an edge can be created between two nodes

            Parameters:
                node_1: 1st node to compare
                node_2: 2nd node to compare

            Returns:
                True if the tracks are of compatible key (adjacent on Camelot wheel)

                False otherwise
        """
        return (node_1["camelot_note"] == node_2["camelot_note"]) or (abs(node_1["camelot_note"] -
                                                                          node_2["camelot_note"]) <= key_tolerance and node_1["camelot_m"] == node_2["camelot_m"])

    def remove_edges(self):
        """Removes all edges from graph"""
        self.G.remove_edges_from(list(self.G.edges()))

    def recalculate_edges(self, bpm_tolerance: int = 1, key_tolerance: int = 1):
        """Creates edges in the graph. Use when first creating graph, and when nodes to add > nodes in graph

            Parameters:
                bpm_tolerance (int): Max BPM difference between tracks that allows an edge to be formed          
        """
        self.remove_edges()
        nodes = list(self.G.nodes(data=True))
        for idx, node in enumerate(nodes):
            for comp in nodes[idx+1:]:
                bpm_diff = abs(node[1]["bpm"]-comp[1]["bpm"])
                if self.valid_edge(node[1], comp[1], key_tolerance) and bpm_diff <= bpm_tolerance:
                    self.G.add_edge(node[0], comp[0], weight=bpm_diff)

    def add_edges(self, nodes: List[TrackNode], bpm_tolerance: int = 1, key_tolerance: int = 1):
        """Adds edges for the nodes provided.  Use when nodes to add < nodes in graph

                Parameters:
                    nodes (list of TrackNodes): List of nodes to add edges for
                    bpm_tolerance (int): Max BPM difference between tracks that allows an edge to be formed
        """
        graph_nodes = list(self.G.nodes(data=True))
        for node in nodes:
            dict_node = node.__dict__
            for graph_node in graph_nodes:
                bpm_diff = abs(dict_node["bpm"]-graph_node[1]["bpm"])
                if self.valid_edge(dict_node, graph_node[1], key_tolerance) and bpm_diff <= bpm_tolerance:
                    if dict_node["uuid"] != graph_node[0]:
                        self.G.add_edge(
                            dict_node["uuid"], graph_node[0], weight=bpm_diff)

    def add_nodes(self, nodes: List[TrackNode]):
        """Adds new nodes to the graph.

            Parameters:
                nodes (list of TrackNodes): Nodes to create in graph

            Returns:
                ids (list of TrackNodes): Nodes updated with ids
        """
        id_nodes = []
        for node in nodes:
            id = str(uuid.uuid4())
            node.add_uuid(id)
            dict_node = node.__dict__
            self.G.add_node(id, **dict_node)
            id_nodes.append(node)
        return id_nodes

    def get_random_node(self):
        """Returns a random node from the graph"""
        return random.choice((list(self.G.nodes(data=True))))

    def shortest_weighted_path(self, source, target):
        """Finds the shortest path minimising BPM changes between two nodes, using the Dijkstra algorithm

            Parameters:
                source: Source node in path
                target: Target node in path

            Returns:
                path: List of nodes in the path
        """
        return nx.algorithms.bidirectional_dijkstra(self.G, source, target)

    def shortest_path(self, source, target):
        """Finds the shortest path between two nodes

            Parameters:
                source: Source node in path
                target: Target node in path

            Returns:
                path: List of nodes in the path
        """
        return nx.algorithms.bidirectional_shortest_path(self.G, source, target)

    def get_node_info(self, node):
        """Returns the Track information of a node

            Parameters:
                node: Target node to retrieve information from

            Returns:
                info: Dict representation of TrackNode that corresponds to the provided node
        """
        return self.G.nodes[node]

    def get_path_info(self, nodes):
        """Returns the Track information of all nodes in a path

            Parameters:
                nodes: List of nodes in path

            Returns:
                info: List of dict representations of TrackNodes that corresponds to the provided nodes
        """
        return [self.get_node_info(x) for x in nodes]

    def title_uuid_dict(self):
        """Returns a dict of {title:uuid} for all nodes in graph"""
        return {x[1]["title"]: x[0] for x in self.G.nodes(data=True)}

    def plot(self):
        """Plots a visual representation of the graph"""
        # elarge = [(u, v)
        #           for (u, v, d) in self.G.edges(data=True) if d["weight"] >= 1]
        esmall = [(u, v)
                  for (u, v, d) in self.G.edges(data=True)]
        pos = nx.spring_layout(self.G, seed=7)
        nx.draw_networkx_nodes(self.G, pos, node_size=1500)
        # nx.draw_networkx_edges(self.G, pos, edgelist=elarge, width=6)
        nx.draw_networkx_edges(self.G, pos, edgelist=esmall, width=1,
                               alpha=0.5, edge_color="b", style="dashed")

        # node labels
        node_labels = nx.get_node_attributes(self.G, "title")
        nx.draw_networkx_labels(self.G, pos, node_labels,
                                font_size=8, font_family="sans-serif")
        # edge weight labels
        # edge_labels = nx.get_edge_attributes(self.G, "weight")
        # nx.draw_networkx_edge_labels(self.G, pos, edge_labels)

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

    def to_json(self):
        """Converts the graph to a JSON format"""
        return nx.node_link_data(self.G)
