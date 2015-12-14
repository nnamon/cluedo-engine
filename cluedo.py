#!/usr/bin/python

class CluedoEngine:

    def __init__(self, card_sets, player_list, name):
        self.card_sets = card_sets
        self.no_cards = sum(len(i) for i in card_sets)
        self.player_list = player_list
        self.name = name
        if self.name not in self.player_list:
            raise Exception("You must be in the game!")
        self.no_open = (self.no_cards - len(self.card_sets)) % len(self.player_list)
        self.no_cardsper = ((self.no_cards - len(self.card_sets)) - self.no_open) / len(self.player_list)
        self.definite = self.no_cardsper
        self.players = self.player_list
        self.player_list.append("+")
        self.player_list.append("-")
        self.flat = self.flatten_sets(self.card_sets)
        self.generate_matrices()

    def generate_matrices(self):
        self.matrices = {}
        for i in self.players:
            self.matrices[i] = self.initialise_matrix()
        # The first version will not use the derivative matrices

    def initialise_matrix(self):
        outer_matrix = {}
        for i in self.player_list:
            inner_matrix = {}
            for j in self.flat:
                inner_matrix[j] = -1
            outer_matrix[i] = inner_matrix
        return outer_matrix

    def flatten_sets(self, sets):
        flat = []
        for i in sets:
            for j in i:
                flat.append(j)
        return flat

    def print_matrix(self, matrix):
        text = ""
        longest_item = max(len(i) for i in self.flat)
        longest_name = max(max(len(i) for i in self.player_list), 5)
        header = " " * (longest_item + 1) + "|" + "|".join(i.ljust(longest_name, " ") for i in self.player_list) + "|"
        text += header + "\n"
        for i in self.flat:
            vals = []
            for j in self.player_list:
                vals.append(matrix[j][i])
            line = i.ljust(longest_item + 1, " ") + "|" + "|".join(("%.2f" % j).rjust(longest_name, " ") for j in vals) + "|"
            text += line + "\n"
        return text

    def mark_definite(self, thename, confirmed):
        # Only handles the player's matrix in this version
        pm = self.matrices[self.name]
        for i in pm.keys():
            for j in confirmed:
                if i == thename:
                    pm[i][j] = self.definite
                else:
                    pm[i][j] = 0

    def print_player(self):
        print self.print_matrix(self.matrices[self.name])

    def open_cards(self, opened):
        self.mark_definite("+", opened)

    def personal_cards(self, my_cards):
        self.mark_definite(self.name, my_cards)

def main():
    cards = [("X.1", "X.2", "X.3", "X.4", "X.5"), ("Y.1", "Y.2", "Y.3"), ("Z.1", "Z.2", "Z.3", "Z.4", "Z.5", "Z.6")]
    players = ["A", "B", "C"]
    cluedo = CluedoEngine(cards, players, "A")

    opened = ["Z.5", "Z.6"]
    cluedo.open_cards(opened)
    cluedo.print_player()

    my_cards = ["X.1", "X.2", "X.4"]
    cluedo.personal_cards(my_cards)
    cluedo.print_player()

if __name__ == "__main__":

    main()
