import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI

# Board dimensions and number of mines
HEIGHT = 8
WIDTH = 8
MINES = 8

# Colors in RGB
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Initialize pygame and screen
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Board layout calculations
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Load and resize images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Create game logic + AI
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Track game state
revealed = set()   # Cells revealed by user or AI
flags = set()      # Cells flagged as mines
lost = False       # Game-over condition
instructions = True  # Show rules before game starts

# -------------------------------
# Main game loop
# -------------------------------
while True:

    # Check quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Instructions screen (before playing)
    if instructions:
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect(center=((width / 2), 50))
        screen.blit(title, titleRect)

        # Game rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Mark all mines successfully to win!"
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect(center=((width / 2), 150 + 30 * i))
            screen.blit(line, lineRect)

        # Play button
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect(center=buttonRect.center)
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # If clicked → start game
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # -------------------------------
    # Draw Minesweeper board
    # -------------------------------
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            # Draw gray square for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            # Show mine/flag/number if revealed
            if game.is_mine((i, j)) and lost:
                screen.blit(mine, rect)  # Reveal mine only if game lost
            elif (i, j) in flags:
                screen.blit(flag, rect)  # Player-flagged mine
            elif (i, j) in revealed:
                neighbors = smallFont.render(
                    str(game.nearby_mines((i, j))), True, BLACK
                )
                neighborsTextRect = neighbors.get_rect(center=rect.center)
                screen.blit(neighbors, neighborsTextRect)

            row.append(rect)
        cells.append(row)

    # -------------------------------
    # Buttons: AI Move / Reset
    # -------------------------------
    aiButton = pygame.Rect((2 / 3) * width + BOARD_PADDING,
                           (1 / 3) * height - 50,
                           (width / 3) - BOARD_PADDING * 2, 50)
    pygame.draw.rect(screen, WHITE, aiButton)
    screen.blit(mediumFont.render("AI Move", True, BLACK), aiButton.move(40, 10))

    resetButton = pygame.Rect((2 / 3) * width + BOARD_PADDING,
                              (1 / 3) * height + 20,
                              (width / 3) - BOARD_PADDING * 2, 50)
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(mediumFont.render("Reset", True, BLACK), resetButton.move(50, 10))

    # Win/Loss display
    text = "Lost" if lost else "Won" if game.mines == flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect(center=((5 / 6) * width, (2 / 3) * height))
    screen.blit(text, textRect)

    move = None  # Default (no move yet)
    left, _, right = pygame.mouse.get_pressed()

    # -------------------------------
    # Player input
    # -------------------------------
    # Right-click → toggle flag
    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    # Left-click → AI button / Reset / Reveal cell
    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # AI move
        if aiButton.collidepoint(mouse) and not lost:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    flags = ai.mines.copy()
                    print("No moves left to make.")
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
            time.sleep(0.2)

        # Reset button
        elif resetButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            continue

        # Reveal clicked cell
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                        and (i, j) not in flags
                        and (i, j) not in revealed):
                        move = (i, j)

    # -------------------------------
    # Apply chosen move
    # -------------------------------
    if move:
        if game.is_mine(move):
            lost = True
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)

    pygame.display.flip()
