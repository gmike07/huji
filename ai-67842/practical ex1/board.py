import numpy as np


class Board:

    """
    A Board describes the current state of the game board. It's separate from
    the game engine to allow the Input objects to check if their moves are valid,
    etc... without the help of the game engine.

    The Board stores:
    - board_w/board_h: the width and height of the playing area
    - state: a 2D array of the board state. -1 = free; 0-3 = player x's tile
    - _legal: a 4 x 2D array. _legal[player][y][x] is True iff (x,y) is not
      on another player's piece or adjacent to a player's own piece
    - connected: a 4 x 2D array. _connected[player][y][x] is True iff (x,y) is
      diagonally connected to another one of the player's tiles
    - piece_list: A PieceList object (probably shared with the game engine) to
      help understand the moves
    """

    def __init__(self, board_w, board_h, num_players, piece_list, starting_point=(0, 0)):
        self.board_w = board_w
        self.board_h = board_h
        self.num_players = num_players
        self.scores = [0] * self.num_players

        self.state = np.full((board_h, board_w), -1, np.int8)

        self._legal = np.full((num_players, board_h, board_w), True, np.bool_)

        self.connected = np.full((num_players, board_h, board_w), False, np.bool_)
        self.connected[0, starting_point[0], starting_point[1]] = True
        self.piece_list = piece_list
        self.pieces = np.full((num_players, piece_list.get_num_pieces()), True, np.bool_)

    def add_move(self, player, move):
        """
        Try to add <player>'s <move>.

        If the move is legal, the board state is updated; if it's not legal, a
        ValueError is raised.

        Returns the number of tiles placed on the board.
        """
        if not self.check_move_valid(player, move):
            raise ValueError("Move is not allowed")

        piece = move.piece
        self.pieces[player, move.piece_index] = False  # mark piece as used

        # Update internal state for each tile
        for (xi, yi) in move.orientation:
            (x, y) = (xi + move.x, yi + move.y)
            self.state[y, x] = player

            # Nobody can play on this square
            for p in range(self.num_players):
                self._legal[p][y][x] = False

            # This player can't play next to this square
            if x > 0:
                self._legal[player, y, x - 1] = False
            if x < self.board_w - 1:
                self._legal[player, y, x + 1] = False
            if y > 0:
                self._legal[player, y - 1, x] = False
            if y < self.board_h - 1:
                self._legal[player, y + 1, x] = False

            # The diagonals are now attached
            if x > 0 and y > 0:
                self.connected[player, y - 1, x - 1] = True
            if x > 0 and y < self.board_h - 1:
                self.connected[player, y + 1, x - 1] = True
            if x < self.board_w - 1 and y < self.board_h - 1:
                self.connected[player, y + 1, x + 1] = True
            if x < self.board_w - 1 and y > 0:
                self.connected[player, y - 1, x + 1] = True

        self.scores[player] += piece.get_num_tiles()
        return piece.get_num_tiles()

    def do_move(self, player, move):
        """
        Performs a move, returning a new board
        """
        new_board = self.__copy__()
        new_board.add_move(player, move)

        return new_board

    def get_legal_moves(self, player):
        """
        Returns a list of legal moves for given player for this board state 
        """
        # Generate all legal moves
        move_list = []
        for piece in self.piece_list:
            for x in range(self.board_w - 1):
                for y in range(self.board_h - 1):
                    for ori in piece:
                        new_move = Move(piece,
                                        self.piece_list.pieces.index(piece),
                                        ori, x, y)
                        if self.check_move_valid(player, new_move):
                            move_list.append(new_move)
        return move_list

    def check_move_valid(self, player, move):
        """
        Check if <player> can legally perform <move>.

        For a move to be valid, it must:
        - Use a piece that is available
        - Be completely in bounds
        - Not be intersecting any other tiles
        - Not be adjacent to any of the player's other pieces
        - Be diagonally attached to one of the player's pieces or their corner

        Return True if the move is legal or False otherwise.
        """
        if not self.pieces[player, move.piece_index]:
            # piece has already been used
            return False

        attached_corner = False

        for (x, y) in move.orientation:
            # If any tile is illegal, this move isn't valid
            if not self.check_tile_legal(player, x + move.x, y + move.y):
                return False

            if self.check_tile_attached(player, x + move.x, y + move.y):
                attached_corner = True

            # If at least one tile is attached, this move is valid
        return attached_corner

    def check_tile_legal(self, player, x, y):
        """
        Check if it's legal for <player> to place one tile at (<x>, <y>).

        Legal tiles:
        - Are in bounds
        - Don't intersect with existing tiles
        - Aren't adjacent to the player's existing tiles

        Returns True if legal or False if not.
        """

        # Make sure tile in bounds
        if x < 0 or x >= self.board_w or y < 0 or y >= self.board_h:
            return False

        # Otherwise, it's in the lookup table
        return self._legal[player, y, x]

    def check_tile_attached(self, player, x, y):
        """Check if (<x>, <y>) is diagonally attached to <player>'s moves.

        Note that this does not check if this move is legal.

        Returns True if attached or False if not.
        """

        # Make sure tile in bounds
        if x < 0 or x >= self.board_w or y < 0 or y >= self.board_h:
            return False

        # Otherwise, it's in the lookup table
        return self.connected[player, y, x]

    def get_position(self, x, y):
        return self.state[y, x]

    def score(self, player):
        return self.scores[player]

    def __eq__(self, other):
        return np.array_equal(self.state, other.state) and np.array_equal(self.pieces, other.pieces)

    def __hash__(self):
        return hash(str(self.state))

    def __str__(self):
        out_str = []
        for row in range(self.board_h):
            for col in range(self.board_w):
                if self.state[col, row] == -1:
                    out_str.append('_')
                else:
                    out_str.append(str(self.state[col, row]))
            out_str.append('\n')
        return ''.join(out_str)

    def __copy__(self):
        cpy_board = Board(self.board_w, self.board_h, self.num_players, self.piece_list)
        cpy_board.state = np.copy(self.state)
        cpy_board._legal = np.copy(self._legal)
        cpy_board.connected = np.copy(self.connected)
        cpy_board.pieces = np.copy(self.pieces)
        cpy_board.scores = self.scores[:]
        return cpy_board


class Move:
    """
    A Move describes how one of the players is going to spend their move.

    It contains:
    - Piece: the ID of the piece being used
    - x/y: the center coordinates of the piece [0-19)
    - Rotation: how many times the piece should be rotated CW [0-3]
    - Flip: whether the piece should be flipped (True/False)
    """

    def __init__(self, piece, piece_index, orientation, x=0, y=0):
        self.piece = piece
        self.piece_index = piece_index
        self.x = x
        self.y = y
        self.orientation = orientation

    def __str__(self):
        out_str = [[' ' for _ in range(5)] for _ in range(5)]
        for (x, y) in self.orientation:
            out_str[x][y] = '0'
        out_str = '\n'.join(
            [''.join([x_pos for x_pos in out_str[y_val]])
             for y_val in range(5)]
        )
        return ''.join(out_str) + "x: " + str(self.x) + " y: " + str(self.y)
