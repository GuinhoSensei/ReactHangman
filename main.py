import pygame
import random
import sys
from words import words_with_hints

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman - PyGame")
clock = pygame.time.Clock()

# Colors and Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 180, 0)
BLUE = (30, 144, 255)

FONT = pygame.font.SysFont("arial", 48)
SMALL = pygame.font.SysFont("arial", 28)

# Sounds
correct_sound = pygame.mixer.Sound("assets/correct.wav")
incorrect_sound = pygame.mixer.Sound("assets/incorrect.wav")
winner_sound = pygame.mixer.Sound("assets/winner.wav")
loser_sound = pygame.mixer.Sound("assets/loser.wav")

# Background music
pygame.mixer.music.load("assets/background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Globals
difficulty = None
max_wrong = 0
games_won = 0
games_lost = 0

def draw_hangman(errors):
    base_x = 100
    base_y = 500
    if errors > 0: pygame.draw.line(screen, BLACK, (base_x, base_y), (base_x+100, base_y), 5)
    if errors > 1: pygame.draw.line(screen, BLACK, (base_x+50, base_y), (base_x+50, base_y-250), 5)
    if errors > 2: pygame.draw.line(screen, BLACK, (base_x+50, base_y-250), (base_x+150, base_y-250), 5)
    if errors > 3: pygame.draw.line(screen, BLACK, (base_x+150, base_y-250), (base_x+150, base_y-220), 5)
    if errors > 4: pygame.draw.circle(screen, BLACK, (base_x+150, base_y-195), 25, 5)
    if errors > 5: pygame.draw.line(screen, BLACK, (base_x+150, base_y-170), (base_x+150, base_y-100), 5)
    if errors > 6: pygame.draw.line(screen, BLACK, (base_x+150, base_y-160), (base_x+120, base_y-130), 5)
    if errors > 7: pygame.draw.line(screen, BLACK, (base_x+150, base_y-160), (base_x+180, base_y-130), 5)
    if errors > 8: pygame.draw.line(screen, BLACK, (base_x+150, base_y-100), (base_x+120, base_y-70), 5)
    if errors > 9: pygame.draw.line(screen, BLACK, (base_x+150, base_y-100), (base_x+180, base_y-70), 5)

def draw_button(x, y, w, h, text, active=True, color=GRAY):
    pygame.draw.rect(screen, color, (x, y, w, h))
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2)
    label = SMALL.render(text, True, BLACK)
    screen.blit(label, (x + (w - label.get_width())//2, y + (h - label.get_height())//2))

def inside(x, y, bx, by, bw, bh):
    return bx <= x <= bx + bw and by <= y <= by + bh

def difficulty_screen():
    selecting = True
    while selecting:
        screen.fill(WHITE)
        title = FONT.render("Select Difficulty", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

        draw_button(250, 300, 120, 60, "Easy", color=GREEN)
        draw_button(430, 300, 120, 60, "Hard", color=RED)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if inside(mx, my, 250, 300, 120, 60):
                    return 10
                if inside(mx, my, 430, 300, 120, 60):
                    return 5

def reset_game():
    global word, hint, guessed, wrong, show_hint, game_over, win
    word, hint = random.choice(words_with_hints)
    guessed = []
    wrong = 0
    show_hint = False
    game_over = False
    win = False

max_wrong = difficulty_screen()
reset_game()

running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Word display
    display_word = ' '.join([l.upper() if l in guessed else '_' for l in word])
    word_surface = FONT.render(display_word, True, BLACK)
    screen.blit(word_surface, (400 - word_surface.get_width()//2, 280))

    # Hangman
    draw_hangman(wrong)

    # Hint button
    draw_button(620, 40, 140, 40, "Show Hint")
    if show_hint:
        hint_text = SMALL.render(f"Hint: {hint}", True, RED)
        screen.blit(hint_text, (400 - hint_text.get_width()//2, 340))

    # Wrong letters
    wrong_letters = [l.upper() for l in guessed if l not in word]
    wrong_text = SMALL.render("Wrong: " + ' '.join(wrong_letters), True, RED)
    screen.blit(wrong_text, (400 - wrong_text.get_width()//2, 390))

    # Stats
    stats_text = SMALL.render(f"Wins: {games_won}   Losses: {games_lost}", True, BLACK)
    screen.blit(stats_text, (10, 10))

    # Game Over & Replay
    if game_over:
        msg = "🎉 You Win!" if win else f"You Lost! Word: {word.upper()}"
        end_text = FONT.render(msg, True, RED)
        screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, 440))
        draw_button(320, 500, 160, 50, "Play Again", color=BLUE)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.KEYDOWN and not game_over:
            if event.unicode.isalpha():
                letter = event.unicode.lower()
                if letter not in guessed:
                    guessed.append(letter)
                    if letter not in word:
                        wrong += 1
                        incorrect_sound.play()
                    else:
                        correct_sound.play()
            if all([l in guessed for l in word]):
                win = True
                game_over = True
                games_won += 1
                winner_sound.play()
            elif wrong >= max_wrong:
                win = False
                game_over = True
                games_lost += 1
                loser_sound.play()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if inside(mx, my, 620, 40, 140, 40):
                show_hint = True
            if game_over and inside(mx, my, 320, 500, 160, 50):
                max_wrong = difficulty_screen()
                reset_game()

pygame.quit()
