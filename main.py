import cv2
import mediapipe as mp
import numpy as np
import random


class Hero:

    def __init__(self, x: int = 5, y: int = 5):

        self.x = x
        self.y = y
        self.goal_x = x
        self.goal_y = y

        self.hp = 100
        self.atk = 10
        self.df = 10
        self.money_counter = 0

        self.img = cv2.imread('images/wizard.png')
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

    def draw_text(self, img2):

        img2 = cv2.putText(img2, 'Health: ' + str(main_char.hp), (190 * 5 + 25, 100),
                                 cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
        img2 = cv2.putText(img2, 'Strength: ' + str(main_char.atk), (190 * 5 + 25, 100 + 60),
                                 cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
        img2 = cv2.putText(img2, 'Defence: ' + str(main_char.df), (190 * 5 + 25, 100 + 60 + 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
        img2 = cv2.putText(img2, 'Money: ' + str(main_char.money_counter), (190 * 5 + 25, 100 + 60 + 60 + 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)

        return img2

    def get_prise(self):

        prise = random.randint(1, 5)
        if self.hp == 100:
            if prise == 1:
                self.hp -= 30
            else:
                self.money_counter += 1
        else:
            if prise == 1:
                self.hp -= 30
            elif prise == 2 or prise == 3:
                self.hp += 10
            else:
                self.money_counter += 1


class Chest:

    def __init__(self, x: int = 387, y: int = 245):

        self.x = x
        self.y = y
        self.img = cv2.imread('images/chest.png')
        self.alive = True

    def random_position(self, char: "Hero") -> None:

        if not self.alive:

            self.alive = True

            chest_x = random.choice(line_x)
            chest_y = random.choice(line_y)

            while chest_x == char.x and chest_y == char.y:
                chest_x = random.choice(line_x)
                chest_y = random.choice(line_y)

            self.x = chest_x
            self.y = chest_y

    def draw(self, img2):

        if chest.alive:
            return draw_character(img2, self.img, self.x, self.y + 40)
        else:
            return img2


class Craft:

    def __init__(self):

        self.x = 766
        self.y = 5
        self.img = cv2.imread('images/craft.png')
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        self.products = ['stick', 'shield']

        self.stick_img = cv2.imread('images/stick.png')
        self.stick_img = cv2.cvtColor(self.stick_img, cv2.COLOR_BGR2RGB)
        self.stick_img = cv2.resize(self.stick_img, (198, 480))

        self.shield_img = cv2.imread('images/shield.png')
        self.shield_img = cv2.cvtColor(self.shield_img, cv2.COLOR_BGR2RGB)
        self.shield_img = cv2.resize(self.shield_img, (368, 448))

    def draw_items(self, img2):

        if 'stick' in self.products:
            img2 = draw_character(img2, self.stick_img, 200, 70)
            img2 = cv2.putText(img2, 'Attack: +10 ', (200, 150 + 480 - 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
            img2 = cv2.putText(img2, 'Cost: 10 ', (200, 150 + 480 + 40),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)

        if 'shield' in self.products:
            img2 = draw_character(img2, self.shield_img, 750, 100)
            img2 = cv2.putText(img2, 'Defence: +10 ', (750, 150 + 480 - 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)
            img2 = cv2.putText(img2, 'Cost: 10 ', (750, 150 + 480 + 40),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)

        return img2


def touch(ch: 'Chest', mn: 'Hero') -> None:

    if ch.x == mn.x and ch.y == mn.y:

        ch.alive = False
        mn.get_prise()


# код функции взят с docs.opencv.org
def draw_character(img1, img2, x=0, y=0) -> np.array:

    rows, cols, channels = img2.shape
    roi = img1[y:rows+y, x:cols+x]

    img2gray = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    img2_fg = cv2.bitwise_and(img2, img2, mask=mask)

    dst = cv2.add(img1_bg, img2_fg)
    img1[y:rows+y, x:cols+x] = dst

    return img1


def draw_field():

    # Числа подбирались вручную, исходя из рамеров картинок
    cv2.line(flippedRGB, (0, 240), (190 * 5, 240), (149, 255, 110), 10)
    cv2.line(flippedRGB, (0, 240 * 2), (190 * 5, 240 * 2), (149, 255, 110), 10)

    cv2.line(flippedRGB, (190, 0), (190, 720), (149, 255, 110), 10)
    cv2.line(flippedRGB, (190 * 2, 0), (190 * 2, 720), (149, 255, 110), 10)
    cv2.line(flippedRGB, (190 * 3, 0), (190 * 3, 720), (149, 255, 110), 10)
    cv2.line(flippedRGB, (190 * 4, 0), (190 * 4, 720), (149, 255, 110), 10)
    cv2.line(flippedRGB, (190 * 5, 0), (190 * 5, 720), (149, 255, 110), 10)


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

    x = int(results.multi_hand_landmarks[0].landmark[4].x * flippedRGB.shape[1])
    y = int(results.multi_hand_landmarks[0].landmark[4].y * flippedRGB.shape[0])

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

    y_top = int(results.multi_hand_landmarks[0].landmark[4].y *
                flippedRGB.shape[0])
    x_top = int(results.multi_hand_landmarks[0].landmark[4].x *
                flippedRGB.shape[0])
    y_low = int(results.multi_hand_landmarks[0].landmark[8].y *
                flippedRGB.shape[0])
    x_low = int(results.multi_hand_landmarks[0].landmark[8].x *
                flippedRGB.shape[0])

    check_finger = abs(y_top - y_low) <= 30 and abs(x_low - x_top) <= 30

    if main_char.goal_y != main_char.y:
        main_char.y += 10 * (main_char.goal_y - main_char.y) // abs(main_char.goal_y - main_char.y)
        if abs(main_char.goal_y - main_char.y) <= 9:
            main_char.y = main_char.goal_y

    elif main_char.x != main_char.goal_x:
        main_char.x += 10 * (main_char.goal_x - main_char.x) // abs(main_char.goal_x - main_char.x)
        if abs(main_char.goal_x - main_char.x) <= 9:
            main_char.x = main_char.goal_x

    elif check_finger:
        main_char.goal_x, main_char.goal_y = fingers_pos()

        if (abs(main_char.x - main_char.goal_x) > 200 or abs(main_char.y - main_char.goal_y) > 300 or
                (main_char.goal_x != main_char.x and main_char.goal_y != main_char.y)):
            main_char.goal_x, main_char.goal_y = main_char.x, main_char.y


handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)

main_char = Hero()
chest = Chest()
craft = Craft()
field_plane = [[[5, 5], [196, 5], [387, 5], [578, 5], [766, 5]],
               [[5, 245], [196, 245], [387, 245], [578, 245], [766, 245]],
               [[5, 489], [196, 489], [387, 489], [578, 489], [766, 489]]]
line_x = [5, 196, 387, 578, 766]
line_y = [5, 245, 489]
world_status = 'main'


while cap.isOpened():

    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break
    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    flippedRGB = cv2.resize(flippedRGB, (1280, 720))
    results = handsDetector.process(flippedRGB)

    if world_status == 'main':
        chest.random_position(main_char)
        flippedRGB = chest.draw(flippedRGB)

        draw_field()

        flippedRGB = draw_character(flippedRGB, craft.img, craft.x, craft.y)

        flippedRGB = main_char.draw_text(flippedRGB)

        flippedRGB = draw_character(flippedRGB, main_char.img, main_char.x, main_char.y)

        if results.multi_hand_landmarks is not None:

            cursor_draw()

            character_moving()

            touch(chest, main_char)

        if craft.x == main_char.x and craft.y == main_char.y:
            world_status = 'craft'

    elif world_status == 'craft':

        craft.draw_items(flippedRGB)

    res_image = cv2.cvtColor(flippedRGB, cv2.COLOR_RGB2BGR)
    cv2.imshow("Game", res_image)


handsDetector.close()
