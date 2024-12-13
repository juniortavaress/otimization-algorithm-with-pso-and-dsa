# -*- coding: utf-8 -*-
import re
import json

class OdbUtils():
    @staticmethod
    def initialize_data():
        """
        Initializes the temperature ranges and tool node mappings.
        """
        node_range_strs = {
            "h0025": "840, 10656:10628:-1, 148, 6594:6581:-1, 433, 93117:93125:1, 6244",
            "h0050": "701, 17491:17463:-1, 1105, 21538:21525:-1, 1449, 74255:74247:-1, 5217",
            "h0075": "721, 18941:18913:-1, 1125, 22988:22975:-1, 1469, 75705:75697:-1, 5227",
            "h0100": "741, 20391:20363:-1, 1145, 24438:24425:-1, 1489, 77155:77147:-1, 5237"
        }

        spanwinkel_nodes = {
            "+6": 2878,  # Spanwinkel +6° → Knoten 2878
            "-6": 1795   # Spanwinkel -6° → Knoten 1795
        }
        return node_range_strs, spanwinkel_nodes

    @staticmethod
    def extract_info_from_filename(filename):
        """
            Extracts rake angle (gam) and thickness (h) from the filename.

            :param filename: Name of the ODB file
            :return: A tuple (gam, h)
        """
        gam_match = re.search(r"_gam([+-]\d+)_", filename)
        h_match = re.search(r"h(\d+)", filename)
        # Extrair os valores com segurança e formato adequado
        gam = gam_match.group(1) if gam_match else None
        h = "h{}".format(h_match.group(1)) if h_match else None
        return gam, h

    @staticmethod
    def generate_node_path(node_range_str):
        """
        Generates a list of node labels based on the node range string.

        :param node_range_str: A string defining node ranges
        :return: A list of node labels
        """
        node_ranges = node_range_str.split(', ')
        node_labels = []

        for node_range in node_ranges:
            if ':' in node_range:
                # Verarbeite Knotenbereiche
                start, end, step = map(int, node_range.split(':'))
                node_labels.extend(range(start, end + step, step))  # +step, um sicherzustellen, dass der Endknoten enthalten ist
            else:
                # Verarbeite einzelne Knotenlabels
                node_labels.append(int(node_range))   
        
        return node_labels

    @staticmethod
    def calculate_distances(nodes, node_path):
        """Calculate cumulative distances between nodes along a path."""
        coords = {node.label: node.coordinates for node in nodes}
        distances = [0.0]
        for i in range(1, len(node_path)):
            dist = sum(
                (coords[node_path[i]][j] - coords[node_path[i - 1]][j]) ** 2
                for j in range(3)
            ) ** 0.5
            distances.append(distances[-1] + dist)
        return distances



