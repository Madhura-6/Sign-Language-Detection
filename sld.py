import streamlit as st
import mediapipe as mp
import cv2
import numpy as np
import tempfile
import time
from PIL import Image
import os
import speech_recognition as sr
from PIL import Image
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils


DEMO_VIDEO = 'demo.mp4'
DEMO_IMAGE = 'demo.jpg'

my_list = []



st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 350px;
        margin-left: -350px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title('Sign Language Detection')
st.sidebar.subheader('-Parameter')

@st.cache_resource()
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):

    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:

        r = height / float(h)
        dim = (int(w * r), height)


    else:

        r = width / float(w)
        dim = (width, int(h * r))


    resized = cv2.resize(image, dim, interpolation=inter)


    return resized

app_mode = st.sidebar.selectbox('Choose the App mode',
['Select Mode','Sign Language to Text','Speech to sign Language']
)

if app_mode =='Select Mode':
    st.title('Sign Language Detection System')
    st.markdown('In this application, we are using *MediaPipe* for detecting sign language. Our system employs machine learning algorithms to interpret hand gestures and translate them into text. With the help of *MediaPipe*, we can accurately detect and analyze various sign language gestures in real-time, enabling seamless communication.. ')
    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
    
    st.markdown('''
              # About Us \n 
              Our cutting-edge AI technology empowers users to interpret sign languages effectively,
              ensuring seamless communication for individuals with hearing
              and speech disabilities. Committed to bridging communication gaps, we strive
              to enhace accessibility and improve outcomes for all. Join us in transforming
              the way sign language is detected and interpreted, one gesture at a time.

            
              If you are facing any issue while working feel free to mail us on \n
                *officialg35btech@gmail.com*\n
              Special credit to   *Mr. N. A. Haval Sir*

                ''')
elif app_mode == 'Sign Language to Text':
    st.title('Sign Language to Text')
    st.set_option('deprecation.showfileUploaderEncoding', False)

    use_webcam = st.sidebar.button('Use Webcam')
    record = st.sidebar.checkbox("Record Video")
    if record:
        st.checkbox("Recording", value=True)

    st.sidebar.markdown('---')
    sameer=""
    st.markdown(' ## Output')
    st.markdown(sameer)

    stframe = st.empty()
    video_file_buffer = st.sidebar.file_uploader("Upload a video", type=["mp4", "mov", 'avi', 'asf', 'm4v'])
    tfflie = tempfile.NamedTemporaryFile(delete=False)

    if not video_file_buffer:
        if use_webcam:
            vid = cv2.VideoCapture(0)
        else:
            vid = cv2.VideoCapture(DEMO_VIDEO)
            tfflie.name = DEMO_VIDEO

    else:
        tfflie.write(video_file_buffer.read())
        vid = cv2.VideoCapture(tfflie.name)

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_input = int(vid.get(cv2.CAP_PROP_FPS))

    codec = cv2.VideoWriter_fourcc('V', 'P', '0', '9')
    out = cv2.VideoWriter('output1.mp4', codec, fps_input, (width, height))

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.sidebar.markdown('---')
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 400px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 400px;
            margin-left: -400px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    threshold = 0.1  # Define a reasonable threshold value
    while True:
        ret, img = vid.read()
        img = cv2.flip(img, 1)
        h, w, c = img.shape
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img)

        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(hand_landmark.landmark):
                    lm_list.append(lm)
                finger_fold_status = []
                for tip in finger_tips:
                    x, y = int(lm_list[tip].x * w), int(lm_list[tip].y * h)
                    # print(id, ":", x, y)
                    # cv2.circle(img, (x, y), 15, (255, 0, 0), cv2.FILLED)

                    if lm_list[tip].x < lm_list[tip - 2].x:
                        # cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                        finger_fold_status.append(True)
                    else:
                        finger_fold_status.append(False)

                print(finger_fold_status)
                x, y = int(lm_list[8].x * w), int(lm_list[8].y * h)
                print(x, y)
               

                # one
                if lm_list[3].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y and lm_list[4].y < lm_list[
                    12].y:
                    cv2.putText(img, "ONE", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("1")

                # two
                if lm_list[3].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                    cv2.putText(img, "TWO", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("2")
                    sameer="two"
                # three
                if lm_list[2].x < lm_list[4].x and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                    cv2.putText(img, "THREE", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("3")
                    sameer="three"

                # four
                if lm_list[2].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                        lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[2].x < lm_list[8].x:
                    cv2.putText(img, "FOUR", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("4")
                    sameer="Four"

                # five
                if lm_list[2].x < lm_list[4].x and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                        lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[
                    0].x < \
                        lm_list[5].x:
                    cv2.putText(img, "FIVE", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("5")
                    sameer="Five"
                    # six
                if lm_list[2].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                        lm_list[16].y < lm_list[14].y and lm_list[20].y > lm_list[18].y and lm_list[17].x < lm_list[
                    0].x < \
                        lm_list[5].x:
                    cv2.putText(img, "SIX", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("6")
                    sameer="Six"
                # SEVEN
                if lm_list[2].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[
                    0].x < \
                        lm_list[5].x:
                    cv2.putText(img, "SEVEN", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("7")
                    sameer="Seven"
                # EIGHT
                if lm_list[2].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                        lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[
                    0].x < \
                        lm_list[5].x:
                    cv2.putText(img, "EIGHT", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("8")
                    sameer="Eight"
                # NINE
                if lm_list[2].x > lm_list[4].x and lm_list[8].y > lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                        lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[
                    0].x < \
                        lm_list[5].x:
                    cv2.putText(img, "NINE", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("9")
                    sameer="Nine"
                # A
                if lm_list[2].y > lm_list[4].y and lm_list[8].y > lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y and lm_list[17].x < lm_list[
                    0].x < \
                        lm_list[5].x and lm_list[4].y < lm_list[6].y:
                    cv2.putText(img, "A", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("A")
                # B
                if lm_list[2].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                        lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[2].x > lm_list[8].x:
                    cv2.putText(img, "B", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("B")
                    sameer="B"
                # c
                if lm_list[2].x < lm_list[4].x and lm_list[8].x > lm_list[6].x and lm_list[12].x > lm_list[10].x and \
                        lm_list[16].x > lm_list[14].x and lm_list[20].x > lm_list[18].x:
                    cv2.putText(img, "C", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("C")
                # d
                if lm_list[3].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y and lm_list[4].y > lm_list[8].y:
                    cv2.putText(img, "D", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("D")

                # E
                if lm_list[2].x > lm_list[4].x and lm_list[8].y > lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y and lm_list[17].x < lm_list[
                    0].x < \
                        lm_list[5].x and lm_list[4].y > lm_list[6].y:
                    cv2.putText(img, "E", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("E")

               
              
                #F
                if lm_list[2].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[12].y > lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y < lm_list[18].y and lm_list[8].x > lm_list[4].x:
                    cv2.putText(img, "F", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("F")

                # G
                if lm_list[2].x > lm_list[4].x and lm_list[8].y > lm_list[6].y and \
                        lm_list[8].x < lm_list[6].x and lm_list[12].y > lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                    cv2.putText(img, "G", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("G")

                # H
                if lm_list[2].x < lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[12].y < lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y > lm_list[18].y:
                    cv2.putText(img, "H", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("H")

                # I
                if lm_list[2].x < lm_list[4].x and lm_list[8].y > lm_list[6].y and \
                        lm_list[12].y > lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y < lm_list[18].y:
                    cv2.putText(img, "I", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("I")

                # J
                if lm_list[2].x > lm_list[4].x and lm_list[8].y > lm_list[6].y and \
                        lm_list[12].y > lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y < lm_list[18].y:
                    cv2.putText(img, "J", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("J")

                # K
                if lm_list[2].x < lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[12].y < lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y < lm_list[18].y:
                    cv2.putText(img, "K", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("K")

                # L
                if lm_list[2].x < lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[12].y > lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y > lm_list[18].y:
                    cv2.putText(img, "L", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("L")
                # M
                    threshold = 20 # adjust this value to change the sensitivity of the gesture detection
                if (lm_list[2].x < lm_list[4].x - threshold and lm_list[8].y > lm_list[6].y + threshold and
                    lm_list[12].y > lm_list[10].y + threshold and lm_list[16].y > lm_list[14].y + threshold and
                    lm_list[20].y > lm_list[18].y + threshold and lm_list[4].y < lm_list[8].y - threshold and
                    lm_list[2].x > 0 and lm_list[2].x < img.shape[1] and lm_list[4].x > 0 and lm_list[4].x < img.shape[1] and
                    lm_list[6].y > 0 and lm_list[6].y < img.shape[0] and lm_list[8].y > 0 and lm_list[8].y < img.shape[0]):
                    cv2.putText(img, "M", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("M")  

                # N
                if lm_list[2].x < lm_list[4].x and lm_list[8].y > lm_list[6].y and \
                        lm_list[12].y > lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y > lm_list[18].y:
                    cv2.putText(img, "N", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("N")

                # O
                if lm_list[2].x < lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[8].x < lm_list[6].x and lm_list[12].y < lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                    cv2.putText(img, "O", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("O")

                # P
                if lm_list[2].x < lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[12].y < lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y < lm_list[18].y:
                    cv2.putText(img, "P", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("P")

                # Q
                if lm_list[2].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[8].x < lm_list[6].x and lm_list[12].y > lm_list[10].y and \
                        lm_list[16].y > lm_list[14].y and lm_list[20].y < lm_list[18].y:
                    cv2.putText(img, "Q", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("Q")

                # R
                if lm_list[2].x < lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[12].y > lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y > lm_list[18].y:
                    cv2.putText(img, "R", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("R")

                # S
                if lm_list[2].x < lm_list[4].x and lm_list[8].y > lm_list[6].y and \
                        lm_list[12].y > lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y > lm_list[18].y:
                    cv2.putText(img, "S", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("S")

                # T
                if lm_list[2].x < lm_list[4].x and lm_list[8].y > lm_list[6].y and \
                        lm_list[12].y > lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y > lm_list[18].y and lm_list[4].y < lm_list[10].y:
                    cv2.putText(img, "T", (20, 30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 3)
                    my_list.append("T")

                # U
                if lm_list[2].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[12].y < lm_list[10].y and lm_list[16].y < lm_list[14].y and \
                        lm_list[20].y < lm_list[18].y and lm_list[4].y > lm_list[10].y:
                    cv2.putText(img, "U", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("U")

                # V
                if lm_list[2].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[12].y < lm_list[10].y and lm_list[16].y < lm_list[14].y and \
                        lm_list[20].y < lm_list[18].y and lm_list[4].y > lm_list[10].y and \
                        lm_list[8].y > lm_list[14].y:
                    cv2.putText(img, "V", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("V")

                # W
                if lm_list[2].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[12].y < lm_list[10].y and lm_list[16].y < lm_list[14].y and \
                        lm_list[20].y < lm_list[18].y and lm_list[4].y > lm_list[10].y and \
                        lm_list[8].y > lm_list[14].y and lm_list[12].y > lm_list[18].y:
                    cv2.putText(img, "W", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("W")

                # X
                if lm_list[2].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[12].y < lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y < lm_list[18].y and lm_list[8].x < lm_list[6].x:
                    cv2.putText(img, "X", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("X")

                # Y
                if lm_list[2].x < lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[12].y < lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y < lm_list[18].y and lm_list[8].x < lm_list[6].x:
                    cv2.putText(img, "Y", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("Y")

                # Z
                if lm_list[2].x < lm_list[4].x and lm_list[8].y < lm_list[6].y and \
                        lm_list[12].y > lm_list[10].y and lm_list[16].y > lm_list[14].y and \
                        lm_list[20].y < lm_list[18].y:
                    cv2.putText(img, "Z", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    my_list.append("Z")    
                    
            mp_draw.draw_landmarks(img, hand_landmark,
                                   mp_hands.HAND_CONNECTIONS,
                                   mp_draw.DrawingSpec((0, 0, 255), 6, 3),
                                   mp_draw.DrawingSpec((0, 255, 0), 4, 2)
                                   )
            if record:

                out.write(img)


            frame = cv2.resize(img, (0, 0), fx=0.8, fy=0.8)
            frame = image_resize(image=frame, width=640)
            stframe.image(frame, channels='BGR', use_column_width=True)

    st.text('Video Processed')

    output_video = open('output1.mp4', 'rb')
    out_bytes = output_video.read()
    st.video(out_bytes)

    vid.release()
    out.release()
else:
    st.title('Speech to Sign Language (The System uses Indian Sign Language)')
    # initialize the speech recognition engine
    # initialize the speech recognition engine
    r = sr.Recognizer()


    # define function to display sign language images
    def display_images(text):
        # get the file path of the images directory
        img_dir = "images/"

        # initialize variable to track image position
        image_pos = st.empty()

        # iterate through the text and display sign language images
        for char in text:
            if char.isalpha():
                # display sign language image for the alphabet
                img_path = os.path.join(img_dir, f"{char}.png")
                img = Image.open(img_path)

                # update the position of the image
                image_pos.image(img, width=300)

                # wait for 2 seconds before displaying the next image
                time.sleep(2)

                # remove the image
                image_pos.empty()
            elif char == ' ':
                # display space image for space character
                img_path = os.path.join(img_dir, "space.png")
                img = Image.open(img_path)

                # update the position of the image
                image_pos.image(img, width=300)

                # wait for 2 seconds before displaying the next image
                time.sleep(2)

                # remove the image
                image_pos.empty()

        # wait for 2 seconds before removing the last image
        time.sleep(2)
        image_pos.empty()


    # add start button to start recording audio
    if st.button("Start Talking"):
        # record audio for 5 seconds
        with sr.Microphone() as source:
            st.write("Say something!")
            audio = r.listen(source, phrase_time_limit=5)

            try:
                text = r.recognize_google(audio)
            except sr.UnknownValueError:
                st.write("Sorry, I did not understand what you said.")
            except sr.RequestError as e:
                st.write(f"Could not request results from Google Speech Recognition service; {e}")

        # convert text to lowercase
        text = text.lower()
        # display the final result
        st.write(f"You said: {text}", font_size=41)

        # display sign language images
        display_images(text)