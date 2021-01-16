from enum import Enum

class Piece(Enum):
  PAWN = 1
  ROOK = 2
  KNIGHT = 3
  BISHOP = 4
  QUEEN = 5
  KING = 6

class Side(Enum):
  WHITE = 1
  BLACK = 2

class OwnedPiece:
  def __init__(self, piece, side):
    self.piece = piece
    self.side = side

  def value(self):
    if self.piece == Piece.PAWN:
      return 1
    elif self.piece == Piece.BISHOP or self.piece == Piece.KNIGHT:
      return 3
    elif self.piece == Piece.ROOK:
      return 5
    elif self.piece == Piece.QUEEN:
      return 9
    else:
      return 10000000
  
  def __str__(self):
    pieceStr = ""
    if self.piece == Piece.PAWN:
      pieceStr = 'P'
    elif self.piece == Piece.ROOK:
      pieceStr = 'R'
    elif self.piece == Piece.KNIGHT:
      pieceStr = 'N'
    elif self.piece == Piece.BISHOP:
      pieceStr = 'B'
    elif self.piece == Piece.QUEEN:
      pieceStr = 'Q'
    else: # self.piece == Piece.KING
      pieceStr = 'K'
    
    if self.side == Side.BLACK:
      pieceStr = pieceStr.lower()
    
    return pieceStr

class Board:
  def __init__(self):
    self.current_turn = Side.WHITE
    self.board = [[None for j in range(8)] for i in range(8)]
    self.place_piece('a2', OwnedPiece(Piece.PAWN, Side.WHITE))
    self.place_piece('b2', OwnedPiece(Piece.PAWN, Side.WHITE))
    self.place_piece('c2', OwnedPiece(Piece.PAWN, Side.WHITE))
    self.place_piece('d2', OwnedPiece(Piece.PAWN, Side.WHITE))
    self.place_piece('e2', OwnedPiece(Piece.PAWN, Side.WHITE))
    self.place_piece('f2', OwnedPiece(Piece.PAWN, Side.WHITE))
    self.place_piece('g2', OwnedPiece(Piece.PAWN, Side.WHITE))
    self.place_piece('h2', OwnedPiece(Piece.PAWN, Side.WHITE))
    self.place_piece('a1', OwnedPiece(Piece.ROOK, Side.WHITE))
    self.place_piece('b1', OwnedPiece(Piece.KNIGHT, Side.WHITE))
    self.place_piece('c1', OwnedPiece(Piece.BISHOP, Side.WHITE))
    self.place_piece('d1', OwnedPiece(Piece.QUEEN, Side.WHITE))
    self.place_piece('e1', OwnedPiece(Piece.KING, Side.WHITE))
    self.place_piece('f1', OwnedPiece(Piece.BISHOP, Side.WHITE))
    self.place_piece('g1', OwnedPiece(Piece.KNIGHT, Side.WHITE))
    self.place_piece('h1', OwnedPiece(Piece.ROOK, Side.WHITE))
    self.place_piece('a7', OwnedPiece(Piece.PAWN, Side.BLACK))
    self.place_piece('b7', OwnedPiece(Piece.PAWN, Side.BLACK))
    self.place_piece('c7', OwnedPiece(Piece.PAWN, Side.BLACK))
    self.place_piece('d7', OwnedPiece(Piece.PAWN, Side.BLACK))
    self.place_piece('e7', OwnedPiece(Piece.PAWN, Side.BLACK))
    self.place_piece('f7', OwnedPiece(Piece.PAWN, Side.BLACK))
    self.place_piece('g7', OwnedPiece(Piece.PAWN, Side.BLACK))
    self.place_piece('h7', OwnedPiece(Piece.PAWN, Side.BLACK))
    self.place_piece('a8', OwnedPiece(Piece.ROOK, Side.BLACK))
    self.place_piece('b8', OwnedPiece(Piece.KNIGHT, Side.BLACK))
    self.place_piece('c8', OwnedPiece(Piece.BISHOP, Side.BLACK))
    self.place_piece('d8', OwnedPiece(Piece.QUEEN, Side.BLACK))
    self.place_piece('e8', OwnedPiece(Piece.KING, Side.BLACK))
    self.place_piece('f8', OwnedPiece(Piece.BISHOP, Side.BLACK))
    self.place_piece('g8', OwnedPiece(Piece.KNIGHT, Side.BLACK))
    self.place_piece('h8', OwnedPiece(Piece.ROOK, Side.BLACK))
  
  def chess_square_to_indices(self, square):
    x = ord(square[0].lower()) - ord('a')
    y = int(square[1]) - 1
    return (x, y)

  def place_piece(self, square, piece):
    x, y = self.chess_square_to_indices(square)
    self.board[y][x] = piece

  def remove_piece(self, square):
    x, y = self.chess_square_to_indices(square)
    piece = self.board[y][x]
    self.board[y][x] = None
    return piece

  def move_piece(self, from_square, to_square):
    # TODO: validate move is valid
    piece = self.remove_piece(from_square)
    self.place_piece(to_square, piece)
    if self.current_turn == Side.WHITE:
      self.current_turn = Side.BLACK
    else:
      self.current_turn = Side.WHITE

  def evaluate_board(self, side):
    black_score = 0
    white_score = 0
    for row in self.board:
      for piece in row:
        if piece is not None:
          if piece.side == Side.WHITE:
            white_score += piece.value()
          else:
            black_score += piece.value()
    if side == Side.WHITE:
      return white_score - black_score
    else:
      return black_score - white_score

  def print_board(self):
    for row_ind, row in enumerate(reversed(self.board)):
      print("{}  ".format(8 - row_ind), end='')
      for piece in row:
        if piece is None:
          print(" _ ", end='')
        else:
          print(" {} ".format(piece), end='')
      print()
    print()
    print('    a  b  c  d  e  f  g  h')
    print()
  

class Game:
  def __init__(self, side):
    self.side = side
    self.board = Board()

  def turn(self):
    # Recommend a move if it's bot's turn
    if self.side == self.board.current_turn:
      # TODO:  Recommend a move
      print("recommend a move")

    # Confirm a move by user
    from_square, to_square = self.get_user_move()
    self.board.move_piece(from_square, to_square)
    
    # Board state
    print("Board evaluation score: {}".format(self.board.evaluate_board(self.side)))
    self.board.print_board()

  def get_user_move(self):
    sure = False
    from_square = None
    to_square = None
    while not sure:
      from_square = input("From Square:")
      to_square = input("To Square:")
      sure = input("You sure? Y/n:") != "n"
    return (from_square, to_square)

  def play_game(self):
    self.board.print_board()
    while True:
      self.turn()



game = Game(Side.WHITE)
game.play_game()
