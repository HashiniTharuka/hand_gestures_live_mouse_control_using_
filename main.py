import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# ----------------------------
# Setup
# ----------------------------
cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils


# ----------------------------
# Finger detection helper
# ----------------------------
def fingers_up(lm_list):
    fingers = []

    # Thumb
    fingers.append(1 if lm_list[4][0] < lm_list[3][0] else 0)

    # Other 4 fingers
    tip_ids = [8, 12, 16, 20]
    for tip in tip_ids:
        fingers.append(1 if lm_list[tip][1] < lm_list[tip - 2][1] else 0)

    return fingers


# ----------------------------
# Main loop
# ----------------------------
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    lm_list = []

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            for id, lm in enumerate(hand.landmark):
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            if lm_list:
                fingers = fingers_up(lm_list)

                # ----------------------------
                # 1. Index only → Move mouse
                # ----------------------------
                if fingers == [0, 1, 0, 0, 0]:
                    x = np.interp(lm_list[8][0], (0, w), (0, screen_w))
                    y = np.interp(lm_list[8][1], (0, h), (0, screen_h))
                    pyautogui.moveTo(x, y)

                # ----------------------------
                # 2. Index + Middle → Left click
                # ----------------------------
                elif fingers == [0, 1, 1, 0, 0]:
                    pyautogui.click()

                # ----------------------------
                # 3. Index + Middle + Ring → Right click
                # ----------------------------
                elif fingers == [0, 1, 1, 1, 0]:
                    pyautogui.rightClick()

                # ----------------------------
                # 4. All fingers up → Scroll up
                # ----------------------------
                elif fingers == [1, 1, 1, 1, 1]:
                    pyautogui.scroll(10)

                # ----------------------------
                # 5. Fist → Scroll down
                # ----------------------------
                elif fingers == [0, 0, 0, 0, 0]:
                    pyautogui.scroll(-10)

                # ----------------------------
                # 6. Thumb + Index → Drag
                # ----------------------------
                elif fingers == [1, 1, 0, 0, 0]:
                    pyautogui.mouseDown()

                # ----------------------------
                # 7. Thumb only → Release drag
                # ----------------------------
                elif fingers == [1, 0, 0, 0, 0]:
                    pyautogui.mouseUp()

                # ----------------------------
                # 8. Index only (slow mode) → Move slower
                # ----------------------------
                elif fingers == [0, 1, 0, 0, 0]:
                    x = np.interp(lm_list[8][0], (0, w), (0, screen_w))
                    y = np.interp(lm_list[8][1], (0, h), (0, screen_h))
                    pyautogui.moveTo(x, y, duration=0.1)

                # ----------------------------
                # 9. Index + Pinky → Double click
                # ----------------------------
                elif fingers == [0, 1, 0, 0, 1]:
                    pyautogui.doubleClick()

                # ----------------------------
                # 10. Middle + Ring → Pause (do nothing)
                # ----------------------------
                elif fingers == [0, 0, 1, 1, 0]:
                    pass

    cv2.imshow("Hand Mouse Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()