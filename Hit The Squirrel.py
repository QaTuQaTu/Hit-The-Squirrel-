question=input('Choose the level(easy/hard)')
question.lower()
if question=='easy':

    import pygame
    import time
    from random import randint

    pygame.init()

    pygame.mixer.init()

    hit_sound = pygame.mixer.Sound('hit.wav')
    miss_sound = pygame.mixer.Sound('miss.wav')

    WINDOW_SIZE = (500, 600)  
    IMAGE_WIDTH, IMAGE_HEIGHT = 210, 230
    NUM_ROWS = 3  
    NUM_COLS = 3  
    SPACING_X = 150
    SPACING_Y = 160
    UPDATE_INTERVAL = 1  
    GAME_DURATION = 30
    WIN_POINTS = 10

    mw = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    squirrel_image = pygame.image.load('squirrel new2.png')
    squirrel_image = pygame.transform.scale(squirrel_image, (IMAGE_WIDTH, IMAGE_HEIGHT))

    hole_image = pygame.image.load('hole new2.png')
    hole_image = pygame.transform.scale(hole_image, (IMAGE_WIDTH, IMAGE_HEIGHT))

    hammer_image = pygame.image.load('hammer.png')
    hammer_image = pygame.transform.scale(hammer_image, (50, 50))

    # Rectangle class
    class Area:
        def __init__(self, x=0, y=0, width=10, height=10):# CONSTRUCTER
            self.rect = pygame.Rect(x, y, width, height)
        
        def collidepoint(self, x, y):
            return self.rect.collidepoint(x, y)

    class Label(Area):
        def __init__(self, x=0, y=0, width=10, height=10):
            super().__init__(x, y, width, height)
            self.text = ''
            self.font_size = 20
            self.text_color = (0, 0, 100)  # DARK_BLUE
            self.font = pygame.font.SysFont('verdana', self.font_size)
        
        def set_text(self, text, fsize=20, text_color=(0, 0, 100)):  # DARK_BLUE
            self.text = text
            self.font_size = fsize
            self.text_color = text_color
            self.font = pygame.font.SysFont('verdana', self.font_size)
        
        def draw(self):
            text_image = self.font.render(self.text, True, self.text_color)
            mw.blit(text_image, self.rect.topleft)

    time_text = Label(0, 0, 500, 50)
    time_text.set_text('Time:', 40, (0, 0, 100))  # DARK_BLUE
    score_text = Label(380, 0, 120, 50)
    score_text.set_text('Count:', 45, (0, 0, 100))  # DARK_BLUE
    timer = Label(50, 55, 100, 40)
    timer.set_text('0', 40, (0, 0, 100))  # DARK_BLUE
    score = Label(430, 55, 100, 40)
    score.set_text('0', 40, (0, 0, 100))  # DARK_BLUE

    def draw_static_text():
        time_text.draw()
        score_text.draw()
        timer.draw()
        score.draw()

    squirrels = []
    x_offset = 30
    y_offset = 120

    # Create squirrels and holes
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            x = x_offset + col * SPACING_X
            y = y_offset + row * SPACING_Y
            squirrels.append(Label(x, y, IMAGE_WIDTH, IMAGE_HEIGHT))

    wait = 0
    points = 0
    start_time = time.time()
    cur_time = start_time
    squirrel_timer = time.time()
    current_squirrel = randint(0, len(squirrels) - 1)
    next_squirrel_time = start_time + UPDATE_INTERVAL

    # Main game loop
    while True:
        mw.fill((200, 255, 255))  # BACK color


        for i, squirrel in enumerate(squirrels):
            mw.blit(hole_image, squirrel.rect.topleft)  
            if i == current_squirrel:
                mw.blit(squirrel_image, squirrel.rect.topleft)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if squirrels[current_squirrel].collidepoint(x, y):
                    points += 1
                    hit_sound.play()  # Play hit sound
                else:
                    points -= 1
                    miss_sound.play()  # Play miss sound
                score.set_text(str(points), 40, (0, 0, 100))  # DARK_BLUE
                pygame.display.update()  # Ensure score is updated immediately
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    IMAGE_WIDTH += 10
                    IMAGE_HEIGHT += 10
                    hole_image = pygame.transform.scale(hole_image, (IMAGE_WIDTH, IMAGE_HEIGHT))
                    squirrel_image = pygame.transform.scale(squirrel_image, (IMAGE_WIDTH, IMAGE_HEIGHT))
                elif event.key == pygame.K_DOWN:
                    IMAGE_WIDTH -= 10
                    IMAGE_HEIGHT -= 10
                    hole_image = pygame.transform.scale(hole_image, (IMAGE_WIDTH, IMAGE_HEIGHT))
                    squirrel_image = pygame.transform.scale(squirrel_image, (IMAGE_WIDTH, IMAGE_HEIGHT))

        new_time = time.time()

        if new_time - start_time >= GAME_DURATION:
            mw.fill((250, 128, 114))  # LIGHT_RED
            win_message = Label(0, 0, 500, 500)
            win_message.set_text("Time's up!!!", 60, (0, 0, 100))  # DARK_BLUE
            win_message.draw()
            pygame.display.update()
            pygame.time.wait(2000)  # Wait for 2 seconds before quitting
            break

        if int(new_time) - int(cur_time) == 1:
            timer.set_text(str(int(new_time - start_time)), 40, (0, 0, 100))  # DARK_BLUE
            cur_time = new_time

        if points >= WIN_POINTS:
            mw.fill((200, 255, 200))  # LIGHT_GREEN
            win_message = Label(0, 0, 500, 500)
            win_message.set_text("You won!!!", 60, (0, 0, 100))  # DARK_BLUE
            win_message.draw()
            result_time = Label(90, 230, 250, 250)
            result_time.set_text("Completion time: " + str(int(new_time - start_time)) + " sec", 40, (0, 0, 100))  # DARK_BLUE
            result_time.draw()
            pygame.display.update()
            pygame.time.wait(2000)  
            break

        if new_time >= next_squirrel_time:
            current_squirrel = randint(0, len(squirrels) - 1)
            next_squirrel_time = new_time + UPDATE_INTERVAL

        draw_static_text()
        
        # cursor to hammer
        pygame.mouse.set_visible(False)  # Hide default cursor
        mw.blit(hammer_image, pygame.mouse.get_pos())

        pygame.display.update()
        clock.tick(40)


if question=='hard':
    import pygame
    import time
    from random import randint

    pygame.init()

    # Initialize sound mixer
    pygame.mixer.init()

    # Load sound effects
    hit_sound = pygame.mixer.Sound('hit.wav')
    miss_sound = pygame.mixer.Sound('miss.wav')

    WINDOW_SIZE = (500, 600)  
    IMAGE_WIDTH, IMAGE_HEIGHT = 210, 230
    NUM_ROWS = 3  
    NUM_COLS = 3  
    SPACING_X = 150
    SPACING_Y = 160
    UPDATE_INTERVAL = 0.6
    GAME_DURATION = 20
    WIN_POINTS = 15

    mw = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    # Load and scale squirrel image
    squirrel_image = pygame.image.load('squirrel new2.png')
    squirrel_image = pygame.transform.scale(squirrel_image, (IMAGE_WIDTH, IMAGE_HEIGHT))

    # Load and scale hole image
    hole_image = pygame.image.load('hole new2.png')
    hole_image = pygame.transform.scale(hole_image, (IMAGE_WIDTH, IMAGE_HEIGHT))

    # Load and scale hammer image
    hammer_image = pygame.image.load('hammer.png')
    hammer_image = pygame.transform.scale(hammer_image, (50, 50))

    # Rectangle class
    class Area:
        def __init__(self, x=0, y=0, width=10, height=10):
            self.rect = pygame.Rect(x, y, width, height)
        
        def collidepoint(self, x, y):
            return self.rect.collidepoint(x, y)

    class Label(Area):
        def __init__(self, x=0, y=0, width=10, height=10):
            super().__init__(x, y, width, height)
            self.text = ''
            self.font_size = 20
            self.text_color = (0, 0, 100)  # DARK_BLUE
            self.font = pygame.font.SysFont('verdana', self.font_size)
        
        def set_text(self, text, fsize=20, text_color=(0, 0, 100)):  # DARK_BLUE
            self.text = text
            self.font_size = fsize
            self.text_color = text_color
            self.font = pygame.font.SysFont('verdana', self.font_size)
        
        def draw(self):
            text_image = self.font.render(self.text, True, self.text_color)
            mw.blit(text_image, self.rect.topleft)

    time_text = Label(0, 0, 500, 50)
    time_text.set_text('Time:', 40, (0, 0, 100))  # DARK_BLUE
    score_text = Label(380, 0, 120, 50)
    score_text.set_text('Count:', 45, (0, 0, 100))  # DARK_BLUE
    timer = Label(50, 55, 100, 40)
    timer.set_text('0', 40, (0, 0, 100))  # DARK_BLUE
    score = Label(430, 55, 100, 40)
    score.set_text('0', 40, (0, 0, 100))  # DARK_BLUE

    def draw_static_text():
        time_text.draw()
        score_text.draw()
        timer.draw()
        score.draw()

    squirrels = []
    x_offset = 30
    y_offset = 120

    # Create squirrels and holes
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            x = x_offset + col * SPACING_X
            y = y_offset + row * SPACING_Y
            squirrels.append(Label(x, y, IMAGE_WIDTH, IMAGE_HEIGHT))

    wait = 0
    points = 0
    start_time = time.time()
    cur_time = start_time
    squirrel_timer = time.time()
    current_squirrel = randint(0, len(squirrels) - 1)
    next_squirrel_time = start_time + UPDATE_INTERVAL

    # Main game loop
    while True:
        mw.fill((200, 255, 255))  # BACK color

        # Draw the hole image first, then draw the squirrel on top if it's the current one
        for i, squirrel in enumerate(squirrels):
            mw.blit(hole_image, squirrel.rect.topleft)  # Draw hole
            if i == current_squirrel:
                mw.blit(squirrel_image, squirrel.rect.topleft)  # Draw squirrel on top of the hole

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if squirrels[current_squirrel].collidepoint(x, y):
                    points += 1
                    hit_sound.play()  
                else:
                    points -= 1
                    miss_sound.play() 
                score.set_text(str(points), 40, (0, 0, 100))  # DARK_BLUE
                pygame.display.update()  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    IMAGE_WIDTH += 10
                    IMAGE_HEIGHT += 10
                    hole_image = pygame.transform.scale(hole_image, (IMAGE_WIDTH, IMAGE_HEIGHT))
                    squirrel_image = pygame.transform.scale(squirrel_image, (IMAGE_WIDTH, IMAGE_HEIGHT))
                elif event.key == pygame.K_DOWN:
                    IMAGE_WIDTH -= 10
                    IMAGE_HEIGHT -= 10
                    hole_image = pygame.transform.scale(hole_image, (IMAGE_WIDTH, IMAGE_HEIGHT))
                    squirrel_image = pygame.transform.scale(squirrel_image, (IMAGE_WIDTH, IMAGE_HEIGHT))

        new_time = time.time()

        if new_time - start_time >= GAME_DURATION:
            mw.fill((250, 128, 114))  # LIGHT_RED
            win_message = Label(0, 0, 500, 500)
            win_message.set_text("Time's up!!!", 60, (0, 0, 100))  # DARK_BLUE
            win_message.draw()
            pygame.display.update()
            pygame.time.wait(2000)  # Wait for 2 seconds before quitting
            break

        if int(new_time) - int(cur_time) == 1:
            timer.set_text(str(int(new_time - start_time)), 40, (0, 0, 100))  # DARK_BLUE
            cur_time = new_time

        if points >= WIN_POINTS:
            mw.fill((200, 255, 200))  # LIGHT_GREEN
            win_message = Label(0, 0, 500, 500)
            win_message.set_text("You won!!!", 60, (0, 0, 100))  # DARK_BLUE
            win_message.draw()
            result_time = Label(90, 230, 250, 250)
            result_time.set_text("Completion time: " + str(int(new_time - start_time)) + " sec", 40, (0, 0, 100))  # DARK_BLUE
            result_time.draw()
            pygame.display.update()
            pygame.time.wait(2000)  # Wait for 2 seconds before quitting
            break

        if new_time >= next_squirrel_time:
            current_squirrel = randint(0, len(squirrels) - 1)
            next_squirrel_time = new_time + UPDATE_INTERVAL

        draw_static_text()
        
        # Update cursor to hammer
        pygame.mouse.set_visible(False)  # Hide default cursor
        mw.blit(hammer_image, pygame.mouse.get_pos())

        pygame.display.update()
        clock.tick(40)