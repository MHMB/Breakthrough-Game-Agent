import copy
from random import randint
from board import Board


class Agent:
    def __init__(self, color, oppopnentColor, time=None):
        self.color = color
        self.oppopnentColor = oppopnentColor

    def cal_next_move(self, tree):
        return tree.root.decisionChild.get_from_cell(), tree.root.decisionChild.get_to_cell()

    def move(self, board):
        pruned_tree = Tree(board, self.color, self.oppopnentColor, 3)
        from_cell, to_cell = self.cal_next_move(pruned_tree)
        return from_cell, to_cell
        

class Node:
    def __init__(self, from_cell, to_here_cell, board, maximizer):
        self.children = []
        self.from_cell = from_cell
        self.to_here_cell = to_here_cell
        self.decisionChild = None
        self.board = board
        self.alpha = -200
        self.beta = 200
        self.maximizer = maximizer
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
        self.value = eval_value
        print('Eval Value: ', eval_value)
            
    def set_utility(self, utility):
        self.value = utility

    def set_child(self, child):
        self.children.append(child)

    def get_from_cell(self):
        return self.from_cell

    def get_to_cell(self):
        return self.to_here_cell

    def is_maximizer(self):
        return self.maximizer

    def setDecisionChild(self, decisionChild):
        self.decisionChild = decisionChild

        

class Tree:
    def __init__(self, board, color, opponentColor, height):
        self.height = height
        self.board = board
        self.root = self.make_node(0, board, True)
        self.build_pruned_tree(color, opponentColor)

    def make_node(self, height, board, isMaximizer, from_cell=None, to_cell=None):
        node = Node(from_cell, to_cell, board, isMaximizer)
        return node

    def build_pruned_tree(self, color, opponentColor):
        print('start build Tree')
        self.expand_node(self.root, self.height-1, color, opponentColor)
        print('end build Tree')

    def expand_node(self, node, height, color, opponentColor):
        if height == 0:
            return node.evaluation_function(color, opponentColor)
        else:
            piecesFromCell, piecesToCell = node.board.getPiecesPossibleLocations(color)
            for i in range(len(piecesToCell)):
                for j in range(len(piecesToCell[i])):
                    newBoard = copy.deepcopy(node.board)
                    newBoard.changePieceLocation(color, piecesFromCell[i], piecesToCell[i][j])
                    childNode = self.make_node(height, newBoard, not node.maximizer ,piecesFromCell[i], piecesToCell[i][j])
                    node.set_child(childNode)
                    if node.is_maximizer() and node.value < childNode.value or not node.is_maximizer() and node.value > childNode.value:
                        self.expand_node(childNode, height-1, color, opponentColor)
                        if node.is_maximizer() and node.value < childNode.value:
                            node.set_utility(childNode.value)
                            node.setDecisionChild(childNode)
                        elif not(node.is_maximizer()) and node.value > childNode.value:
                            node.set_utility(childNode.value)
                            node.setDecisionChild(childNode)

            print('node value: ', node.value)
            return node.value