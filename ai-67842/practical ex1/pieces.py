import os

"""
Classes and utilities to describe all of the game pieces.
"""


def negate_list_positive(lst):
    """
    Helper function: negate every item in a list
    """
    new_list = [-x for x in lst]
    list_min = min(new_list)
    return [x - list_min for x in new_list]


class Piece(object):
    """
    A piece is a collection of tiles with various (x,y) offsets.

    Variables:
    - x: Lists of x coordinates of the piece
    - y: Lists of y coordinates of the piece

    x and y each have 8 elements, which are:
    x/y[0]: Initial orientation
    x/y[1]: Rotated CW once
    x/y[2]: Rotated CW twice
    x/y[3]: Rotated CW three times
    x/y[k+4]: x/y[k] flipped horizontally
    """

    def __init__(self, x_list, y_list):
        if len(x_list) != len(y_list):
            raise ValueError(
                "Length of x and y lists are unequal (%d and %d)" % (len(x_list), len(y_list)))
        if len(x_list) == 0:
            raise ValueError("No tiles provided!")
        if len(x_list) > 5:
            raise ValueError("%d tiles provided; maximum 5" % len(x_list))

        minx = min(x_list)
        miny = min(y_list)

        x_list = [x - minx for x in x_list]
        y_list = [y - miny for y in y_list]

        # Calculate flipped lists
        x_list_flipped = negate_list_positive(x_list)
        y_list_flipped = negate_list_positive(y_list)

        # Set up data structure
        x_lists = []
        y_lists = []

        # Position 0: default
        x_lists.append(x_list)
        y_lists.append(y_list)

        # Position 1: rotated x1
        x_lists.append(y_list)
        y_lists.append(x_list_flipped)

        # Position 2: rotated x2
        x_lists.append(x_list_flipped)
        y_lists.append(y_list_flipped)

        # Position 3: rotated x3
        x_lists.append(y_list_flipped)
        y_lists.append(x_list)

        # Positions 4-7: flipped copies
        for i in range(4):
            x_lists.append(negate_list_positive(x_lists[i]))
            y_lists.append(y_lists[i])

        self.orientations = set()

        for (x_list, y_list) in zip(x_lists, y_lists):
            self.orientations.add(frozenset(zip(x_list, y_list)))

        self.num_tiles = len(x_list)
        self.orientations = frozenset(self.orientations)

        self.x = x_list
        self.y = y_list

    def get_num_tiles(self):
        """
        Return the number of tiles in this block. Helpful for iterating
        through each tile.
        """
        return self.num_tiles

    def copy(self):
        return Piece(self.x[0], self.y[0])

    def __iter__(self):
        return self.orientations.__iter__()

    def __str__(self):
        out_str = []
        for ori in self:
            temp_arr = [[' ' for _ in range(5)] for _ in range(5)]
            for (x, y) in ori:
                temp_arr[y][x] = '0'
            temp_arr = '\n'.join(
                [''.join([x_pos for x_pos in temp_arr[y_val]])
                 for y_val in range(5)]
            )
            out_str.append(temp_arr)
        return '\n'.join(out_str)

    def __eq__(self, other):
        return self.orientations.__eq__(other.orientations)

    def __hash__(self):
        return self.orientations.__hash__()


class PieceList(object):
    """
    The PieceList class stores a list of all of the Blokus game pieces (the
    distinct 5-polyominos).
    """

    def __init__(self, fname=None):
        """
        Read the game pieces from the file <fname>

        File format must be:
        - Line 1: n (number of pieces)
        - For k in [0, n):
          - Line 1: line_index (number of lines in piece)
          - Lines 2 - line_index+1: layout of piece (# means tile, O means center)

        Sample file:
        2
        2
        O#
        ##
        1
        ##O##
        """
        self.pieces = []
        directory = "layouts"
        if fname is not None:
            with open(os.path.join(directory, fname)) as f:
                lines = f.read().splitlines()

            n = int(lines[0])
            line_index = 1
            for i in range(n):
                x_origin = 0
                y_origin = 0

                x_list = []
                y_list = []

                num_lines = int(lines[line_index])
                for j in range(num_lines):
                    line = lines[line_index + 1 + j]
                    for k in range(len(line)):
                        if line[k] in ('O', 'o', '0'):
                            x_origin = k
                            y_origin = j
                        if line[k] is not ' ':
                            x_list.append(k)
                            y_list.append(j)

                x_list = [x - x_origin for x in x_list]
                y_list = [y - y_origin for y in y_list]
                self.pieces.append(Piece(x_list, y_list))

                line_index += 1 + num_lines

    def get_num_pieces(self):
        """
        Return the number of distinct pieces in the list.
        """
        return len(self.pieces)

    def get_piece(self, n):
        """
        Return piece <n> from this list.
        """
        if n < 0:
            raise ValueError("Can't retrieve piece %d" % n)

        return self.pieces[n]

    def __iter__(self):
        return self.pieces.__iter__()

    def copy(self):
        cpy_p_list = PieceList(None)
        cpy_p_list.pieces = [piece.copy() for piece in self.pieces]
        return cpy_p_list
