from enum import Enum

class Piece:
    privileged = False
    coordinates = []

    def __init__(self, coords, is_privileged=False):
        """
        Coordinates are given as eg. [(0,1), (0,2), (0,3)] for a piece which appears on the top row across the
        second, third and fourth places.
        is_privileged refers to whether this piece is the one which needs to be sent to the exit.
        """
        self.coordinates = coords
        self.privileged = is_privileged

class Direction(Enum):
    up = 1
    right = 2
    down = 3
    left = 4


def opposite_direction(direction):
    if direction == Direction.up:
        return Direction.down
    elif direction == Direction.down:
        return Direction.up
    elif direction == Direction.left:
        return Direction.right
    elif direction == Direction.right:
        return Direction.left


class Move():
    direction = 0
    piece_num = 0

    def __init__(self, piece, direction):
        self.piece_num = piece
        self.direction = direction

    def __str__(self):
        return "Move piece {0} in direction {1}".format(self.piece_num, self.direction)

class Board:
    # board is a 2d array, with 0 an empty space, 1 a space occupied by the privileged block, then natural numbers for
    # each of the other blocks
    board = []

    # exit_position is a single integer; wlog the exit appears on the right-hand side of the board, so exit_position
    # gives only the distance from the top (indexed from 0).
    # For instance, if the exit is on the right-hand edge on the second row down from the top, exit_position would be 1.
    exit_position = -1

    # blocks_num holds the number of blocks
    blocks_num = 0

    @property
    def board_height(self): return len(self.board)

    @property
    def board_width(self):
        if len(self.board) > 0:
            return len(self.board[0])
        else:
            raise Exception("Board is empty but we tried to get its width.")

    def __init__(self, pieces_list, exit_pos, board_width=-1, board_height=-1):
        """
        Initialise the board using width, height and a list of Pieces:
        [Piece([(0,1),(0,2),(0,3)]), Piece([(1,0),(1,1)], is_privileged=True)]
        If width and height are absent, uses instead the smallest x and y coordinates possible from the
        board coordinates.
        exit_pos is a y-coordinate, distance from top of board: see the definition of Board.exit_position above.
        """

        # for initialisation purposes, if the board width and height were not given, we find the least possible
        # ones given the coordinates available. Note that we are not setting self.board_width.
        if board_width == -1:
            board_width = max(coord[1] for piece in pieces_list for coord in piece.coordinates)+1
        if board_height == -1:
            board_height = max(coord[0] for piece in pieces_list for coord in piece.coordinates)+1

        self.blocks_num = len(pieces_list)
        self.exit_position = exit_pos

        self.board = [[0 for x in range(board_width)] for y in range(board_height)]

        privileged_piece = [p for p in pieces_list if p.privileged]
        if len(privileged_piece) == 0:
            raise Exception("No privileged piece found.")
        elif len(privileged_piece) > 1:
            raise Exception("Too many privileged pieces: {0}.".format(privileged_piece))
        else:
            privileged_piece = privileged_piece[0]

        for coord in privileged_piece.coordinates:
            self.board[coord[0]][coord[1]] = 1

        piece_counter = 2
        for p in pieces_list:
            if not p.privileged:
                for coord in p.coordinates:
                    self.board[coord[0]][coord[1]] = piece_counter
                piece_counter += 1

    def __str__(self):
        rows = [''.join(str(i) for i in row) for row in self.board]
        rows[self.exit_position] += '|'
        return '\n'.join(rows) + '\n'

    def coords_of_piece(self, piece_number):
        """
        Returns the coordinates of the piece with specified number.
        """
        enumerated = [(x, y) for x in range(self.board_height) for y in range(self.board_height)]
        return [coords for coords in enumerated if self.board[coords[0]][coords[1]] == piece_number]

    def move_allowed(self, piece_number, direction):
        piece_coordinates = self.coords_of_piece(piece_number)

        bottom = max([coords[0] for coords in piece_coordinates])
        top = min([coords[0] for coords in piece_coordinates])
        left = min([coords[1] for coords in piece_coordinates])
        right = max([coords[1] for coords in piece_coordinates])

        try:
            if direction == Direction.up and left != right:
                raise Exception("Tried to move a piece up, but the piece has width greater than 1.")
            elif direction == Direction.down and left != right:
                raise Exception("Tried to move a piece down, but the piece has width greater than 1.")
            elif direction == Direction.right and top != bottom:
                raise Exception("Tried to move a piece right, but the piece has height greater than 1.")
            elif direction == Direction.left and top != bottom:
                raise Exception("Tried to move a piece left, but the piece has height greater than 1.")

            if direction == Direction.down:
                if bottom < self.board_height - 1:
                    if self.board[bottom+1][left] == 0:
                        pass
                    else:
                        raise Exception("Tried to move piece {0} down but it would be moving into a piece.".format(piece_number))
                else:
                    raise Exception("Tried to move piece {0} down but it is at the bottom already.".format(piece_number))
            elif direction == Direction.up:
                if top > 0:
                    if self.board[top-1][left] == 0:
                        pass
                    else:
                        raise Exception("Tried to move piece {0} up but it would be moving into a piece.".format(piece_number))
                else:
                    raise Exception("Tried to move piece {0} up but it is at the top already.".format(piece_number))
            elif direction == Direction.left:
                if left > 0:
                    if self.board[top][left-1] == 0:
                        pass
                    else:
                        raise Exception("Tried to move piece {0} left but it would be moving into a piece.".format(piece_number))
                else:
                    raise Exception("Tried to move piece {0} left but it is already on the edge.".format(piece_number))
            elif direction == Direction.right:
                if right < self.board_width - 1:
                    if self.board[top][right+1] == 0:
                        pass
                    else:
                        raise Exception("Tried to move piece {0} right but it would be moving into a piece.".format(piece_number))

                else:
                    raise Exception("Tried to move piece {0} left but it is already on the edge.".format(piece_number))
        except:
            return False

        return True

    def slide_piece(self, move=None, piece_number=None, direction=None):
        """
        Returns the board state when the given slide is made on the board. Does not alter the board.
        """
        if move is not None:
            return self.slide_piece(piece_number=move.piece_num, direction=move.direction)
        backup_board = self.board
        self.slide_piece_in_place(piece_number, direction)
        new_board = self.board
        self.board = backup_board
        return new_board

    def slide_piece_in_place(self, move=None, piece_number=None, direction=None):
        """
        Alters the board so that the piece with specified number moves in the specified direction.
        direction should be a Direction enum.
        """
        if move is not None:
            self.slide_piece_in_place(piece_number=move.piece_num, direction=move.direction)
            return

        # check if we're moving an existent piece
        if piece_number > self.blocks_num:
            raise Exception("Attempted to move a piece ({0}) which is not present.".format(piece_number))
        elif piece_number < 0:
            raise Exception("Attempted to move a negative-numbered piece ({0}).".format(piece_number))

        if self.move_allowed(piece_number, direction):

            piece_coordinates = self.coords_of_piece(piece_number)

            bottom = max([coords[0] for coords in piece_coordinates])
            top = min([coords[0] for coords in piece_coordinates])
            left = min([coords[1] for coords in piece_coordinates])
            right = max([coords[1] for coords in piece_coordinates])

            if direction == Direction.down:
                self.board[bottom+1][left] = piece_number
                self.board[top][left] = 0
            elif direction == Direction.up:
                self.board[top-1][left] = piece_number
                self.board[bottom][left] = 0
            elif direction == Direction.left:
                self.board[top][left-1] = piece_number
                self.board[top][right] = 0
            elif direction == Direction.right:
                self.board[top][right+1] = piece_number
                self.board[top][left] = 0

    def find_available_moves(self):
        """
        Produces a list of Move objects corresponding to how each piece can move.
        """

        avail = []  # will be a list: [[Move(1, dir), Move(1, dir)], [Move(2, dir)], …]

        for piece in range(self.blocks_num):
            # find how piece+1 can move
            piece_coordinates = self.coords_of_piece(piece+1)
            bottom = max([coords[0] for coords in piece_coordinates])
            top = min([coords[0] for coords in piece_coordinates])
            left = min([coords[1] for coords in piece_coordinates])
            right = max([coords[1] for coords in piece_coordinates])

            allowable = [Direction.left, Direction.right, Direction.up, Direction.down]
            if bottom != top:
                # we can't move left or right
                allowable.remove(Direction.left)
                allowable.remove(Direction.right)
            if left != right:
                allowable.remove(Direction.up)
                allowable.remove(Direction.down)

            avail.append([Move(piece+1, direction=direc) for direc in allowable if self.move_allowed(piece+1, direc)])

        return [m for piece in avail for m in piece]

    def is_solved(self):
        """
        Returns True iff the board may be solved in one move.
        """
        piece_coordinates = self.coords_of_piece(1)

        return max([coords[0] for coords in piece_coordinates]) == self.exit_position and \
               max([coords[1] for coords in piece_coordinates]) == self.board_width-1


pieces = [Piece([(0,4), (1,4), (2,4)]),
          Piece([(2,2),(2,3)], is_privileged=True),
          Piece([(3,3),(4,3)]),
          Piece([(4,4),(4,5)])]
board = Board(pieces, exit_pos=2, board_width=6, board_height=6)
print(str(board))

print("Which pieces can move where?")
print([str(m) for m in board.find_available_moves()])

print("Solution follows.")

board.slide_piece_in_place(piece_number=1, direction=Direction.left)
print(str(board))
board.slide_piece_in_place(piece_number=3, direction=Direction.up)
print(str(board))
board.slide_piece_in_place(piece_number=4, direction=Direction.left)
board.slide_piece_in_place(piece_number=4, direction=Direction.left)
board.slide_piece_in_place(piece_number=4, direction=Direction.left)
print(str(board))
board.slide_piece_in_place(piece_number=3, direction=Direction.down)
board.slide_piece_in_place(piece_number=2, direction=Direction.down)
board.slide_piece_in_place(piece_number=2, direction=Direction.down)
board.slide_piece_in_place(piece_number=2, direction=Direction.down)
print(str(board))
board.slide_piece_in_place(piece_number=1, direction=Direction.right)
board.slide_piece_in_place(piece_number=1, direction=Direction.right)
board.slide_piece_in_place(piece_number=1, direction=Direction.right)
print(str(board))
print("Solved!" if board.is_solved() else "Not solved.")