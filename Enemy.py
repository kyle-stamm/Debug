# Enemy spawning code


import pygame
import random
import time

SCREEN_WIDTH = 1300

# Set list of random spawn points
spawn_points = [(SCREEN_WIDTH+50,0),(SCREEN_WIDTH+50,120),(SCREEN_WIDTH+50,240),(SCREEN_WIDTH+50,360),(SCREEN_WIDTH+50,480)]


class Enemy:

    def __init__(self, enemy_name):
        global crunch, poison
        # Crunch and poison sound effects
        crunch = pygame.mixer.Sound("assets/crunch.mp3")
        poison = pygame.mixer.Sound("assets/poison.mp3")
        
        self.image = pygame.image.load(f"assets/{enemy_name}.png")
        self.name = enemy_name
        self.spawn = spawn_points[random.randint(0,len(spawn_points)-1)]
        self.x = self.spawn[0]
        self.y = self.spawn[1]
        self.hitbox = pygame.Rect(self.x,self.y,100,100)
        self.speed = 0
        self.hp = 0
        self.timer = 1
        self.collide = 0
        self.attack = 0
        self.dps = 0
        self.chomped = False
        self.time = 0
        self.player_damage = 0
        self.is_boss = 0
        self.is_poisoned = False
        self.poison_time = None

        # Sets the scorpion's spawn point in the center 3 rows since its a boss
        if self.name == "scorpion":
            self.x = 1320
            self.y = 120
    def render(self, screen):
        
        # Gives the scorpion a special set of render dimensions since it's a boss
        if self.name == "scorpion":
            self.image = pygame.transform.scale(self.image,(300,300))
            screen.blit(self.image,(self.x-20,self.y+30))
            
        # Renders the normal enemies
        else:
            self.image = pygame.transform.scale(self.image,(100,100))
            screen.blit(self.image,(self.x,self.y))
    
    def move(self,delta_time):

        # Movement for normal enemies
        if self.name != "scorpion":
            if self.collide == 0:
                self.x -= self.speed*delta_time
                self.hitbox = pygame.Rect(self.x,self.y,100,100)
        # Movement for the scorpion boss
        else:
            if self.collide == 0:
                self.x -= self.speed*delta_time
                self.hitbox = pygame.Rect(self.x+20,self.y,280,300)

    # Removes the enemies if they die or they reach the left side of the screen
    def remove(self):
        if self.x <300:
            return True
        if self.hp <= 0:
            return True
        return False

    # Returns the hitbox for use in collisions
    def get_hitbox(self):
        return self.hitbox

    # Allows the enemies to damage the fighters at set intervals while they're colliding
    def dmg_timer(self,delta_time):
        self.timer -= delta_time
        if not self.chomped or self.is_boss == 1:
            if self.is_boss == 1 and self.chomped:
                if time.time() - self.time >= 1:
                    self.take_damage(1)
                    crunch.play()
                    self.time = time.time()
                    print(self.name, "HP:", self.hp)
            if self.timer < 0:
                self.attack = 1
            if self.timer < -delta_time:
                self.timer = 1
                self.attack = 0
        else:
            if time.time() - self.time >= 1:
                self.take_damage(1)
                crunch.play()
                self.time = time.time()
                print(self.name, "HP:", self.hp)

    # Detects if the enemy is poisoned            
    def poison(self):
        self.poison_time = time.time()
        self.is_poisoned = True

    # Deals poison damage to the enemy if they are poisoned
    def poison_damage(self):
        
        if self.is_poisoned:
            if time.time() - self.poison_time >= 1:
                self.take_damage(1)
                self.poison_time = time.time()
                print("poisoned", self.hp)
                poison.play()
                
    
    def get_health(self):
        return self.hp

    def get_chomped(self):
        return self.chomped
    
    
    def attack(self):
        return self.attack

    # Detects if the enemy is colliding with a fighter or not
    def hit(self):
        self.collide = 1    
    def not_hit(self):
        self.collide = 0

    # Deals damage to the enemy
    def take_damage(self, damage):
        self.hp -= damage
        
    def get_dps(self):
        return self.dps

    def get_y(self):
        return self.y

    # Chomps the enemies
    def chomp(self, time):
        self.chomped = True
        self.collide = 1
        self.attack = 0
        self.time = time

    def get_player_damage(self):
        return self.player_damage

    # Detects if the enemy is a boss
    def get_is_boss(self):
        return self.is_boss

    def boss_chomp(self, time):
        self.chomped = True
        self.collide = 1
        self.time = time
        
# Initializes the enemies with their stats
class Mantis(Enemy):

    def __init__(self):
        super().__init__("mantis")
        self.speed = 100
        self.hp = 3
        self.dps = 3
        self.player_damage = 8

class Cockroach(Enemy):

    def __init__(self):
        super().__init__("cockroach")
        self.speed = 50
        self.hp = 7
        self.dps = 2
        self.player_damage = 4

class Mosquito(Enemy):

    def __init__(self):
        super().__init__("mosquito")
        self.speed = 150
        self.hp = 1
        self.dps = 1
        self.player_damage = 2

class Bee(Enemy):

    def __init__(self):
        super().__init__("bee")
        self.speed = 125
        self.hp = 4
        self.dps = 2
        self.player_damage = 6

class Beetle(Enemy):

    def __init__(self):
        super().__init__("beetle")
        self.speed = 62.5
        self.hp = 12
        self.dps = 1
        self.player_damage = 10

class Ant(Enemy):

    def __init__(self):
        super().__init__("ant")
        self.speed = 75
        self.hp = 5
        self.dps = 2
        self.player_damage = 4

class Scorpion(Enemy):

    def __init__(self,num):
        super().__init__("scorpion")
        
        # Increases the scorpions health and speed each time it spawns
        self.speed = 25*(1+(num*0.4))
        self.hp = 80*(1+(num*0.35))
        
        self.dps = 4
        self.player_damage = 40
        self.is_boss = 1
