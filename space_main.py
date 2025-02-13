import pgzrun
import os
import random
import time
from pgzero.actor import Actor
from pgzero.builtins import keyboard
from pgzero.keyboard import keys
#SETTINGS

# Load background music

background_music = sounds.background_music.play(loops=-1,maxtime=0)

# Screen settings*
WIDTH = 1200
HEIGHT = 700
os.environ["SDL_VIDEO_CENTERED"] = "1"
TITLE = "Heighliner"

# Background color
background_color = (48, 25, 52)

# Buttons: 
button_play_rect = Rect((WIDTH // 2 - 100, HEIGHT // 3 - 30), (200, 60))  
button_sound_rect = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 30), (200, 60))  
button_quit_rect = Rect((WIDTH // 2 - 100, HEIGHT // 1.5 - 30), (200, 60))  

# Ship settings
ship = Actor('ship.png')
ship.x = WIDTH // 2
ship.y = HEIGHT - 75 
ship_speed = 8

damaged_time = 0
damage_duration = 0.25

# Fire actor
fire = Actor('fire.png')
fire_speed = 5
fire_location = ship.height / 1.3

# Bullet settings
bullet_speed = 10
bullets = []

# Enemies and Meteors settings
enemies = []
meteor_big = []
meteor_small = []

enemy_speed = 3
meteor_big_speed = 2
meteor_small_speed = 4

# Score settings
score = 0  
highest_score = 0

# Lives settings
lives = [Actor('ship_life') for _ in range(3)]

# Game state
game_over = False
game_started = False

# --------------------------------------------------------------------
#PLAYER:


# Initial positions:

for i, life in enumerate(lives):
    life.x = WIDTH - 50 * (i + 1) 
    life.y = 50

# Update lives :

def update_lives():
    global score, highest_score, game_over
    
    if len(lives) > 0:
        lives.pop()
        
    if len(lives) == 0: 
        game_over = True
        sounds.gameover.play()
        if score > highest_score:
            highest_score = score
            
# --------------------------------------------------------------------

# GAME FUNCTIONS: 

# Game start function
def start_game():
    global game_started, score, lives, enemies, meteor_big, meteor_small, game_over,WIDTH, HEIGHT
    game_started = True 
    score = 0 
    ship.x = WIDTH // 2
    ship.y = HEIGHT - 75 
    lives = [Actor('ship_life') for _ in range(3)] 
    
    # Initialize positions of lives
    for i, life in enumerate(lives):
        life.x = WIDTH - 50 * (i + 1)
        life.y = 50
        
    enemies = []  
    meteor_big = []  
    meteor_small = []  
    game_over = False 


def on_key_down(key):
    
     # 'R' key to reset the game
        
    if game_over and key == keys.R:
        start_game()
          
    # The ship fires bullets with the space key
    
    elif key == keys.SPACE and game_started:
        bullet = Actor('bullet')
        bullet.x = ship.x
        bullet.y = ship.y
        bullets.append(bullet)

        
def on_mouse_down(pos):
    global game_started, background_music
    
    
    if not game_started:
        
        if button_sound_rect.collidepoint(pos):
           
            background_music = not background_music
            if background_music:
                sounds.background_music.play(loops=-1, maxtime=0)
            else:
                sounds.background_music.stop()
                
        elif button_quit_rect.collidepoint(pos): 
    
            quit() 
              
        elif button_play_rect.collidepoint(pos):
            
            game_started = True
    
        
       
def get_damaged():
    
    global damaged_time
    
    if time.time() - damaged_time < damage_duration:
        ship.image = 'damaged_ship.png'  
    else: 
        ship.image = 'ship.png'  
        damaged_time = 0 
        
   
def update():
    global score, damaged_time,fire, game_started
    
    if not game_started:
        return
    
    if game_over:
        return
      
    # Spawn enemies and meteors
    if random.randint(1, 50) == 1:
        spawn_enemy()
    if random.randint(1, 70) == 1:
        spawn_meteor_big()
    if random.randint(1, 50) == 1:
        spawn_meteor_small()

    # The ship can move left,right,up and down using arrow keys: 
    if keyboard.left:
        ship.x -= ship_speed
        fire.image = 'fire.png'
    if keyboard.right:
        ship.x += ship_speed
        fire.image = 'fire.png' 
    if keyboard.up:
        ship.y -= ship_speed
        fire.image = 'fire_up.png'
    if keyboard.down:
        ship.y += ship_speed
        fire.image = 'fire.png'
        
    # Fire follows the ship's position, always below it  
    fire.x = ship.x
    fire.y = ship.y + fire_location
        
        
    # Update bullet positions:
    for bullet in bullets:
        bullet.y -= bullet_speed
    
    # Update enemy positions:
    for enemy in enemies:
        enemy.y += enemy_speed
        for bullet in bullets:
            if enemy.colliderect(bullet):
                sounds.lasershot.play()
                score += 3
                bullets.remove(bullet)
                enemies.remove(enemy)
                
        # When enemy takes damages from ship:
               
        if enemy.colliderect(ship):            
            
            sounds.damage.play()
            damaged_time = time.time() 
            get_damaged()
            update_lives() 
            enemies.remove(enemy)
               
    # Meteors update
    for meteor in meteor_big:
        meteor.y += meteor_big_speed
        
        meteor.angle += 1
        if meteor.angle >= 360:
            meteor.angle = 0
        
        for bullet in bullets:
            if meteor.colliderect(bullet):
                sounds.lasershot.play()
                score += 2
                bullets.remove(bullet)
                meteor_big.remove(meteor)
                
        # When meteor takes damages from ship:
        if meteor.colliderect(ship):
            
            sounds.damage.play()
            damaged_time = time.time() 
            update_lives() 
            meteor_big.remove(meteor)

    for meteor in meteor_small:
        meteor.y += meteor_small_speed
        
        meteor.angle += 2
        if meteor.angle >= 360:
            meteor.angle = 0
        
        for bullet in bullets:
            if meteor.colliderect(bullet):
                sounds.lasershot.play()
                score += 1
                bullets.remove(bullet)
                meteor_small.remove(meteor)
                
        # When meteor takes damages from ship:
        
        if meteor.colliderect(ship):
            
            sounds.damage.play()
            damaged_time = time.time() 
            get_damaged()
            update_lives() 
            meteor_small.remove(meteor)

    # Remove off-screen bullets
    bullets[:] = [bullet for bullet in bullets if bullet.y > 0]
    
    # Remove off-screen enemies and meteors
    enemies[:] = [enemy for enemy in enemies if enemy.y < HEIGHT]
    meteor_big[:] = [meteor for meteor in meteor_big if meteor.y < HEIGHT]
    meteor_small[:] = [meteor for meteor in meteor_small if meteor.y < HEIGHT]
    
    get_damaged()

# --------------------------------------------------------------------

# Enemies and Meteors functions:

def spawn_enemy():
    enemy = Actor('enemy')
    enemy.x = random.randint(40, WIDTH - 40)
    enemy.y = random.randint(-300, -50)
    enemies.append(enemy)

def spawn_meteor_big():
    meteor = Actor('meteor_big')
    meteor.x = random.randint(40, WIDTH - 40)
    meteor.y = random.randint(-300, -50)
    meteor.angle = random.randint(0, 360) 
    meteor_big.append(meteor)

def spawn_meteor_small():
    meteor = Actor('meteor_small')
    meteor.x = random.randint(40, WIDTH - 40)
    meteor.y = random.randint(-300, -50)
    meteor.angle = random.randint(0, 360) 
    meteor_small.append(meteor)
    
    
# --------------------------------------------------------------------

def draw_start_screen():
    screen.draw.text("Play", center=button_play_rect.center, fontsize=50, color="white")
    screen.draw.text("Sound", center=button_sound_rect.center, fontsize=50, color="white")
    screen.draw.text("Quit", center=button_quit_rect.center, fontsize=50, color="white")

def draw_score():
    screen.draw.text(f"Score: {score}", (5, 5), color="black", fontsize=40)

def draw_game_over():
    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), color="red", fontsize=60)
        screen.draw.text(f"Score: {score}", center=(WIDTH // 2, HEIGHT // 3), color="black", fontsize=60)
        screen.draw.text(f"Highest Score: {highest_score}", center=(WIDTH // 2, HEIGHT // 4), color="black", fontsize=60)
        screen.draw.text("Press 'R' to Restart", center=(WIDTH // 2, HEIGHT // 2 + 100), color="white", fontsize=40)

def draw():
    screen.clear()
    screen.fill(background_color)
    
    if not game_started:
        
        draw_start_screen()
        return
    
    ship.draw()
    fire.draw()
        
    for bullet in bullets:
        bullet.draw()
    for enemy in enemies:
        enemy.draw()
    for meteor in meteor_big:
        meteor.draw()
    for meteor in meteor_small:
        meteor.draw()
    for life in lives:
        life.draw()

    draw_score()


    if game_over:
        draw_game_over()
        return

pgzrun.go()