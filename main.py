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


def help_draw():
    x_top = int(results.multi_hand_landmarks[0].landmark[8].x *
                flippedRGB.shape[1])
    y_top = int(results.multi_hand_landmarks[0].landmark[8].y *
                flippedRGB.shape[0])

    cv2.circle(flippedRGB, (x_top, y_top), 10, (255, 0, 0), -1)

    x_low = int(results.multi_hand_landmarks[0].landmark[5].x *
                flippedRGB.shape[1])
    y_low = int(results.multi_hand_landmarks[0].landmark[5].y *
                flippedRGB.shape[0])

    cv2.circle(flippedRGB, (x_low, y_low), 10, (0, 255, 0), -1)

    x_top = int(results.multi_hand_landmarks[0].landmark[12].x *
                flippedRGB.shape[1])
    y_top = int(results.multi_hand_landmarks[0].landmark[12].y *
                flippedRGB.shape[0])

    cv2.circle(flippedRGB, (x_top, y_top), 10, (255, 0, 0), -1)

    x_low = int(results.multi_hand_landmarks[0].landmark[9].x *
                flippedRGB.shape[1])
    y_low = int(results.multi_hand_landmarks[0].landmark[9].y *
                flippedRGB.shape[0])

    cv2.circle(flippedRGB, (x_low, y_low), 10, (0, 255, 0), -1)


handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)
k = 0

main_char = cv2.imread('wizard1.png')
main_char = cv2.cvtColor(main_char, cv2.COLOR_BGR2RGB)
char_x = 5
char_y = 489
field_plane = [[[5, 5], [196, 5], [387, 5], [578, 5], [766, 5], [957, 5]],
               [[5, 245], [196, 245], [387, 245], [578, 245], [766, 254], [957, 245]],
               [[5, 489], [196, 489], [387, 487], [578, 487], [766, 287], [957, 245]]]


while cap.isOpened():
    k += 1

    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break
    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = handsDetector.process(flippedRGB)

    flippedRGB = draw_character(flippedRGB, main_char, char_x, char_y)
    draw_field()

    if results.multi_hand_landmarks is not None:

        help_draw()


        # check_finger = abs(y_top - y_low) <= 140
        pass

    res_image = cv2.cvtColor(flippedRGB, cv2.COLOR_RGB2BGR)
    cv2.imshow("Hands", res_image)


handsDetector.close()
