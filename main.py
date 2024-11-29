import cv2
import mediapipe as mp
import numpy as np


# код функции взят с docs.opencv.org
def draw_character(img1, img2, x=0, y=0):

    rows, cols, channels = img2.shape
    roi = img1[y:rows+y, x:cols+x]

    img2gray = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    img2_fg = cv2.bitwise_and(img2, img2, mask=mask)

    dst = cv2.add(img1_bg, img2_fg)
    img1[y:rows+y, x:cols+x] = dst

    return img1


def draw_field():

    cv2.line(flippedRGB, (0, 240), (1280, 240), (149, 255, 110), 10)
    cv2.line(flippedRGB, (0, 240 * 2), (1280, 240 * 2), (149, 255, 110), 10)

    cv2.line(flippedRGB, (190, 0), (190, 720), (149, 255, 110), 10)
    cv2.line(flippedRGB, (190 * 2, 0), (190 * 2, 720), (149, 255, 110), 10)
    cv2.line(flippedRGB, (190 * 3, 0), (190 * 3, 720), (149, 255, 110), 10)
    cv2.line(flippedRGB, (190 * 4, 0), (190 * 4, 720), (149, 255, 110), 10)
    cv2.line(flippedRGB, (190 * 5, 0), (190 * 5, 720), (149, 255, 110), 10)
    cv2.line(flippedRGB, (190 * 6, 0), (190 * 6, 720), (149, 255, 110), 10)


def cursor_draw():
    x_top = int(results.multi_hand_landmarks[0].landmark[4].x *
                flippedRGB.shape[1])
    y_top = int(results.multi_hand_landmarks[0].landmark[4].y *
                flippedRGB.shape[0])

    cv2.circle(flippedRGB, (x_top, y_top), 10, (255, 0, 0), -1)

    x_low = int(results.multi_hand_landmarks[0].landmark[8].x *
                flippedRGB.shape[1])
    y_low = int(results.multi_hand_landmarks[0].landmark[8].y *
                flippedRGB.shape[0])

    cv2.circle(flippedRGB, (x_low, y_low), 10, (255, 0, 0), -1)


def fingers_pos():

    x = int(results.multi_hand_landmarks[0].landmark[4].x *
                flippedRGB.shape[1])
    y = int(results.multi_hand_landmarks[0].landmark[4].y *
                flippedRGB.shape[0])

    row = 0
    col = 0

    for i in range(len(line_y)):
        if line_y[i] > y:
            row = max(0, i - 1)
            break
        elif i == len(line_y) - 1:
            row = i
            break

    for i in range(len(line_x)):
        if line_x[i] > x:
            col = max(0, i - 1)
            break
        elif i == len(line_x) - 1:
            col = i
            break

    return field_plane[row][col]


def character_moving():
    global char_x, char_y, goal_y, goal_x

    y_top = int(results.multi_hand_landmarks[0].landmark[4].y *
                flippedRGB.shape[0])
    y_low = int(results.multi_hand_landmarks[0].landmark[8].y *
                flippedRGB.shape[0])

    check_finger = abs(y_top - y_low) <= 30

    if goal_y != char_y:
        char_y += 4 * (goal_y - char_y) // abs(goal_y - char_y)
        if abs(goal_y - char_y) <= 3:
            char_y = goal_y

    elif char_x != goal_x:
        char_x += 4 * (goal_x - char_x) // abs(goal_x - char_x)
        if abs(goal_x - char_x) <= 3:
            char_x = goal_x

    elif check_finger:
        goal_x, goal_y = fingers_pos()

        if abs(char_x - goal_x) > 200 or abs(char_y - goal_y) > 300:
            goal_x, goal_y = char_x, char_y


handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)

main_char = cv2.imread('wizard1.png')
main_char = cv2.cvtColor(main_char, cv2.COLOR_BGR2RGB)
char_x = 5
char_y = 5
goal_x = 5
goal_y = 5
field_plane = [[[5, 5], [196, 5], [387, 5], [578, 5], [766, 5], [957, 5]],
               [[5, 245], [196, 245], [387, 245], [578, 245], [766, 245], [957, 245]],
               [[5, 489], [196, 489], [387, 487], [578, 487], [766, 487], [957, 487]]]
line_x = [5, 196, 387, 578, 766, 957]
line_y = [5, 245, 489]


while cap.isOpened():

    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break
    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = handsDetector.process(flippedRGB)

    flippedRGB = draw_character(flippedRGB, main_char, char_x, char_y)
    draw_field()

    if results.multi_hand_landmarks is not None:

        cursor_draw()

        character_moving()

    res_image = cv2.cvtColor(flippedRGB, cv2.COLOR_RGB2BGR)
    cv2.imshow("Hands", res_image)


handsDetector.close()
