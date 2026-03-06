import pygame

# ------------------------- Global Variables and Initialization -------------------------

# Initialize Pygame - or simply put, start the game engine
pygame.init()
pygame.mixer.init() # Initialize sound effects (May add later)


# GLOBAL VARIABLES
PADDLE_SPEED = 5
AI_SPEED = 4
BALL_SPEED_X = 2
BALL_SPEED_Y = 2
PLAYER_SCORE = 0
COMP_SCORE = 0
WIDTH = 800
HEIGHT = 600
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
SCREEN_TITLE = "Pong Prototype"
FONT = pygame.font.SysFont("Arial", 30)
TEXT_SURFACE_1 = FONT.render(str("Player: " + str(PLAYER_SCORE)), True, WHITE_COLOR)
TEXT_SURFACE_2 = FONT.render(str("Computer: " + str(COMP_SCORE)), True, WHITE_COLOR)
GAME_STATE = "START" # Can be START, PLAYING, and GAMEOVER

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# Set up the game clock to control the frame rate (Otherswise, the game would run as fast as the computer can handle, which is not ideal)
clock = pygame.time.Clock()
TICK_RATE = 60

# This first fills the screen black, and then is creating the paddles and the ball
screen.fill(BLACK_COLOR)
playerPaddle =pygame.draw.rect(screen, WHITE_COLOR, (50, 250, 10, 100))  # Left paddle
compPaddle = pygame.draw.rect(screen, WHITE_COLOR, (740, 250, 10, 100))  # Right paddle
ball =pygame.draw.rect(screen, WHITE_COLOR, (385, 300, 15, 15))  # Ball - left/right, up/down, size of the ball

ball.x = WIDTH // 2
ball.y = HEIGHT // 2

# ------------------------- Main game loop -------------------------
    # Playing/displaying the game screen
while True:
    # Break out of the loop 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed() # Check for key presses to move the paddle 

    if GAME_STATE == "START":
    # Display the start screen
        screen.fill(BLACK_COLOR)
        start_text = FONT.render("Press SPACE to Start", True, WHITE_COLOR)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
        pygame.display.flip()
        if keys[pygame.K_SPACE]: # If the space key is pressed, start the game
            GAME_STATE = "PLAYING"


    elif GAME_STATE == "PLAYING":
        
        if keys[pygame.K_UP]:
            playerPaddle.y -= PADDLE_SPEED  # Move the paddle up
        elif keys[pygame.K_DOWN]:
            playerPaddle.y += PADDLE_SPEED  # Move the paddle down

        # Logic for Players paddle 
        if playerPaddle.top <= 0: # Stops the paddle from going above the screen
            playerPaddle.top = 0
        elif playerPaddle.bottom >= HEIGHT: # Stops the paddle from going below the screen
            playerPaddle.bottom = HEIGHT

        # Logic for the ball movement
        ball.x += BALL_SPEED_X
        ball.y += BALL_SPEED_Y

        if BALL_SPEED_X > 10:
            BALL_SPEED_X = 10

        if BALL_SPEED_Y > 10:
            BALL_SPEED_Y = 10

        if ball.left <= 0:
            BALL_SPEED_X = 2
            COMP_SCORE += 1
            TEXT_SURFACE_2 = FONT.render(str("Computer: " + str(COMP_SCORE)), True, WHITE_COLOR) # Update the score text for the computer
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
            BALL_SPEED_X *= -1  # Reverse the x direction of the ball (Horizontal bounce)
        elif ball.right >= WIDTH:
            BALL_SPEED_X = 2
            PLAYER_SCORE += 1
            TEXT_SURFACE_1 = FONT.render(str("Player: " + str(PLAYER_SCORE)), True, WHITE_COLOR) # Update the score text for the player
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
            BALL_SPEED_X *= -1  # Reverse the x direction of the ball (Horizontal bounce)

        # Logic for ball collision with the top and bottom of the screen
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            BALL_SPEED_Y *= -1  # Reverse the y direction of the ball (Vertical bounce)

        # Logic for ball collision with paddles
        if ball.colliderect(playerPaddle) or ball.colliderect(compPaddle):
            BALL_SPEED_X *= -1  # Reverse the x direction of the ball (Horizontal bounce)
            if BALL_SPEED_X > 0:
                ball.x += 5  # Move the ball slightly to prevent it from getting stuck in the paddle
                BALL_SPEED_X += 0.5  # Increase the speed of the ball after each paddle hit 
            else:
                ball.x -= 5
                BALL_SPEED_X -= 0.5  # Increase the speed of the ball after each paddle hit            

        # Logic for computer paddle movement - simple AI that follows the ball's y position
        if compPaddle.top <= 0: # Stops the paddle from going above the screen
            compPaddle.top = 0
        elif compPaddle.bottom >= HEIGHT: # Stops the paddle from going below the screen
            compPaddle.bottom = HEIGHT

        if ball.centery > compPaddle.centery + 8: # if the ball is below the center of the computer paddle, move the paddle down
            compPaddle.y += AI_SPEED
        elif ball.centery < compPaddle.centery - 8: # If the ball is above the center of the computer paddle, move the paddle up
            compPaddle.y -= AI_SPEED

        # Drawing the game elements on the screen - everytime we run through the loop, we have to redraw the screen as well to create the effects of graphics
        screen.fill(BLACK_COLOR)
        screen.blit(TEXT_SURFACE_1, (WIDTH // 3 - 200, 10))
        screen.blit(TEXT_SURFACE_2, (WIDTH // 2 + 200, 10))
        pygame.draw.rect(screen, WHITE_COLOR, playerPaddle)
        pygame.draw.rect(screen, WHITE_COLOR, compPaddle)
        pygame.draw.rect(screen, WHITE_COLOR, ball)
        pygame.display.flip()  # Can either update the whole screen or just a portion of it, depending on the needs of the game

        # Winner logic 
        if PLAYER_SCORE >= 5 or COMP_SCORE >= 5:
            GAME_STATE = "GAMEOVER"

        clock.tick(TICK_RATE)


    elif GAME_STATE == "GAMEOVER":
        # Display Game Over screen
        screen.fill(BLACK_COLOR)
        if PLAYER_SCORE > COMP_SCORE:
            game_over_text = FONT.render("Game Over! You Win!", True, WHITE_COLOR)
        elif COMP_SCORE > PLAYER_SCORE:
            game_over_text = FONT.render("Game Over! Computer Wins!", True, WHITE_COLOR)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()