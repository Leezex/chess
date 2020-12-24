rows = range(1,9)
cols = ['A','B','C','D','E','F','G','H']
positions = []
for row in range(1,9):
	tmp = []
	for col in cols:
		tmp.append(col + str(row))
	positions.append(tmp)

class Chess:
	WhitePieces = []
	BlackPieces = []
	def __init__(self):
		self.WhitePieces = [Rook('W',"A8"), Knight('W', "B8"), Bishop('W', "C8"), Queen('W', "D8"), King('W', "E8"), Bishop('W', "F8"), Knight('W', "G8"), Rook('W',"H8")]		
		self.BlackPieces = [Rook('B',"A1"), Knight('B', "B1"), Bishop('B', "C1"), Queen('B', "D1"), King('B', "E1"), Bishop('B', "F1"), Knight('B', "G1"), Rook('B',"H1")]		
		for pos in positions[6]:
			self.WhitePieces.append(Pawn('W', pos))
		for pos in positions[1]:
			self.BlackPieces.append(Pawn('B', pos))
	
	def show(self):
		Board = [[None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
		for piece in self.WhitePieces + self.BlackPieces:
			row, col = piece.indexOfPos()
			Board[row][col] = piece.show()	
		for i in range(0,8):
			print("-------------------------")
			print('|', end='', flush=True)
			for j in range(0,8):
				if Board[i][j] == None:
					print("  ", end = '|')
				else:
					print(Board[i][j], end = '|')
			print("")
		print("-------------------------")

class Piece:
	Name = None
	Moves = [[]]
	dirs = []
	pos = None

	def update(self):
		self.Moves = []
		for dir in self.dirs:
			tmp = []
			square = self.indexOfPos()
			while(square[0] in range(0,8) and square[1] in range(0,8)): 
				pos = positions[square[0]][square[1]]
				square = self.addDir(square, dir)
				tmp.append(pos)
			self.Moves.append(tmp)

	def __init__(self, colour, pos):
		self.pos = pos
		self.Colour = colour
		self.dirs()
		self.update()
	
	def addDir(self,d1,d2):
		return d1[0] + d2[0], d1[1] + d2[1]

	def indexOfPos(self):
		for i in range(0,8):
			for j in range(0,8):
				if self.pos == positions[i][j]:
					return i, j
		return -1, -1
	
	def show(self):
		return self.Colour + self.Name	

class Rook(Piece):
	Name = "r"
	def dirs(self):
		self.dirs = [(1,0),(0,1),(-1,0),(0,-1)] 

class Bishop(Piece):
	Name = "b"
	def dirs(self):
		self.dirs = [(1,1),(1,-1),(-1,1),(-1,-1)]

class Queen(Piece):
	Name = "Q"
	def dirs(self):
		self.dirs = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

class King(Piece):
	Name = "K"
	def dirs(self):
		self.dirs = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

	def update(self):
		self.Moves = []
		for dir in self.dirs:
			tmp = []
			square = self.addDir(self.indexOfPos(), dir)
			if square[0] in range(0,8) and square[1] in range(0,8):
				tmp.append(positions[square[0]][square[1]])
				self.Moves.append(tmp)

class Pawn(Piece):
	Name = "p"
	def dirs(self):
		if self.Colour == 'B':
			self.dirs = [(1,0),(1,1),(1,-1)]
			if self.pos in positions[1]:
				self.dirs.append((2,0))
		else:
			self.dirs = [(-1,0),(-1,1),(-1,-1)]
			if self.pos in positions[6]:
				self.dirs.append((-2,0))

	def update(self):
		self.Moves = []
		for dir in self.dirs:
			tmp = []
			square = self.addDir(self.indexOfPos(), dir)
			if square[0] in range(0,8) and square[1] in range(0,8):
				if dir == (2,0) or dir == (-2,0):
					self.Moves[0].append(positions[square[0]][square[1]])
				else:
					tmp.append(positions[square[0]][square[1]])
					self.Moves.append(tmp)

class Knight(Piece):
	Name = "k"
	def dirs(self):
		self.dirs = [(2,1),(1,2),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]

	def update(self):
		self.Moves = []
		for dir in self.dirs:
			tmp = []
			square = self.addDir(self.indexOfPos(), dir)
			if square[0] in range(0,8) and square[1] in range(0,8):
				tmp.append(positions[square[0]][square[1]])
				self.Moves.append(tmp)

def main():
	a = Chess()
	a.show()
	

if __name__ == "__main__":
	main()
