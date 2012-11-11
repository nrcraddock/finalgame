#combat engine for final game project
#Notice that on first build/debug I was getting a lot of errors 
#because of asinine mistakes:
#capitalization and pluralization differences, etc.
#Make sure to be incredibly careful when doing this.
#STILL NEEDS FIXED: you can only engage an enemy when in the tile
#to the right of them.
#TODO: Add job classes, magic, a discernable plot, goal progression.
#Also, could I make rooms that aren't square/rectangular?


from random import randint,random
from time import sleep
from sys import exit

class character(object):
	"""This is the main PC, named after whatever 
	you enter upon beginning the game."""
	def __init__(self, name, health, strength, vitality):
		self.name = name
		self.health = health
		self.strength = strength
		self.vitality = vitality
		#self.magic = magic commented out the stats for later use
		#self.spirit = spirit
		#self.evade = evade
		#self.speed = speed
		self.x = -1
		self.y = -1

	def navigate(self,x,y,room):
		if x<0 or y<0:
			raise IndexError
		"""navigate through or to any given coordinate in any room"""
		if room.cells[y][x] == ' ':
			try:
				room.cells[self.y][self.x] = ' '
			except IndexError:
				pass
			self.x = x
			self.y = y
			self.room = room
			room.cells[y][x] = self
			for cell in room.adjacent_cells(x,y):
				if str(type(cell)) == "<class '__main__.monster'>":
					self.room.show()
					fight = battle(self,cell,"You confront the {opponent}!")
					fight = fight.fight()
					if fight == "win":
						room.cells[cell.y][cell.x] = ' '
					if fight == "loss":
						print "You got hurt and collapsed. Game over, man!"
						exit(0)
				return "success"
			else:
				return "fail"


class room(object):
    """mostly a list of cells with strings, monsters or your character in it"""
    def __init__(self,width,height,monsters):
        self.width = width
        self.height = height
        self.monsters = monsters
        self.cells = []
        for y in range(self.height):
            self.cells.append([])
            for x in range(self.width):
                self.cells[y].append(' ')
        for monster in monsters:
            self.cells[monster.y][monster.x] = monster
                
                
    def adjacent_cells(self,x,y):
        adj_cells = []
        if x == self.width-1:
            offsetx = range(-1,1)
        elif x == 0:
            offsetx = range(0,2)
        else:
            offsetx = range(-1,2)
        if y == self.height-1:
            offsety = range(-1,1)
        elif y == 0:
            offsety = range(0,2)
        else:
            offsety = range(-1,2)
        for dx in offsetx:
            for dy in offsety:
                if not dy == dx:
                    adj_cells.append(self.cells[y+dy][x+dx])

        return adj_cells
        
    def enter(self,player,x,y):
        self.player = player
        self.player.x = x
        self.player.y = y
        self.cells[y][x] = player
        
    def addmonsters(self,monsters):
        for monster in monsters:
            self.cells[monster.y][monster.x] = monster
    
    def addplayer(self,player):
        if self.cells[player.y][player.x] != ' ':
            self.cells[player.y][player.x] = player
        else:
            return "error"


    def show(self):
        """shows the room in the CLI
        player is a tuple of coordinates
        opponents is a list of tuples with coordinates
        """
        for line in self.cells:
            for cell in line:
                if str(type(cell)) == "<class '__main__.monster'>":
                    print "[x]",
                elif str(type(cell)) == "<class '__main__.character'>":
                    print "[o]",
                else:
                    print "[ ]",
            print "\n"
                
                
        

class battle(object):
	def __init__(self, player, opponent, reason):
		print reason.format(opponent = opponent.type)
		self.player = player
		self.opponent = opponent
		action = raw_input("What do you do next?\n\t1. fight!\n\t2. flee!\n\t3. negotiate!\n> ") #NB: Flee and Negotiate don't work at the moment. They need to be added right under the first if statement down here.
		if "ight" in action or "1" in action:
			print "\nBring it on!\n"
			sleep(1)
			
	def fight(self):
		while self.player.health > 0 and self.opponent.health > 0:
		#NB: This is a stopgap hit/miss calc. TODO: update and improve math to use SPD and EVA in calcs.
		#Also, TODO: Include prompt and functions to use magic.
		#Also, TODO: Make it easier to hit each other, sheesh!
		#Also, TODO: Make it so you can command the battle OR autobattle. That means programming some AI.
			playeroption = randint(1, 6)
			monsteroption = randint(1, 3)
			nodamage = False
			if playeroption >= 2:
				print "{} attacks!".format(self.player.name)
				rndp = random()
				playerdamage = int(((float(self.player.strength)/float(self.opponent.vitality))*100)*rndp)
				self.opponent.health -= playerdamage
			elif playeroption == 1:
				print "{} dodges quickly!".format(self.player.name)
				nodamage = True
				
			sleep(1)
			
			if monsteroption >=2:
				print "{} attacks!".format(self.opponent.type)
				rndm = random()
				monsterdamage = int(((float(self.opponent.strength)/float(self.player.vitality))*100)*rndm)
				self.player.health -= monsterdamage
				
			elif monsteroption == 1:
				print "{} dodges!".format(self.opponent.type)
				if playeroption >= 2:
					self.opponent.health += playerdamage
			if nodamage == True and monsteroption >= 2:
				self.player.health += monsterdamage
				
			sleep(1)
			
			if playeroption >= 2 and monsteroption >= 2:
				print "\t{player} damages the {monster} for {damage}!".format(
				            player = self.player.name, monster = self.opponent.type, 
				            damage = playerdamage)
				print "\t{monster} damages {player} for {damage}!".format(
				            monster = self.opponent.type, player = self.player.name, 
				            damage = monsterdamage)
				print "\t\t\t\t{player} {phealth} || {mhealth} {monster}".format(
				            player = self.player.name, phealth = self.player.health, 
				            mhealth = self.opponent.health, 
				            monster = self.opponent.type)
				
			elif monsteroption == 1 and playeroption >= 2:
				print "{player} misses!".format(player = self.player.name)
				
			elif monsteroption >= 2 and playeroption == 1:
				print "{monster} misses!".format(monster = self.opponent.type)
			
			else:
				print "Both miss!"
			
			print "\n------------\n"
			sleep(2)
			
		if self.player.health <= 0:
			return "loss"
		else:
			return "win"

class monster(object):
    """both for fights and rooms"""
    def __init__(self,x,y,room,mtype,strength,vitality,health):
        #check if coords are taken
        allowed = True
        for monster in room.monsters:
            if (x,y) == (monster.x,monster.y):
                allowed = False
                break
            else:
                allowed = True
        if allowed == True:
            self.x = x
            self.y = y
            self.room = room
            self.type = mtype
            self.strength = strength
            self.vitality = vitality
            self.health = health
        else:
            print "monster crashed"
            del self

			
#Start the game.
print "\nWhat is your name, traveler?\n"
name = raw_input("> ")

print "\nAnd what is your profession?\n" #give options for job classes!
job = raw_input("> ")

#TODO: change this to set these variables penchant upon a job class.
strength = randint(30, 70)
vitality = 100-strength
health = (vitality * 30)

print "\nLet's size you up.\n"
print "\nYour strength is {}; your vitality is {}, and your health is {}.\n".format(strength, vitality, health)
player = character(name, health, strength, vitality)

newb_room = room(10, 10, [])

startmonsters = [] #sets up a dict full of monsters for this instance.
for x in range(5): #you can put a randint in the range() portion to randomize the number of monsters present.
	startmonsters.append(monster(randint(0, newb_room.width-1), randint(0, newb_room.height-1), newb_room, "Muttshroom", 50, 25, 400))
for x in range(2):
	startmonsters.append(monster(randint(0, newb_room.width - 1), randint(0, newb_room.height - 1), newb_room, "Tripper", 100, 25, 500))
startmonsters.append(monster(randint(0, newb_room.width-1), randint(0, newb_room.height-1), newb_room, "Rave Wraith!", 135, 40, 1000))
newb_room.addmonsters(startmonsters)
newb_room.show()

print "The discotheque is shrouded in dry ice fog and your head is pounding. The wubs dropped an hour ago and haven't let up!"
print "You've got to make it out with your sanity!"
print "An X means a ravegoing mob. If you're next to one, you'll have to fight your way out!"
print "Where were you dancing when the madness began?"

coordinates = raw_input("(x, y)> ")
x, y = coordinates.strip('()').split(',')
x = int(x) - 1
y = 10 - int(y)
while player.navigate(int(x), int(y), newb_room) == "fail":
	print "You can't get over there!"
	coordinates = raw_input("(x, y)> ")
	x, y = coordinates.strip('()').split(',')
	x = int(x) - 1
	y = int(y) - 1
newb_room.show()

#The beginning ends here; the repetitive part starts as follows:

print "If you don't take care of the ravegoers they might follow you out! Best take care of them."
print "\nEnter any sequence of WASD keys to move. For example: SD-<RETURN> should move you down once and then to the right once."

while True:

	seq = raw_input("> ")
	for letter in seq:
		try: #I know the X and Y axes are backwards but it works.
			if letter == "W" or letter == "w":
				player.navigate(player.x, player.y-1, newb_room)
			if letter == "A" or letter == "a":
				player.navigate(player.x-1, player.y, newb_room)
			if letter == "S" or letter == "s":
				player.navigate(player.x, player.y+1, newb_room)
			if letter == "D" or letter == "d":
				player.navigate(player.x+1, player.y, newb_room)
		except IndexError:
			newb_room.show()
			print "You got stuck and didn't make it out with your sanity in tact!"
			print "The wubs have you."
			exit(0)
	newb_room.show()
	anymonsters = False
	for line in newb_room.cells: #Checks to see if there are any mobs remaining.
		for cell in line:
			if str(type(cell)) == "<class '__main__.monster'>":
				anymonsters = True
	if anymonsters == False:
		print "\nYou dispatched all of the ravers!"
		print "\nGet out while you still can!"
	print "\nEnter any sequence of WASD keys to move."