from random import randint
from board import Board


class Agent:
    def __init__(self, color, oppopnentColor, time=None):
        self.color = color
        self.oppopnentColor = oppopnentColor

    def move(self, board):
       node = Node(None, None, board, True)
       print(node.evaluation_function(self.color, self.oppopnentColor))

# class MyBoard(Board):
#     def getOpponentArmy(self, op_color):
        

class Node:
    def __init__(self, from_cell, to_here_cell, board, maximizer):
        self.children = []
        self.from_cell = from_cell
        self.to_here_cell = to_here_cell
        self.board = board
        self.alpha = -200
        self.beta = 200
        if maximizer:
            self.value = self.alpha
        else:
            self.value = self.beta

    def evaluation_function(self, color, opponentColor):
        eval_value = self.board.getNumberOfArmy(color)
        eval_value -= self.board.getNumberOfArmy(opponentColor)
        my_army_postions = self.board.travelOverBoard(color)
        opponent_army_postions = self.board.travelOverBoard(opponentColor)
        if color == 'B':
            best_row = 1
            dir = -1
            worst_row = 4
        else:
            best_row = 4
            dir = 1
            worst_row = 1
        for pos in my_army_postions:
            if pos[0] == best_row:
                eval_value += 5
            elif pos[0] == best_row+dir:
                eval_value += 100
            else:
                if self.board.board[pos[0]+dir][pos[1]] == 'E':
                    eval_value += 1
        for pos in opponent_army_postions:
            if pos[0] == worst_row:
                eval_value -= 5
            elif pos[0] == worst_row-dir:
                eval_value -= 100
            else:
                if self.board.board[pos[0]-dir][pos[1]] == 'E':
                    eval_value -= 1
        print('Eval Value: ', eval_value)
            
    def set_utility(self, utility):
        self.value = utility

    def set_child(self, child):
        self.children.append(child)

    def get_from_cell(self):
        return self.from_cell

        

class Tree:
    def __init__(self, board, color, oppopnentColor, height):
        self.height = height
        self.board = board
        self.nodes = [[] for i in range(self.height+1)]
        self.root = self.make_node(0, board)

    def make_node(self, height, board, from_cell=None, to_cell=None):
        node = Node(from_cell, to_cell, board, True)
        self.nodes[height].append(node)
        return node

    def build_pruned_tree(self, color, oppopnentColor):
        maxNodes = [self.root]
        minNodes = []
        maxTurn = True

    def expand_node(self):
        pass