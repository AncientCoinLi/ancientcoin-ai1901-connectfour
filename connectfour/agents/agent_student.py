from connectfour.agents.computer_player import RandomAgent
import random


class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 1

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        # I wanna user all_moves so I have to update this variable myself
        self.__update_all_moves(board, board.last_move)
        self.__update_scores(board, board.last_move, False)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, 1) )

        best_move = moves[vals.index( max(vals) )]

        # update all_moves in board, and convert tuple to list
        # to prevent the opposite all_moves, check if this move in all_moves
        self.__update_all_moves(board, list(best_move))
        self.__update_scores(board, list(best_move), True)
        return best_move

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states

        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])

            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1) )

        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

    def evaluateBoardState(self, board):
        """
        Your evaluation function should look at the current state and return a score for it. 
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """

        if self.id == 1:
            self_index = 0
            other_index = 1
            other_id = 2
        else:
            self_index = 1
            other_index = 0
            other_id = 1

        if board.winner() == self.id:
            return 1
        elif board.winner() == 0:
            self.__update_scores(board, board.last_move, True)
            last_row = board.last_move[0]
            last_col = board.last_move[1]
            standard = len(board.winning_zones[last_col][last_row])

            # minimise opposite's benefit
            score = -1
            count_of_3_oppo = -100
            count_of_3_self = -100
            count = 0
            for win_index in range(len(board.score_array[other_index])):
                if board.score_array[self_index][win_index] - board.score_array[other_index][win_index] == 3:
                    count += 1
            if count > count_of_3_oppo:
                count_of_3_self = count
            for col in range(board.width):
                row = board.try_move(col)
                next_state = board.next_state(other_id, col)
                if next_state != 0:
                    if next_state.winner() == other_id:
                        return -1
                    self.__update_scores(next_state, [row, col], False)
                    index = -1
                    count = 0
                    for win_index in range(len(next_state.score_array[other_index])):
                        if next_state.score_array[other_index][win_index] - next_state.score_array[self_index][win_index] == 3:
                            count += 1
                    if count > count_of_3_oppo:
                        count_of_3_oppo = count

            num_of_winning_zones = len(board.winning_zones[col][row])
            ratio = (standard - num_of_winning_zones + 100/(count_of_3_oppo+1) + count_of_3_self * 10) / 150
            if ratio > score:
                score = ratio
            return score
            # return self.__negamax(board, node_count, self.id)
        else:
            return -1
        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """
        return random.uniform(0, 1)

    def __update_all_moves(self, board, move):
        if move is None:
            return
        if move not in board.all_moves:
            board.all_moves.append(move)

    def __update_scores(self, board, move, is_for_self):
        if move is None or move[0] is None:
            return
        col = move[1]
        row = move[0]
        if self.id == 1:
            if is_for_self:
                is_player_one = True
            else:
                is_player_one = False
        elif self.id == 2:
            if is_for_self:
                is_player_one = False
            else:
                is_player_one = True
        # check if score of this move has been updated
        if len(board.winning_zones[col][row]) != 0:
            # update scores
            board.update_scores(col, row, "", is_player_one)
            # remove win_index of this move in winning_zones
            # board.winning_zones[col][row] = []





