""" Jerry Zheng
    May 28, 2015
    Bomberman: This is a game one players are pitted against eachother and must
    blow eachother up with their bombs. The players must first however use their
    bombs to escape their respective corners and reach the opponents. Along the
    way players will be able to collect powerups to aid them in defeating their
    enemies the game ends when either one or no players are left standing
"""
#Import
import pygame, Sprites, random
pygame.init()

def game():
    '''This function defines the 'mainline logic' for the game. It will return
    variables for if he player wants to exit the game and the number of the game's
    winner'''
    #set a variable for if the player wants to exit the game and one for the game's winner
    exit = False
    winner = False
    
      
    # Display
    pygame.display.set_caption("Bomberman")
    
    # Entities
    #load music and sfx
    screen = pygame.display.set_mode((640, 480))
    pygame.mixer.music.load("Sprites/music/theme.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)    
    explode = pygame.mixer.Sound("Sprites/music/explode.wav")
    explode.set_volume(0.5)
    
    background = pygame.image.load("Sprites/background.gif")
    background = background.convert()
    screen.blit(background, (0, 0))
    
    #creats strings for each player
    controllers =[]
    for player in range(2):
        controllers.append('player'+ str( player + 1 ) +'_')
    kinds = ['lives_', 'bomb_', 'power_', 'speed_', 'kick_']
    
    #this creats a label sprite for each stat of ever player using a nested for loop
    labels = []
    y = [23,50,77,103, 104]
    x = 620
    x_kick = 540
    for player in controllers:
        for kind in kinds:
            if kind != 'kick_' and kind != 'speed_':
                exec player + kind + 'label = Sprites.Label( "1", (x, y[kinds.index(kind)] + 120* controllers.index(player)))'
                exec 'labels.append('+ player + kind + 'label)'
            elif kind == 'speed_':
                exec player + kind + 'label = Sprites.Label( "2", (x, y[kinds.index(kind)] + 120* controllers.index(player)))'
                exec 'labels.append('+ player + kind + 'label)'
            else:
                exec player + kind + 'label = Sprites.Label( "No", (x_kick, y[kinds.index(kind)] + 120* controllers.index(player)))'
                exec 'labels.append('+ player + kind + 'label)'
	    
    HUD = Sprites.HUD()
    
    players =[]
    for player in controllers:
        exec"player"+str(controllers.index(player) +1)+" = Sprites.Player("+str(controllers.index(player) +1)+")"
        exec "players.append(player"+str(controllers.index(player) +1)+")"
    
    #creates the game grid variable for the objects to be placed in
    grid = {}
    for x in range(0,480,32):
        for y in range(0,480,32):
            grid[(str(x) + str(y))] =  'empty'

    # a nested for loop to generate the arena and fill the grid with string variables
    empty_space = (32, 64, 384, 416)
    bricks = []
    walls = []
    for x in range(0,480,32):
        for y in range(0,480,32):
            if (y == 0 or y == 448 or x == 0 or x == 448):
                wall = Sprites.Wall(y,x)
                walls.append(wall)
                grid[(str(x) + str(y))] = "wall"
            elif ((y % 64) == 0) and ((x % 64) == 0):
                wall = Sprites.Wall(y,x)
                walls.append(wall)
                grid[(str(x) + str(y))] = "wall"
            elif (y == 32 and (x in empty_space)) or (y == 416 and (x in empty_space))\
	         or (y == 64 or y == 384) and (x == 32 or x == 416):
                pass
            else:
                brick = Sprites.Brick(y,x)
                bricks.append(brick)
                grid[(str(x) + str(y))] = "brick"
                
    powerup_group = pygame.sprite.Group()
    fire_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group(players)         
    brick_group = pygame.sprite.Group(bricks)
    wall_group = pygame.sprite.Group(walls)
    #a grid group and non grid group to seperate update methods to sprites that need the game grid and others that do not
    grid_group = pygame.sprite.Group(bomb_group, player_group)
    non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
    sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
    
    # Assign 
    clock = pygame.time.Clock()
    keepGoing = True
    
# Loop
    while keepGoing:
        # Time
        clock.tick(30)
     
        # Events
	#check if the fire has blown up a block and has a chance of spawning a powe up
        for fire in fire_group:
            if pygame.sprite.spritecollide(fire, brick_group, True):
                grid[str(fire.rect.left) + str(fire.rect.top)] = 'empty'
                if random.randint(1,5) in [1,2]:
                    pu = Sprites.Power_Up(fire.spawn_pu())
                    powerup_group.add(pu)
                    sprite_group.clear(screen, background)
                    grid_group = pygame.sprite.Group(bomb_group, player_group)
                    sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
		
	# checks if the power up is hit by an explosing and check if the powerup
	#is not invincible before destroying it
        for powerup in powerup_group:
            if pygame.sprite.spritecollide(powerup, fire_group, False) and powerup.get_invincible() == 0:
                powerup.kill()
		
	#checks if a bomb has been hit by the explosion of another and will
	#make that bomb explode if it has been hit
	for bomb in bomb_group:
	    if pygame.sprite.spritecollide(bomb, fire_group, False):
		bomb.quick_explode()
		
	#checks if the player has either been hit by an explosion or has touched a powerup
	for player in player_group:
	    if pygame.sprite.spritecollide(player, fire_group, False):
		player.lose_life()
		exec 'player'+player.get_num()+'_lives_label.set_text("' +player.get_lives()+ '")'
		exec 'player'+player.get_num()+'_lives_label.update()'
		
	    for powerup in powerup_group:
		if player.rect.colliderect(powerup.rect):
		    player.boost(powerup.get_type())
		    exec 'player'+player.get_num()+'_'+powerup.get_type()+'_label.set_text(player.get_'+ powerup.get_type() +'())'
		    exec 'player'+player.get_num()+'_'+powerup.get_type()+'_label.update()'
		    powerup.kill()
	    
				
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
		#set the exit variable true
		exit = True
	    if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player1.move((-1,0), grid, bomb_group)
                if event.key == pygame.K_d:
                    player1.move((1,0), grid, bomb_group)
                if event.key == pygame.K_w:
                    player1.move((0,1), grid, bomb_group)
                if event.key == pygame.K_s:
                    player1.move((0,-1), grid, bomb_group)
                if event.key == pygame.K_SPACE:
                    if player1.can_bomb():
                        x,y,size = player1.bomb()
                        bomb = Sprites.Bomb(x,y,size)
                        bomb_group.add(bomb)
                        sprite_group.clear(screen, background)
                        grid_group = pygame.sprite.Group(bomb_group, player_group)
                        sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
                        grid[(str(x) + str(y))] = "bomb"
                
                if event.key == pygame.K_LEFT:
                    player2.move((-1,0), grid, bomb_group)
                if event.key == pygame.K_RIGHT:
                    player2.move((1,0), grid, bomb_group)
                if event.key == pygame.K_UP:
                    player2.move((0,1), grid, bomb_group)
                if event.key == pygame.K_DOWN:
                    player2.move((0,-1), grid, bomb_group)
                if event.key == pygame.K_KP0:
                    if player2.can_bomb():
                        x,y,size = player2.bomb()
                        bomb = Sprites.Bomb(x,y,size)
                        bomb_group.add(bomb)
                        sprite_group.clear(screen, background)
                        grid_group = pygame.sprite.Group(bomb_group, player_group)
                        sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
                        grid[(str(x) + str(y))] = "bomb"
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player2.move((0,0), grid, bomb_group)
                if event.key == pygame.K_RIGHT:
                    player2.move((0,0), grid, bomb_group)
                if event.key == pygame.K_UP:
                    player2.move((0,0), grid, bomb_group)
                if event.key == pygame.K_DOWN:
                    player2.move((0,0), grid, bomb_group)

                if event.key == pygame.K_a:
                    player1.move((0,0), grid, bomb_group)
                if event.key == pygame.K_d:
                    player1.move((0,0), grid, bomb_group)
                if event.key == pygame.K_w:
                    player1.move((0,0), grid, bomb_group)
                if event.key == pygame.K_s:
                    player1.move((0,0), grid, bomb_group)
            
	
	#this method checks if the bomb's timer is zero and then enerates 
	#fire on each of the 4 sides if the ajacent space is empty in the grid.
	#fire will not spawn if it hits a wall and the fire will stop spawning
	#in a certain direction after hitting one brick
        for bomb in bomb_group:
	    if bomb.get_time() == 0:	
		#will round the x and y co-ordinates if the bomb explodes while it is still
		#moving
		if bomb.get_time() == 0:
		    if bomb.rect.left % 32 < 17:
			bomb.rect.left = bomb.rect.left - (bomb.rect.left % 32)
		    else:
			bomb.rect.left = bomb.rect.left + (32 - bomb.rect.left % 32)
		    
		    if bomb.rect.top % 32 < 17:
			bomb.rect.top = (bomb.rect.top - (bomb.rect.top % 32))
		    else:
			bomb.rect.top = (bomb.rect.top + (32 - bomb.rect.top % 32))			
		boom = Sprites.Fire(bomb.rect.centerx, bomb.rect.centery, "center")
		explode.play()
		fire_group.add(boom)
		length_top = bomb.rect.centery
		length_bottom = bomb.rect.centery
		length_left = bomb.rect.centerx
		length_right = bomb.rect.centerx
		
		for side in ['left', 'right', 'top', 'bottom']:
		    for length in range(bomb.get_power()):
			if side == 'left':
			    length_left -= 32
			    if grid[str(length_left -16) + str(bomb.rect.centery - 16)] ==  'empty' or grid[str(length_left -16) + str(bomb.rect.top)] ==  "bomb" :
			        if length == bomb.get_power() -1:
			            boom = Sprites.Fire(length_left, bomb.rect.centery, 'far_left')
			            fire_group.add(boom)
				    sprite_group.clear(screen, background)
				    non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
				    sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
			        else:
			            boom = Sprites.Fire(length_left, bomb.rect.centery, 'left')
			            fire_group.add(boom)
				    sprite_group.clear(screen, background)
				    non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
			            sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
			    elif grid[str(length_left -16) + str(bomb.rect.centery - 16)] ==  "brick":
				boom = Sprites.Fire(length_left, bomb.rect.centery, 'far_left')
				fire_group.add(boom)
				sprite_group.clear(screen, background)
				non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
				sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
				break
			    elif grid[str(length_left -16) + str(bomb.rect.centery - 16)] ==  "wall":
				break
			    
			elif side == 'top':
			    length_top -= 32
			    if grid[str(bomb.rect.centerx - 16) + str(length_top - 16)] ==  'empty' or grid[(str(bomb.rect.left) + str(length_top -16))] ==  "bomb" :
				if length == bomb.get_power() -1:
				    boom = Sprites.Fire(bomb.rect.centerx, length_top, 'far_top')
				    fire_group.add(boom)
				    sprite_group.clear(screen, background)
				    non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
				    sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
				else:
				    boom = Sprites.Fire(bomb.rect.centerx, length_top, 'top')
				    fire_group.add(boom)
				    sprite_group.clear(screen, background)
				    non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
				    sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
			    elif grid[str(bomb.rect.centerx - 16) + str(length_top - 16)] ==  'brick':
				boom = Sprites.Fire(bomb.rect.centerx, length_top, 'far_top')
				fire_group.add(boom)
				non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
				sprite_group.clear(screen, background)
				non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
				sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
				break
			    elif grid[str(bomb.rect.centerx - 16) + str(length_top - 16)] ==  'wall':
				break
			    
			elif side == 'right':
			    length_right += 32
			    if grid[str(length_right -16) + str(bomb.rect.centery - 16)] ==  'empty' or grid[str(length_right -16) + str(bomb.rect.top)] ==  "bomb" :
				if length == bomb.get_power() -1:
				    boom = Sprites.Fire(length_right, bomb.rect.centery, 'far_right')
				    fire_group.add(boom)
				    sprite_group.clear(screen, background)
				    non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
				    sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
				else:
				    boom = Sprites.Fire(length_right, bomb.rect.centery, 'right')
				    fire_group.add(boom)
				    sprite_group.clear(screen, background)
				    non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
				    sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
			    elif grid[str(length_right -16) + str(bomb.rect.centery - 16)] ==  'brick':
				boom = Sprites.Fire(length_right, bomb.rect.centery, 'far_right')
				fire_group.add(boom)
				sprite_group.clear(screen, background)
				non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
				sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
				break
			    elif grid[str(length_right -16) + str(bomb.rect.centery - 16)] ==  'wall':
				break
			    
			elif side == 'bottom':
			    length_bottom += 32
			    if grid[str(bomb.rect.centerx - 16) + str(length_bottom - 16)] ==  'empty' or grid[(str(bomb.rect.left) + str(length_bottom - 16))] ==  "bomb" :
				if length == bomb.get_power() -1:
				    boom = Sprites.Fire(bomb.rect.centerx, length_bottom, 'far_bottom')
				    fire_group.add(boom)
				    sprite_group.clear(screen, background)
				    non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
				    sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
				else:
				    boom = Sprites.Fire(bomb.rect.centerx, length_bottom, 'bottom')
				    fire_group.add(boom)
				    sprite_group.clear(screen, background)
				    non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
				    sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
			    elif grid[str(bomb.rect.centerx - 16) + str(length_bottom - 16)] ==  'brick':
				boom = Sprites.Fire(bomb.rect.centerx, length_bottom, 'far_bottom')
				fire_group.add(boom)
				sprite_group.clear(screen, background)
				non_grid_group = pygame.sprite.OrderedUpdates(labels, fire_group, powerup_group)
				sprite_group = pygame.sprite.OrderedUpdates(HUD, labels, bomb_group, fire_group, player_group, brick_group, wall_group, powerup_group)
				break
			    elif grid[str(bomb.rect.centerx - 16) + str(length_bottom - 16)] ==  'wall':
				break
		                    
	#checks if no one is currently dying
	for player in player_group:
	    if player.get_dying():
		end = False
		break
	#checks if there is a winner and if no one is currently dying it sets a
	#winner variable based on the last player standing and ends the game loop
	if len(player_group) == 1 and end == True:
	    for player in player_group:
		winner = player.get_num()
		keepGoing = False
	elif len(player_group) == 0 and end == True:
	    winner = '0'
	    keepGoing = False
	#reset the end checking variable for the next frame
	end = True
        # Refresh screen
        sprite_group.clear(screen, background)
	
        grid_group.update(grid)
	non_grid_group.update()
	
        sprite_group.draw(screen)
     
        pygame.display.flip()
     
    # Close the game window
    return exit, winner
    

def main():
    """The function that runs the other functions in a loop until the player
    exits the game by clicking the x on the game window"""
    #set an exit variable for then the player wants to close the game
    exit = False
    pygame.display.set_caption("Bomberman")
    while exit == False:
	if exit == False:
	    exit = start_screen()
	if exit == False:
	    exit, winner = game()
	if exit == False:
	    exit = end_screen(winner)
	    
    pygame.quit()  
    
def start_screen():
    """The function that displays the starting instruction screen
    it will return a variable for whether if the player closes the game"""
    # an exit variable that will tell the game to move to the next screen or close
    exit = False

 
    # Display
    
    # Entities
    screen = pygame.display.set_mode((640, 480))
    #Music
    pygame.mixer.music.load("Sprites/music/title.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    start = pygame.mixer.Sound("Sprites/music/game_start.wav")
    start.set_volume(0.5)    
    
    #instruction labels
    instructions1 = Sprites.Label("To start the game insert 2-4 controllers", ((320,330)))
    instructions2 = Sprites.Label("Press Enter", ((320, 350)))
    instructions3 = Sprites.Label("To move your character use wasd or the d-pad", ((320, 180)))
    instructions4 = Sprites.Label("To place a bomb press The space bar or 0",((320,200)))
    instructions5 = Sprites.Label("bomb-up    explosion-up   speed-up   kick-bombs   1-up", ((320, 240)))
    
    allSprites = pygame.sprite.Group(instructions1, instructions2, instructions3, instructions4, instructions5)
    #images
    background = pygame.image.load("Sprites/start_screen.gif")
    background = background.convert()
    screen.blit(background, (0, 0))
    x =[85, 210, 340, 455, 552]
    for boost in ['bomb', 'power', 'speed', 'kick', '1-up']:
	image = pygame.image.load('Sprites/pu/pu '+boost+'.gif')
	image = image.convert()
	screen.blit(image, (x[['bomb', 'power', 'speed', 'kick', '1-up'].index(boost)], 255))
	            
    # Assign 
    clock = pygame.time.Clock()
    keepGoing = True
    
    # Loop
    while keepGoing:
        # Time
        clock.tick(30)
	
	for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
		#set the exit variable true
		exit = True
            elif event.type == pygame.KEYDOWN:
		if event.key == pygame.K_RETURN:
		    keepGoing = False	   
		    
	# Refresh screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
         
        pygame.display.flip()
	
    #returns the exit variable
    if exit == False:
	start.play()
	pygame.mixer.music.fadeout(1000)
	pygame.time.delay(1000)
    return exit

def end_screen(number):
    """The function that recives the number of the winner as a parameter
    and displays the winner. Then it will return the value that determines 
    if the game will close when the player hits start"""
    # an exit variable that will tell the game to move to the next screen or close
    exit = False
    
     
	
    # Display
    
    # Entities
    screen = pygame.display.set_mode((640, 480))    
    
    #sets the image of the winner and the music that will play
    if number == '0':
	pygame.mixer.music.load("Sprites/music/lose.mp3")
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play(1)
	sound = pygame.mixer.Sound("Sprites/music/draw.wav")
	sound.set_volume(0.5)
	sound.play()		
	instructions2 = Sprites.Label("THE BOMB!", ((320, 260)))
	image = pygame.image.load("Sprites/bombs/bomb3.gif")
    else:
	sound = pygame.mixer.Sound("Sprites/music/winner.wav")
	sound.set_volume(0.5)
	sound.play()
	pygame.time.delay(1000)
	pygame.mixer.music.load("Sprites/music/victory.mp3")
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play(1)
	instructions2 = Sprites.Label("PLAYER"+number+"!", ((320, 260)))
	image = pygame.image.load("Sprites/players/"+number+"_down_2.gif")	
	
    background = pygame.image.load("Sprites/Game_Over.gif")
    instructions1 = Sprites.Label("And the Winner is", ((320,240)))
    replay = Sprites.Label("Press start to play again", ((320, 400)))
    image.set_colorkey((255,255,255))
    background.set_colorkey((0,0,0))
    allSprites = pygame.sprite.Group(instructions1, instructions2, replay)

    screen.blit(background, (0, 0))
    screen.blit(image, ((310, 350)))

    
    # Assign 
    clock = pygame.time.Clock()
    keepGoing = True
    
    # Loop
    while keepGoing:
	# Time
	clock.tick(30)
	
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		keepGoing = False
		#set the exit variable true
		exit = True
	    elif event.type == pygame.KEYDOWN:
		if event.key == pygame.K_RETURN:
		    keepGoing = False
	# Refresh screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
         
        pygame.display.flip()
    return exit

main()
