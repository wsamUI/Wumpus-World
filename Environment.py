import random

class Environment:
	"The environment grid"
	
	def __init__(self, 
				width, 
				height, 
				pitProb,
				allowClimbWithoutGold,
				agent,
				terminated,
				wumpusAlive,):
		self.width = width
		self.height = height
		self.pitProb = pitProb
		self.allowClimbWithoutGold = allowClimbWithoutGold
		self.agent = agent
		self.pitLocations = []
		self.gameTerminated = terminated
		self.wumpusLocation = []
		self.wumpusAlive = wumpusAlive
		self.goldLocation = []
		self.actionCount = 0
		self.initalizeAndGenerate()
		
		
	#used to create the 2D loop, set the wumpusLocation and goldLocation
	#and setting the pits with specified random value (0.20)
	#pass on the width and height to the agent
	def initalizeAndGenerate(self):
		#initializing grid
		self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
		
		self.my_custom_random(self.wumpusLocation, self.width, self.height)
		self.my_custom_random(self.goldLocation, self.width, self.height)
		
		for index, item in enumerate(self.grid):
			for index2, item2 in enumerate(item):
				prob = random.random()
				#print("prob: ", prob, " [", index, ",", index2, "]")
				if ((prob <= self.pitProb) and (index != 0 and index2 != 0)):
					self.pitLocations.append([index,index2])
		
		self.agent.setWidthHeight(self.width, self.height)
		
		
	#needed to create a custom random function to exclude [0,0]
	#and exclude from an array value, appends the value to the
	#passed array as well
	def my_custom_random(self, excludeArray, width, height):
		x_rand = random.randint(0,width-1)
		y_rand = random.randint(0,height-1)
		#print(excludeArray) #delete
		#print("{", x_rand, ",", y_rand, "}")
		if (x_rand == 0 and y_rand == 0):
			return self.my_custom_random(excludeArray, width, height)
		elif ([x_rand,y_rand] in excludeArray):
			return self.my_custom_random(excludeArray, width, height)
		else:
			excludeArray.append([x_rand,y_rand])
			
			
	#update the grid, setting the pits, gold, wumpus locations on the grid
	#also updates the breeze and stench locations
	#this function is called everytime Vizualize is called, perhaps not
	#the most efficient way to use this function, but at the moment it works
	def updateGrid(self):
		for index, item in enumerate(self.grid):
			for index2, item2 in enumerate(item):
				text = ""
				if ([index, index2] in self.pitLocations):
					text = text + "P"
				if ([index, index2] in self.wumpusLocation):
					if (self.wumpusAlive):
						text = text + "W"
					else:
						text = text + "w"
				if ([index, index2] in self.goldLocation):
					text = text + "G"
					#text = text + "g" #glitter
				if ([index, index2] == self.agent.coords):
					text = text + "A"
				#print("text: ", text, " index: [", index, ",", index2, "]")
				self.grid[index][index2] = text
				if(([min(self.height-1,index + 1), index2] in self.pitLocations) or
					([max(0,index - 1), index2] in self.pitLocations) or
					([index, min(self.width-1, index2 + 1)] in self.pitLocations) or
					([index, max(0,index2 - 1)] in self.pitLocations)):
						if ("P" not in self.grid[index][index2]):
							self.grid[index][index2] = self.grid[index][index2] + "b"
				if(([min(self.height-1,index + 1), index2] in self.wumpusLocation) or
					([max(0,index - 1), index2] in self.wumpusLocation) or
					([index, min(self.width-1, index2 + 1)] in self.wumpusLocation) or
					([index, max(0,index2 - 1)] in self.wumpusLocation)):
						if (("W" not in self.grid[index][index2]) or ("w" not in self.grid[index][index2])):
							self.grid[index][index2] = self.grid[index][index2] + "s"
				
				
	#vizualize, prints out the grid, also calls the updateGrid() function everytime
	#also prints out the general information for each value state
	#also prints out game loop, its nice to look at
	def visualize(self):
		self.updateGrid()
		temp = self.grid.copy()
		temp.reverse()

		for index, item in enumerate(temp):
			print()
			for index2, item2 in enumerate(item):
				print("[",item2,"]", end="")
		print()
		print("Agent Location: ", self.agent.coords, " Direction: ", self.agent.direction)
		print("Agent has Gold: ", self.agent.hasGold)
		print("Agent hasArrow: ", self.agent.hasArrow)
		print("Agent isAlive: ", self.agent.isAlive)
		print("Wumpus Location: ", self.wumpusLocation)
		print("wumpusAlive: ", self.wumpusAlive)
		print("Gold Location: ", self.goldLocation)
		print("Pit Locations: ", self.pitLocations)
		print("Pit Prob: ", self.pitProb)
		print("AllowClimbWithoutGold: ", self.allowClimbWithoutGold)
		print("gameTerminated: ", self.gameTerminated)
		print("Action Count (Game loop): ", self.actionCount)
		print()
		print("-------------Visualize-------------")
		print()
		
		
	#all the actions are calculated here, for each action 1-6
	#all the required states are changed here, including printing
	#at the end of the function we are calling Vizualize to print
	#will need to consider how to combine with the Percepts for A2
	def action(self, action):
		self.actionCount += 1
		# forward = 1
		if (action == 1):
			self.agent.forward()
			print("Action(1): Move Forward")
			if (self.agent.coords in self.wumpusLocation):
				if (self.wumpusAlive):
					self.agent.isAlive = False
					self.gameTerminated = True #game over
					print("You've been eaten by the Wumpus!!!")
			elif (self.agent.coords in self.pitLocations):
				self.agent.isAlive = False
				self.gameTerminated = True #game over
				print("You fell into a pit!!!")
			
		# turnLeft = 2
		elif (action == 2):
			self.agent.turnLeft()
			print("Action(2): Turn Left")
			
		# turnRight = 3
		elif (action == 3):
			self.agent.turnRight()
			print("Action(3): Turn Right")
			
		# grab, if Gold in same room = 4
		elif (action == 4):
			print("Action(4): Grab")
			if (self.agent.hasGold == True):
				return
			if (self.agent.coords in self.goldLocation):
				self.agent.hasGold = True
				self.goldLocation.clear() #might need to delete later
				
		# shoot = 5
		elif (action == 5):
			print("Action(5): Shoot -> ", self.agent.direction)
			if (self.agent.hasArrow == False):
				return
			self.agent.hasArrow = False
			if (self.agent.direction == "EAST"):
				x = min(self.width - 1, self.agent.coords[1] + 1)
				if ([self.agent.coords[0], x] in self.wumpusLocation):
					self.wumpusAlive = False
					print("SCREEEEEEAAAAAAAAMMMMMMMM!!!!!!")
					print("Arrow shot and hit something!!!!")
			elif (self.agent.direction == "WEST"):
				x = max(0, self.agent.coords[1] - 1)
				if ([self.agent.coords[0], x] in self.wumpusLocation):
					self.wumpusAlive = False
					print("SCREEEEEEAAAAAAAAMMMMMMMM!!!!!!")
					print("Arrow shot and hit something!!!!")
			elif (self.agent.direction == "NORTH"):
				y = min(self.height - 1, self.agent.coords[0] + 1)
				if ([y, self.agent.coords[1]] in self.wumpusLocation):
					self.wumpusAlive = False
					print("SCREEEEEEAAAAAAAAMMMMMMMM!!!!!!")
					print("Arrow shot and hit something!!!!")
			elif (self.agent.direction == "SOUTH"):
				y = max(0, self.agent.coords[0] - 1)
				if ([y, self.agent.coords[1]] in self.wumpusLocation):
					self.wumpusAlive = False
					print("SCREEEEEEAAAAAAAAMMMMMMMM!!!!!!")
					print("Arrow shot and hit something!!!!")
			else:
				print ("Arrow shot and missed.")
			
		# climb, with Gold, on [0,0] = 6
		elif (action == 6):
			print("Action(6): Climb with Gold")
			if ((self.agent.coords == [0,0]) and (self.agent.hasGold == True)):
				self.gameTerminated = True #game over
				print("YOU WIN!!!!")
		#call vizualize
		self.visualize()
		
