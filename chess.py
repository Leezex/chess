#----------------------functions-----------------------

def sign(i):
	if i < 0:
		return -1
	elif i > 0:
		return 1
	return 0

#----------------------classes-------------------------

class Piece:
	def __init__(self, colour):
		self.colour = colour

	
class Nothing:
	colour = "Nothing"
	name = "Nothing"
	def show(self):
		print("  ", end = '|')


class Pawn(Piece):
	name = 'p'

	def show(self):
		print(self.colour + self.name, end = '|')

	def legalSquare(self, rowTo, colTo, rowFrom, colFrom):
		dx = rowTo - rowFrom
		dy = colTo - colFrom
		if self.colour == 'W':
			dx *= -1
		if dx == 1 and dy <= 1 and dy >= -1:
			return True
		elif ((rowFrom == 1 and self.colour == 'B') or (rowFrom == 6 and self.colour == 'W')) and dx == 2 and dy == 0:
			return True
		return False


class Rook(Piece):
	name = 'r'
	def show(self):
		print(self.colour + self.name, end = '|')

	def legalSquare(self, rowTo, colTo, rowFrom, colFrom):
		dx = abs(rowTo - rowFrom)
		dy = abs(colTo - colFrom)
		return (dx == 0 and dy != 0) or (dx != 0 and dy == 0) 


class Knight(Piece):
	name = 'k'

	def show(self):
		print(self.colour + self.name, end = '|')

	def legalSquare(self, rowTo, colTo, rowFrom, colFrom):
		dx = abs(rowTo - rowFrom)
		dy = abs(colTo - colFrom)
		return (dy == 2 and dx == 1) or (dy == 2 and dx == 2)

class Bishop(Piece):
	name = 'b'
	
	def show(self):
		print(self.colour + self.name, end = '|')

	def legalSquare(self, rowTo, colTo, rowFrom, colFrom):
		dx = abs(rowTo - rowFrom)
		dy = abs(colTo - colFrom)
		return dy == dx

class Queen(Piece):
	name = 'Q'
	
	def show(self):
		print(self.colour + self.name, end = '|')

	def legalSquare(self, rowTo, colTo, rowFrom, colFrom):
		dx = abs(rowTo - rowFrom)
		dy = abs(colTo - colFrom)
		return (abs(dx) == abs(dy) or (dx == 0 or dy == 0))


class King(Piece):
	name = 'K'

	def show(self):
		print(self.colour + self.name, end = '|')

	def legalSquare(self, rowTo, colTo, rowFrom, colFrom):
		dx = abs(rowTo - rowFrom)
		dy = abs(colTo - colFrom)
		return dx == 1 or dy == 1

class Chess:
	WhiteKing = King('W')
	BlackKing = King('B')
	

	def show(self):
		for i in range(0,8):
			print("-------------------------")
			print('|', end='', flush=True)
			for j in range(0,8):
				self.Board[i][j].show()
			print("")
		print("-------------------------")
		
	def firstRank(self, c):
		if (c == 'W'):
			king = self.WhiteKing
		else:
			king = self.BlackKing
		return [Rook(c), Knight(c), Bishop(c), Queen(c), king, Bishop(c), Knight(c), Rook(c)]

	def pawnRow(self, c):
		return [Pawn(c), Pawn(c), Pawn(c), Pawn(c), Pawn(c), Pawn(c), Pawn(c), Pawn(c)]

	def emptyRow(self):
		return [Nothing(), Nothing(), Nothing(), Nothing(), Nothing(), Nothing(), Nothing(), Nothing()]

	def __init__(self):
		self.Board = [self.firstRank('B'), self.pawnRow('B'), self.emptyRow(), self.emptyRow(), self.emptyRow(), self.emptyRow(), self.pawnRow('W'), self.firstRank('W')]
		self.show()

	def movePiece(self, rowTo, colTo, rowFrom, colFrom):
		piece = self.Board[rowFrom][colFrom]
		if piece.name == 'p' and (rowTo == 0 or rowTo == 7):
			piece = Queen('W')
		self.Board[rowTo][colTo] = piece
		self.Board[rowFrom][colFrom] = Nothing()

	def move(self, rowFrom, colFrom, rowTo, colTo):
		colour = self.Board[rowFrom][colFrom].colour
		if self.legalMove(rowTo, colTo, rowFrom, colFrom) == True:
			piece = self.movePiece(rowTo, colTo, rowFrom, colFrom)
			if self.validBoard(colour):
				self.LastMovedPiece = self.Board[rowTo][colTo]
				self.LastMove = [rowFrom, colFrom, rowTo, colTo]
				self.show()
			else: 
				self.movePiece(rowFrom, colFrom, rowTo, colTo)
				self.Board[rowTo][colTo] = piece
				print("King Checked")
		elif self.legalMove(rowTo, colTo, rowFrom, colFrom) == "AnPassant":
			piece = self.movePiece(rowFrom, colTo, rowFrom, colFrom)
			self.movePiece(rowTo, colTo, rowFrom, colTo)
			if self.validBoard(colour):
				self.LastMovedPiece = self.Board[rowTo][colTo]
				self.LastMove = [rowFrom, colFrom, rowTo, colTo]
				self.show()
			else: 
				self.movePiece(rowFrom, colFrom, rowTo, colTo)
				self.Board[rowFrom][colTo] = piece
				print("King Checked")
					
		else:
			print("Ilegal Move")
	
	def legalMove(self, rowTo, colTo, rowFrom, colFrom):
		piece = self.Board[rowFrom][colFrom]
		square = self.Board[rowTo][colTo]
		if square.colour != piece.colour and piece.name == 'p':
			if piece.legalSquare(rowTo, colTo, rowFrom, colFrom):
				if self.pathChecker(rowTo, colTo, rowFrom, colFrom) and square.colour == "Nothing" and colTo - colFrom == 0:
					return True
				tmp = [rowTo + (rowTo - self.LastMove[2]), colTo , rowFrom, colTo]
				if square.colour != piece.colour and square.colour != "Nothing" and colTo != colFrom:
					return True
				elif (self.LastMovedPiece.name == 'p' and self.LastMove == tmp and self.LastMovedPiece.colour != piece.colour) and square.colour == "Nothing" and colTo != colFrom:
					return "AnPassant"
		elif square.colour != piece.colour and piece.name == 'k':
			return True
		elif square.colour != piece.colour:
			if piece.legalSquare(rowTo, colTo, rowFrom, colFrom):
				if self.pathChecker(rowTo, colTo, rowFrom, colFrom):
					return True
		return False
	
	def pathChecker(self, rowTo, colTo, rowFrom, colFrom):
		dx = rowTo - rowFrom
		dy = colTo - colFrom
		x = sign(dx)
		y = sign(dy)
		for i in range(1, max(abs(dy),abs(dx))):
			print(self.Board[rowFrom + i*x][colFrom + i*y].name)
			if self.Board[rowFrom + i*x][colFrom + i*y].name != "Nothing":
				return False
		return True
				
	def direction(self, i):
		return {
			0: (0,1),
			1: (0,-1),
			2: (1,0),
			3: (-1,0),
			4: (1,1),
			5: (1,-1),
			6: (-1,-1),
			7: (-1,1),
			}[i]
	
	def validBoard(self, colour):
		if (colour == 'W'):
			king = self.WhiteKing
		else:
			king = self.BlackKing
		row, col = self.locateKing(king)
		for i in range(0,8):
			x, y = self.direction(i)
			j = 1
			while(row + j*x < 8 and row + j*x >= 0 and col + j*y < 8 and col + j*y >= 0):
				piece = self.Board[row+j*x][col+j*y]
				if piece.name != "Nothing":
					if i < 4:
						if (piece.name == 'r' or piece.name == 'Q') and piece.colour != colour:
							return False
						else:
							break
					else:
						if (piece.name == 'b' or piece.name == 'Q') and piece.colour != colour:
							return False
						else:
							break
				j += 1
		dir = 1
		if colour == 'W':
			dir = -1
		knightPos = [(1,2), (2,1), (-1,2), (-2,1), (1,-2), (2,-1), (-1,-2), (-2,-1)]
		for i in range(0,8):
			x, y = knightPos[i]
			x += row
			y += col
			if y >= 0 and y < 8 and x >= 0 and x < 8:
				if (self.Board[x][y].name == 'k' and self.Board[x][y].colour != colour):
					return False
		piece1 = self.Board[row+dir][col-1]
		piece2 = self.Board[row+dir][col+1]
		if (piece1.name == 'p' and piece1.colour != colour) or (piece2.name == 'p' and piece2.colour != colour):
			return False
		for i in range(0,8):
			x, y = self.direction(i)
			if col+y >= 0 and col+y < 8 and row+x >= 0 and row+x < 8:
				if self.Board[row+x][col+y].name == 'K' and self.Board[row+x][col+y].colour != colour:
					return False
		return True
		
	def locateKing(self, king):
		for i in range(0,8):
			for j in range(0,8):
				if self.Board[i][j] == king:
					return i, j
	
	def playerMove(self):
		rowFrom = int(input("From row: ")) -1
		colFrom = int(input("From col: ")) -1
		rowTo = int(input("To row: ")) -1
		colTo = int(input("To col: ")) -1
		if self.Board[rowFrom][colFrom].name == "Nothing":
			print("Not a valid piece!")
			return
		if colTo not in range(0,8) or colFrom not in range(0,8) or rowTo not in range(0,8) or rowFrom not in range(0,8):
			print("Bad input!")
			return
		self.move(rowFrom, colFrom, rowTo, colTo)

def main():
	chess = Chess()
	chess.move(1,4,3,4)
	chess.move(3,4,4,4)

	chess.move(6,4,5,4)

	chess.move(7,3,6,4)
	chess.move(0,3,3,6)
	chess.move(3,6,5,4)
	chess.move(5,4,3,6)

	chess.move(6,3,4,3)
	chess.move(4,4,5,3)
	while(1):
		chess.playerMove()	


if __name__ == "__main__":
	main()
