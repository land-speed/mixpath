import pytest
from graph import Graph
from models import TrackNode, Key


test_nodes = [TrackNode("source", 120, Key("G#min")), TrackNode("small_diff", 121, Key("Bmaj")), TrackNode(
    "tempo_diff", 124, Key("D#min")), TrackNode("key_diff", 121, Key("A#min")), TrackNode("big_diff", 130, Key("Emin"))]

test_additional_nodes = [TrackNode(
    "source-copy", 120, Key("G#min")), TrackNode("small_diff-copy", 121, Key("Bmaj"))]


class TestAddNodes:
    test_graph = Graph()

    def test_add_nodes(self):
        self.test_graph.add_nodes(test_nodes)

        assert self.test_graph.G.number_of_nodes() == len(test_nodes)


class TestValidEdge:
    test_graph = Graph()

    def test_is_valid(self):
        assert self.test_graph.valid_edge(
            test_nodes[0].__dict__, test_nodes[1].__dict__) == True

    def test_key_tolerance(self):
        assert self.test_graph.valid_edge(
            test_nodes[0].__dict__, test_nodes[3].__dict__) == False
        assert self.test_graph.valid_edge(
            test_nodes[0].__dict__, test_nodes[3].__dict__, key_tolerance=2) == True


class TestRecalculateEdges:

    def test_recalculate_edges(self):
        test_graph = Graph()
        nodes = test_graph.add_nodes(test_nodes)
        test_graph.recalculate_edges()

        assert test_graph.G.number_of_edges() == 1
        assert test_graph.G.has_edge(nodes[0].uuid, nodes[1].uuid)

    def test_bpm_tolerance(self):
        test_graph = Graph()
        nodes = test_graph.add_nodes(test_nodes)
        test_graph.recalculate_edges(bpm_tolerance=3)

        assert test_graph.G.number_of_edges() == 2
        assert test_graph.G.has_edge(nodes[0].uuid, nodes[1].uuid)
        assert test_graph.G.has_edge(nodes[2].uuid, nodes[3].uuid)

    def test_key_tolerance(self):
        test_graph = Graph()
        nodes = test_graph.add_nodes(test_nodes)
        test_graph.recalculate_edges(key_tolerance=2)

        assert test_graph.G.number_of_edges() == 2
        assert test_graph.G.has_edge(nodes[0].uuid, nodes[1].uuid)
        assert test_graph.G.has_edge(nodes[0].uuid, nodes[3].uuid)


class TestAddEdges:

    def test_add_edges(self):
        test_graph = Graph()
        nodes = test_graph.add_nodes(test_nodes)
        test_graph.recalculate_edges()

        assert test_graph.G.number_of_edges() == 1
        assert test_graph.G.has_edge(nodes[0].uuid, nodes[1].uuid)

        new_nodes = test_graph.add_nodes(test_additional_nodes)
        test_graph.add_edges(new_nodes)

        assert test_graph.G.number_of_edges() == 6
        assert test_graph.G.has_edge(nodes[0].uuid, new_nodes[0].uuid)
        assert test_graph.G.has_edge(nodes[1].uuid, new_nodes[1].uuid)
        assert test_graph.G.has_edge(nodes[0].uuid, new_nodes[1].uuid)
        assert test_graph.G.has_edge(nodes[1].uuid, new_nodes[0].uuid)
        assert test_graph.G.has_edge(new_nodes[1].uuid, new_nodes[2].uuid)


class TestClearGraph:

    def test_clear_graph(self):
        test_graph = Graph()
        test_graph.add_nodes(test_nodes)
        test_graph.recalculate_edges()

        assert test_graph.G.number_of_edges() == 1

        test_graph.clear()

        assert test_graph.G.number_of_edges() == 0
        assert test_graph.G.number_of_nodes() == 0
