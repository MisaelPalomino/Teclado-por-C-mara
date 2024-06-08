import cv2
import mediapipe as mp
import pygame
import numpy as np

# Inicializar MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Inicializar Pygame
pygame.init()
win_width, win_height = 800, 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Teclado Virtual")
font = pygame.font.Font(None, 74)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Definir las teclas del teclado
keys = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
key_size = 60
spacing = 10
x_start, y_start = 50, 50

def draw_keyboard():
    key_positions = {}
    for i, key in enumerate(keys):
        x = x_start + (i % 10) * (key_size + spacing)
        y = y_start + (i // 10) * (key_size + spacing)
        pygame.draw.rect(win, black, (x, y, key_size, key_size))
        text = font.render(key, True, white)
        win.blit(text, (x + 10, y + 10))
        key_positions[key] = (x, y, key_size, key_size)
    return key_positions

def get_key_from_position(key_positions, pos):
    for key, (x, y, w, h) in key_positions.items():
        if x <= pos[0] <= x + w and y <= pos[1] <= y + h:
            return key
    return None

# Iniciar captura de video
cap = cv2.VideoCapture(0)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    win.fill(white)
    key_positions = draw_keyboard()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                pygame.draw.circle(win, red, (cx, cy), 10)
                key = get_key_from_position(key_positions, (cx, cy))
                if key:
                    print(f"Tecla presionada: {key}")

    cv2.imshow('Hand Tracking', image)
    pygame.display.flip()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
