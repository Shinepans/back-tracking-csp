### This is the another way to match players

import numpy as np
import math
class PM():
    Assignment = []
    Domain = []
    var = []
    cons1 = []
    participants = 0
    first_part_num = 0
    def __init__(self, assignment, domain, var, cons1, participants, num):
        self.Assignment = assignment
        self.Domain = domain
        self.var = var
        self.cons1 = cons1
        self.participants = participants
        self.first_part_num = num

    def value_consistent(self, pair_val, round):  # return a pair of players, p is the player that must invovled
        availablePair = self.Domain[pair_val]
        for i in range(0, availablePair.shape[0]):
            if availablePair[i] == 0 and i != pair_val and self.cons1[round, i] != 1:
                return i
        return -1

    def order_domain_values(self, round):
        round_players = self.cons1[round]
        result = []
        for i in range(0, len(round_players)):
            if round_players[i] == 0:
                result.append(i)

        return result  # could be 5,4,3,2,1,0

    def select_unsigned_var(self):
        for round in range(0, self.first_part_num):  # round:
            for pair in range(0, math.floor(self.participants/2)):  # pair:
                if self.var[round, pair] == -1:
                    return [round, pair]
        return -1  # this case should never show, if return -1, means all the cell has been filled

    def recursive(self):
        tot_var = self.first_part_num * math.floor(self.participants/2) * 2 - self.first_part_num
        if np.count_nonzero(self.Assignment) == tot_var:
            print("recursive: enter the close sentence")
            print(self.Assignment)
            return [True, self.Assignment]
        vars = self.select_unsigned_var()
        assert (vars != -1)  # if var == -1, means the matrix is completed
        round = vars[0]
        pair = vars[1]
        for pair_val in self.order_domain_values(round):
            match = self.value_consistent(pair_val, round)
            if match != -1:
                self.Assignment[round, pair, 0] = pair_val
                self.Assignment[round, pair, 1] = match
                self.Domain[pair_val, match] += 1
                self.Domain[match, pair_val] += 1
                self.cons1[round, pair_val] += 1
                self.cons1[round, match] += 1
                self.var[round, pair] += 1
                result = self.recursive()
                if result[0] != False:
                    return result
                self.Assignment[round, pair, 0] = 0
                self.Assignment[round, pair, 1] = 0
                self.Domain[pair_val, match] -= 1
                self.Domain[match, pair_val] -= 1
                self.cons1[round, pair_val] -= 1
                self.cons1[round, match] -= 1
                self.var[round, pair] -= 1
        return [False]

    def do_shuffle(self):
        result = self.recursive()
        print("Result: ", result)

ROUND = 8
PLAYER_NUMBER = 16
   
cons1 = np.zeros([PLAYER_NUMBER, PLAYER_NUMBER], dtype=int)
var = np.full([ROUND, math.floor(PLAYER_NUMBER/2) ], -1)
Domain = np.zeros([PLAYER_NUMBER, PLAYER_NUMBER], dtype=int)
Assignment = np.zeros([ROUND, math.floor(PLAYER_NUMBER/2), 2], dtype=int)
Matching = PM(Assignment,Domain, var, cons1, PLAYER_NUMBER, ROUND)

print(Matching.do_shuffle())
