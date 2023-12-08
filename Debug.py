# Kyle Stamm and Aidan Priore
# Final Project
# Python 3

from Enemy import *
from Grid import *

heart1 = pygame.image.load("assets/heart1.png")

total_time = 0
# Testing Variables
STARTING_COINS = 20
BITCOIN_TIME = 2

# Spawning variables
spawn_interval = 0
spawn_rate = 0


# Boss variables
boss_time = 0
boss_interval = 60
boss_difficulty = -1

health = 100

# Text variables
health_text = 0
end_text = 0
warning_text = 0

# % chance for enemies to spawn
mosquito_chance = 20
cockroach_chance = 20
bee_chance = 20
beetle_chance = 10
ant_chance = 20
mantis_chance = 10

# Lists
enemy_list = []
spawn_queue = []
chance_list = []

    
# Sets the chances for enemies to spawn
for num in range(1,mantis_chance):
    chance_list.append("mantis")
for num in range(1,cockroach_chance):
    chance_list.append("cockroach")
for num in range(1,mosquito_chance):
    chance_list.append("mosquito")
for num in range(1,bee_chance):
    chance_list.append("bee")
for num in range(1,beetle_chance):
    chance_list.append("beetle")
for num in range(1,ant_chance):
    chance_list.append("ant")


chance_list.append("placeholder")

# Checks for click
def clicks(pos):
    global fighter_list, clicked, grid_list, coins
    x = (pos[0] - 300) // 120
    y = pos[1] // 120
    
    for b in button_list:
        if b.get_clicked():
            click.play()
            if x >= 0 and y >= 0 and x <= 7:
                if grid_list[x][y] == None:
                    zap.play()
                    grid_list[x][y] = b.get_name()
                    fighter_list.append(Fighter(x, y, b.get_image(), b.get_name()))
                    clicked = 0
                    coins -= b.used()
    

# Updates the game every frame
def update(delta_time):

    global spawn_interval, spawn_rate, max_rate, total_time, health, boss_difficulty, coin_time

    # Tracks total time since the program started
    if health > 0:
        total_time += delta_time
        coin_time += delta_time
        if coin_time >= 2:
            coin_list.append(Coins())
            coin_time = 0
        
    global coins, bullet_list

    # Difficulty mods
    if total_time > delta_time:
        spawn_rate = 5
    if total_time > 10:
        spawn_rate = 4.5
    if total_time > 20:
        spawn_rate = 4
    if total_time > 30:
        spawn_rate = 3.5
    if total_time > 40:
        spawn_rate = 3
    if total_time > 50:
        spawn_rate = 2.5
    if total_time > 60:
        spawn_rate = 2
    if total_time > 70:
        spawn_rate = 1.5
    

    for f in fighter_list:

        # Makes bitcoin fighters generate money
        if f.get_name() == "Bitcoin":
            if f.get_time() // BITCOIN_TIME == 1:
                f.reset_time()
                coins += 1
        
        # Makes the java enemies shoot
        elif f.get_name() == "Java":
            for e in enemy_list:
                if e.get_y() == f.get_posy() or 1 in spawn_queue:
                    if f.get_time() // 2 == 1:
                        whoosh.play()
                        bullet_list.append(Bullets("Java", f.get_posx() + 50, f.get_posy() + 10, 300))
                        f.reset_time()
            if f.get_time() // 2 == 1:
                f.reset_time()
        
        # Makes the C# enemies shoot
        elif f.get_name() == "C#":
            for e in enemy_list:
                if e.get_y() == f.get_posy() or 1 in spawn_queue:
                    if f.get_time() // 0.5 == 1:
                        whoosh.play()
                        bullet_list.append(Bullets("C#", f.get_posx() + 45, f.get_posy() + 50, 300))
                        f.reset_time()
            if f.get_time() // 0.5 == 1:
                f.reset_time()
                            

    global boss_time, boss_interval

    # Updates the countdown until the next boss
    if 1 not in spawn_queue:
        boss_time += delta_time

    # Spawns bosses at set intervals
    if boss_time > boss_interval and 1 not in spawn_queue:
        spawn_queue.append("scorpion")
        boss_time = 0
        spawn_queue.append(1)
        # Increases the difficulty of the boss every time it spawns
        boss_difficulty += 1

    
    # Cheats for money lol
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_c]:
        coins += 1
    pass


    # Queues up enemies to be spawned at intervals, gets faster over time
    spawn_interval += delta_time
    if spawn_interval > spawn_rate and health > 0:
        spawn_queue.append(chance_list[random.randint(1,len(chance_list)-1)])
        spawn_interval = 0    
    spawn()


    # Removes the enemies if they die or reach the left side of the screen
    for enemy in enemy_list:
        enemy.move(delta_time)
        if enemy.remove():
            if enemy.get_is_boss() == 1:
                spawn_queue.remove(1)
            enemy_list.remove(enemy)
            if enemy.get_health() > 0:
                health -= enemy.get_player_damage()
            if health <= 0:
                health = 0
        elif enemy.remove():
            enemy_list.remove(enemy)
            if enemy.get_is_boss() == 1:
                spawn_queue.remove(1)

    # Damages the enemies if they get hit by bullets or damaged by poison
    for enemy in enemy_list:
        for b in bullet_list:
            if enemy.get_hitbox().colliderect(b.get_hitbox()):
                if b.get_type() == "Java":
                    enemy.take_damage(2)
                    impact.play()
                elif b.get_type() == "C#":
                    enemy.take_damage(0.5)
                    splat.play()
                bullet_list.remove(b)
        enemy.poison_damage()


        for fighter in fighter_list:

            # Detects if the enemies are colliding with the fighters
            if enemy.get_hitbox().colliderect(fighter.get_hitbox()):

                # Chomps the enemies if the fighter is a python
                if fighter.get_name() == "Python":
                    if fighter.get_chomped():
                        if fighter.get_bug() in enemy_list:
                            if enemy == fighter.get_bug():
                                if enemy.get_health() <= 0:
                                    fighter.unchomp()
                        else:
                            fighter.unchomp()
                    elif enemy.get_is_boss() == 1:
                        chomp_time = time.time()
                        crunch.play()
                        enemy.boss_chomp(chomp_time)
                        fighter.chomp(enemy)
                    else:
                        chomp_time = time.time()
                        crunch.play()
                        enemy.chomp(chomp_time)
                        fighter.chomp(enemy)
                # Poisons the enemy if the fighter is a McCafee spikes
                elif fighter.get_name() == "McAfee Spikes":
                    fighter_list.remove(fighter)
                    enemy.poison()
                    stab.play()
                    grid_list[fighter.get_x()][fighter.get_y()] = None
                    enemy.take_damage(1)

                enemy.hit()

                # Damages the fighter if the enemy is allowed to attack
                if enemy.attack == 1:
                    hurt.play()
                    fighter.damage(enemy.get_dps())
                enemy.dmg_timer(delta_time)
                break
            else:
                enemy.not_hit()

            # Removes the fighter if they die
            if fighter.fighter_remove():
                fighter_list.remove(fighter)
                grid_list[fighter.get_x()][fighter.get_y()] = None
        else:
            enemy.not_hit()

    # Moves the bullets
    for b in bullet_list:
        b.bullet_move(delta_time)

    # Clears all enemies and fighters if the player dies
    if health <= 0:
        enemy_list.clear()
        fighter_list.clear()
        coin_list.clear()
    
def spawn():
    global boss_difficulty

    # Spawns the enemies when they are queued up
    for item in spawn_queue:
        if item == "mantis":
            enemy_list.append(Mantis())
            if len(spawn_queue) > 0:
                spawn_queue.remove(item)
        if item == "cockroach":
            enemy_list.append(Cockroach())
            if len(spawn_queue) > 0:
                spawn_queue.remove(item)
        if item == "mosquito":
            enemy_list.append(Mosquito())
            if len(spawn_queue) > 0:
                spawn_queue.remove(item)
        if item == "bee":
            enemy_list.append(Bee())
            if len(spawn_queue) > 0:
                spawn_queue.remove(item)
        if item == "ant":
            enemy_list.append(Ant())
            if len(spawn_queue) > 0:
                spawn_queue.remove(item)
        if item == "beetle":
            enemy_list.append(Beetle())
            if len(spawn_queue) > 0:
                spawn_queue.remove(item)
        if item == "scorpion":
            enemy_list.append(Scorpion(boss_difficulty))
            if len(spawn_queue) > 0:
                spawn_queue.remove(item)



# Renders the game every frame
def render(screen):
    screen.fill(BACKGROUND)
    # Grid System
    counter = 0
    for y in range(5):
        counter += 1
        for x in range(8):
            pygame.draw.rect(screen, ((200, 200, 200) if counter % 2 == 0 else (40, 40, 40)), ((300 + 120 * x, 0 + 120 * y), (120, 120)))
            counter += 1


    # Render health text
    heart_x = 245
    heart = pygame.transform.scale(heart1,(50,50))
    screen.blit(heart,(heart_x,5))
    health_text = FONT.render(str(health),True,(255,255,255))
    screen.blit(health_text,((50 - health_text.get_width()) / 2 + heart_x,15))

    # Renders the warning text 10 seconds before the boss spawns
    warning_text = FONT.render("Boss fight coming soon!",True,(255,0,0))
    if boss_time > (boss_interval-10) and boss_time < (boss_interval - 5):
        screen.blit(warning_text,(40,562.5))  
    
    
    # Render Coin Amount
    screen.blit(Bitcoin, ((0, 0), (50, 50)))
    bitcoin_text = FONT.render(str(coins), True, (255, 255, 255))
    screen.blit(bitcoin_text, (Bitcoin.get_width(), 10))

    # Renders the buttons
    for b in button_list:
        b.draw(screen)

    # Renders the fighters
    for fighter in fighter_list:
        fighter.draw(screen)

    # Renders the enemies
    for enemy in enemy_list:
        enemy.render(screen)

    # Renders the bullets
    for b in bullet_list:
        b.draw(screen)

    # Renders the game end text
    if health <= 0:
        end_text = END_FONT.render("You died! You survived " + str(round(total_time)) + " seconds!",True,(255,0,0))
        screen.blit(end_text,(400,260))

    for c in coin_list:
        c.draw(screen)


def main():
    pygame.init()
    # Variables and lists
    global grid_list, button_list, screen, fighter_list, clicked, FONT, coins, bullet_list, END_FONT, coin_time, coin_list
    grid_list = []
    button_list = []
    fighter_list = []
    bullet_list = []
    
    clicked = 0
    coins = STARTING_COINS

    coin_time = 0
    coin_list = []

    # Fonts
    FONT = pygame.font.SysFont("comicsansms", 20)
    END_FONT = pygame.font.SysFont("comicsansms", 48)

    # Graphics
    global Bitcoin
    Java = pygame.image.load("assets/Java.png")
    button_list.append(Buttons(30, 60, Java, "Java", FONT, 10))

    Python = pygame.image.load("assets/Python.png")
    button_list.append(Buttons(160, 60, Python, "Python", FONT, 20))
    
    Firewall = pygame.image.load("assets/Firewall.png")
    button_list.append(Buttons(30, 240, Firewall, "Firewall", FONT, 15))

    Bitcoin = pygame.image.load("assets/Bitcoin.png")
    button_list.append(Buttons(160, 240, Bitcoin, "Bitcoin", FONT, 5))
    Bitcoin = pygame.transform.scale(Bitcoin, (50, 50))

    CSharp = pygame.image.load("assets/CSharp.png")
    button_list.append(Buttons(30, 420, CSharp, "C#", FONT, 20))

    McAfee = pygame.image.load("assets/McAfee.png")
    button_list.append(Buttons(160, 420, McAfee, "McAfee Spikes", FONT, 5))

    # audio
    global click, zap, whoosh, impact, crunch, hurt, splat, stab, coin_sound
    pygame.mixer.init()
    
    bg_music = pygame.mixer.Sound("assets/Background.mp3")
    bg_music.set_volume(0.25)
    bg_music.play(20)

    click = pygame.mixer.Sound("assets/click.mp3")
    click.set_volume(50)
    
    zap = pygame.mixer.Sound("assets/zap.mp3")
    zap.set_volume(3)

    whoosh = pygame.mixer.Sound("assets/whoosh.mp3")

    impact = pygame.mixer.Sound("assets/impact.mp3")

    crunch = pygame.mixer.Sound("assets/crunch.mp3")

    hurt = pygame.mixer.Sound("assets/hurt.mp3")
    hurt.set_volume(0.5)

    splat = pygame.mixer.Sound("assets/splat.mp3")

    stab = pygame.mixer.Sound("assets/Stab.mp3")

    coin_sound = pygame.mixer.Sound("assets/coin.mp3")

    poison = pygame.mixer.Sound("assets/poison.mp3")
    
    # Pygame init
    
    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH, SCREEN_HEIGHT = (1300, 600)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Debug")

    # Start game screen
    screen.fill((0, 0,0))
    is_paused = True
    start_text = END_FONT.render("Press p to Start",True,(255,0,0))
    screen.blit(start_text,((screen.get_width() - start_text.get_width()) / 2,(screen.get_height() - start_text.get_height()) / 2))
    pygame.display.flip()
    
    # grid list
    for x in range(8):
        row = []
        grid_list.append(row)
        for y in range(5):
            row.append(None)


    # Render init
    global BACKGROUND
    BACKGROUND = (127, 127, 127)

    while is_paused:
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        is_paused = False
        
    # Game loop
    running = True
    last_frame = time.time()

    while running:

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONUP:
                click_counter = 0
                for b in button_list:    
                    if b.was_clicked(pygame.mouse.get_pos(), clicked, coins):
                        clicked = 1
                for b in button_list:
                    if b.get_clicked():
                        click_counter += 1
                if click_counter == 0:
                    clicked = 0

                # Removes the fighters if the user shift clicks on them
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_LSHIFT]:
                    for f in fighter_list:
                        if f.was_clicked(pygame.mouse.get_pos()):
                            fighter_list.remove(f)
                            grid_list[f.get_x()][f.get_y()] = None

                for c in coin_list:
                    if c.was_clicked(pygame.mouse.get_pos()):
                        coins += 1
                        coin_sound.play()
                        coin_list.remove(c)

                # Gets mouse position    
                clicks(pygame.mouse.get_pos())       

        # Update
        cur_frame = time.time()
        delta_time = cur_frame - last_frame
        last_frame = cur_frame
        update(delta_time)

        # Render
        render(screen)
        pygame.display.flip()

    # Quit game
    pygame.quit()

main()
