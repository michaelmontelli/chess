import pygame

# Define background color with RGB
background_color = (234, 212, 252)

# Define the dimensions of the screen object -> (width, height)
screen = pygame.display.set_mode((800, 800))

# Set the caption of the screen
pygame.display.set_caption('Chess')

# Fill the background color to the screen
# screen.fill(background_color)

# Update the display using flip
pygame.display.flip()

# Variable to keep our game loop running
running = True

# game loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False


