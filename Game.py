from puzzle import *

#Game GUI Classes
class GamePlay() :
	def __init__(self,puzzleCode) :
		self.closeGame = False
		self.puzzle_Code	= puzzleCode
		self.change		= True
		self.blockInfo	= []
		self.zeroBlock	= None
		self.row_size	= int((self.puzzle_Code+1)**0.5)
		self.game = Game(self.puzzle_Code)
		self.lastMove   = None
		self.hint = -1

	def mainLoop(self) :
		while not self.closeGame:
			print(self.game.oldMoves)
			key_pressed = input("INPUT H FOR HINT Q FOR QUIT FOR RESET")
			if self.change:
				self.blockInfo = []
				self.draw()
				self.change = False
			if key_pressed == "Q": self.closeGame = True
			elif key_pressed == "R":
				self.game.reset_game()
				self.hint=-1
				self.change = True
			elif key_pressed == "H":
				#print(self.game.nextHint())
				self.hint,score = self.game.nextHint(self.lastMove)
				if self.hint != -1:
					self.change = True
				else:
					print("No moves available!!!")

	def draw(self) :
		print(self.game.oldMoves)
		print("hi")
		for i in range(self.row_size):
			for j in range(self.row_size):
				if self.game.blocks[(j,i)].number!=0 :
					if self.game.blocks[(j,i)].number==self.hint:
						print(self.hint)
					print(self.game.blocks[(j,i)].number)
					if self.game.win :
						print("You Win!!!")
					self.blockInfo.append((self.game.blocks[(j,i)],self.game.blocks[(j,i)].number))
				else :
					self.zeroBlock = self.game.blocks[(j,i)]


	# def mouseCall(self,event,posx,posy,flag,param) :
	# 	if event == cv2.EVENT_LBUTTONDOWN :
	# 		block,number = self.getBlock(posx,posy)
	# 		if block is not None or number!=-1 :
	# 			if block in (self.zeroBlock.up,self.zeroBlock.down,self.zeroBlock.left,self.zeroBlock.right) :
	# 				self.game.swapBlocks(self.zeroBlock,block)
	# 				self.lastMove = self.zeroBlock
	# 				self.change = True

	# def getBlock(self,posx,posy) :
	# 	for i in self.blockInfo :
	# 		if i[2][0]<=posx<=i[3][0] and i[2][1]<=posy<=i[3][1] :
	# 			return (i[0],i[1])
		return None,-1


#Main Program + Main Menu Creation
#Function Definition
# def buttonPress(event,posx,posy,flag,param) :
# 	global difficulty
# 	if event == cv2.EVENT_LBUTTONDOWN :
# 		if width/2-50<=posx<=width/2+50 and height/2-100<=posy<=height/2-50 :
# 			difficulty=0
# 		elif (width/2)-50<=posx<=(width/2)+50 and (height/2)+50<=posy<=(height/2)+100 :
# 			difficulty=1


#Main Program
mainMenuButton = []
difficulty = 1
while True :
	if   difficulty == 0 :
		game8 = GamePlay(8)
		game8.mainLoop()
		difficulty = -1
	elif difficulty == 1 :
		game8 = GamePlay(15)
		game8.mainLoop()
		difficulty = -1
