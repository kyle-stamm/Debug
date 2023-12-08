# Grid Design and Fighters Code

import pygame
import time
import random

class Buttons:
    
    def __init__(self, x, y, image, name, font, cost):

        self.cost = cost
        self.x = x
        self.y = y
        self.name = name
        self.image = pygame.transform.scale(image, (120, 120))
        self.hitbox = pygame.Rect(self.x, self.y, 120, 120)
        self.clicked = False
        self.text = font.render(self.name, True, (255, 255, 255))
        self.cost_text = font.render(str(cost), True, (255, 255, 255))

    def draw(self, s):

        # Renders the name text for the fighters if they are clicked in the shop
        if self.clicked:
            pygame.draw.rect(s, (200,200,200), self.get_hitbox())
            s.blit(self.text, ((120 - self.text.get_width()) / 2 + self.x, self.y - self.text.get_height()))
        else:
            pygame.draw.rect(s, (255,255,255), self.get_hitbox())
        s.blit(self.cost_text, ((120 - self.cost_text.get_width()) / 2 + self.x, self.y + 120))
        s.blit(self.image, self.get_hitbox())
        
    # Detects if the shop buttons are clicked
    def was_clicked(self, pos, clicked, coins):
        if self.hitbox.collidepoint(pos[0], pos[1]):
            if coins >= self.cost:
                if (not self.get_clicked()):
                    if clicked == 0:
                        self.clicked = True
                else:
                    self.clicked = False
                return self.clicked
            
    def get_clicked(self):
        return self.clicked
    
    def get_name(self):
        return self.name

    def get_image(self):
        return self.image

    def used(self):
        self.clicked = False
        return self.cost
        
        
    def get_hitbox(self):
        return self.hitbox
        
class Fighter:

    def __init__(self, x, y, image, name):
        self.x = 300 + 120 * x
        self.y = 120 * y
        self.image = pygame.transform.scale(image, (120, 120))
        self.name = name
        self.time = time.time()
        self.grid_x = x
        self.grid_y = y
        self.chomped = False
        self.bug_chomped = None


        # Sets the HP stats for the fighters
        if name == "Bitcoin":
            self.hp = 5
        elif name == "Java":
            self.hp = 7
        elif name == "Python":
            self.hp = 13
        elif name == "Firewall":
            self.hp = 30
        elif name == "C#":
            self.hp = 9
        elif name == "McAfee Spikes":
            self.hp = 1

    # Renders the fighters
    def draw(self, s):
        s.blit(self.image, self.get_hitbox())

    def reset_time(self):
        self.time = time.time()
        
    def update(self):
            
        pass

    def get_time(self):
        return time.time() - self.time

    def get_name(self):
        return self.name

    def get_x(self):
        return self.grid_x

    def get_posy(self):
        return self.y

    def get_posx(self):
        return self.x

    def get_chomped(self):
        return self.chomped

    def chomp(self, bug):
        self.chomped = True
        self.bug_chomped = bug

    def get_bug(self):
        return self.bug_chomped

    def unchomp(self):
        self.chomped = False

    def get_y(self):
        return self.grid_y
    
    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, 120, 120)

    # Damages the fighters
    def damage(self,dps):
        self.hp -= dps
        print(str(self.name) +"HP: " + str(self.hp))

    # Removes the fighters if they lose all of their HP
    def fighter_remove(self):
        if self.hp <= 0:
            return True
        return False
    
    def was_clicked(self, pos):
        return self.get_hitbox().collidepoint(pos[0], pos[1])


    

class Bullets:
    def __init__(self, type, x, y, speed):
        self.type = type
        self.x = x
        self.y = y
        self.speed = speed

        # Loads the flame image if the shooting fighter is a java
        if type == "Java":
            flame = pygame.image.load("assets/Flame.png")
            self.image = pygame.transform.scale(flame, (50, 25))

        # Loads the nail image if the shooting fighter is a C#
        elif type == "C#":
            nail = pygame.image.load("assets/Nail.png")
            self.image = pygame.transform.scale(nail, (50,25))
        
    # Renders the nails
    def draw(self, s):
        s.blit(self.image, self.get_hitbox())

    # Moves the bullets
    def bullet_move(self, delta_time):
        self.x += self.speed * delta_time

    def get_type(self):
        return self.type

    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, 50, 25)

class Coins:
    def __init__(self):
        global coin
        coin = pygame.image.load("assets/Bitcoin.png")
        coin = pygame.transform.scale(coin, (25, 25))
        self.x = random.randint(300, 1300 - 25)
        self.y = random.randint(0, 600 - 25)
        self.hitbox = pygame.Rect(self.x, self.y, 25, 25)
        self.timer = 0
        
    def draw(self, s):
        s.blit(coin, self.get_hitbox())

    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, 25, 25)

    def was_clicked(self, pos):
        return self.get_hitbox().collidepoint(pos[0], pos[1])

    def remove(self):
        if self.timer >= 10:
            return True
    
