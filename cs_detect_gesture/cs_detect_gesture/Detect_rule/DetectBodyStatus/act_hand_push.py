# coding:utf-8
from collections import deque
import numpy as np
import math
import os
import configparser
import pyrr as py

class Act_Hand_Push:
    def __init__(self, threshold=20, window_size=5):
        # 肘基準で拳が動き続ける状態 1.0s平均で、しきい値以上の運動をしているか？
        # 読み込み用軸パラメータ
        self.axis = axis = 3
        self.window_size = window_size
        # しきい値^
        self.threshold = threshold

        # 設定読み込み
        inifile = configparser.ConfigParser()
        inifile.read(os.path.dirname(os.path.abspath(__file__)) + '/../../../../../../config.ini', 'UTF-8')
        self.hand_ht = inifile.getint('gesture_recognition','hand_ht')

        # 計算入力
        self.r_wrist = np.zeros((axis))
        self.l_wrist = np.zeros((axis))
        self.r_elbow = np.zeros((axis))
        self.l_elbow = np.zeros((axis))
        self.r_handtip = np.zeros((axis))
        self.l_handtip = np.zeros((axis))
        self.r_hand = np.zeros((axis))
        self.l_hand = np.zeros((axis))
        self.r_thumb = np.zeros((axis))
        self.l_thumb = np.zeros((axis))
        self.head = np.zeros((axis))
        self.chest = np.zeros((axis))
        self.naval = np.zeros((axis))
        self.nose = np.zeros((axis))

        self.is_r_hand_push = 0
        self.is_l_hand_push = 0
        self.is_hand_push = 0

        # Get config file stuff
        # self.seed_naval_z_dist = inifile.getint('gesture_recognition','seed_naval_z_dist')
        self.arm_stretch_thresh = 0.85
        #Generate the screen as a plan to determine the intercept point with the push direction
        self.screen_point_1 = np.array([0, 0, 500]) #Temporary dummy values - change to real values when known
        self.screen_point_2 = np.array([50, 0, 500])
        self.screen_point_3 = np.array([0, 50, 500])
        self.screen_plane = py.plane.create_from_points(self.screen_point_1, self.screen_point_2, self.screen_point_3)

    def calculate(self,
                  r_wrist=np.zeros(3),
                  l_wrist=np.zeros(3),
                  r_elbow=np.zeros(3),
                  l_elbow=np.zeros(3),
                  r_handtip=np.zeros(3),
                  l_handtip=np.zeros(3),
                  r_hand=np.zeros(3),
                  l_hand=np.zeros(3),
                  r_shoulder=np.zeros(3),
                  l_shoulder=np.zeros(3),
                  head=np.zeros(3),
                  chest=np.zeros(3),
                  naval=np.zeros(3),
                  nose=np.zeros(3),
                  is_data=False):
        # 初期値
        self.is_hand_push = 0
        self.is_l_hand_push = 0
        self.is_r_hand_push = 0

        self.r_pushb_intersect = [0,0,0]
        self.l_pushb_intersect = [0,0,0]

        x_idx = 0
        y_idx = 1
        z_idx = 2


        if (is_data):
            #Prelim Calcs
            #Arm length
            r_wr_len = math.sqrt((r_wrist[0]-r_elbow[0])**2 + (r_wrist[1]-r_elbow[1])**2 + (r_wrist[2]-r_elbow[2])**2)
            l_wr_len = math.sqrt((l_wrist[0]-l_elbow[0])**2 + (l_wrist[1]-l_elbow[1])**2 + (l_wrist[2]-l_elbow[2])**2)
            #Elbow to chest
            r_el_sh_len = math.sqrt((r_elbow[0]-r_shoulder[0])**2 + (r_elbow[1]-r_shoulder[1])**2 + (r_elbow[2]-r_shoulder[2])**2)
            l_el_sh_len = math.sqrt((l_elbow[0]-l_shoulder[0])**2 + (l_elbow[1]-l_shoulder[1])**2 + (l_elbow[2]-l_shoulder[2])**2)
            # Trigger arm length
            r_max_arm_length = (r_wr_len + r_el_sh_len) * self.arm_stretch_thresh
            l_max_arm_length = (l_wr_len + l_el_sh_len) * self.arm_stretch_thresh
            # Current arm length
            r_curr_arm_length = math.sqrt((r_wrist[0]-r_shoulder[0])**2 + (r_wrist[1]-r_shoulder[1])**2 + (r_wrist[2]-r_shoulder[2])**2)
            l_curr_arm_length = math.sqrt((l_wrist[0]-l_shoulder[0])**2 + (l_wrist[1]-l_shoulder[1])**2 + (l_wrist[2]-l_shoulder[2])**2)
            # Arm ratio
            r_ratio = r_curr_arm_length/r_max_arm_length
            l_ratio = l_curr_arm_length/l_max_arm_length

            #Push Direction
            push_dir_lx = l_wrist[0] - head[0]
            push_dir_ly = l_wrist[1] - head[1]
            push_dir_lz = l_wrist[2] - head[2]
            l_push_dir = np.array([push_dir_lx,push_dir_ly,push_dir_lz])

            push_dir_rx = r_wrist[0] - head[0]
            push_dir_ry = r_wrist[1] - head[1]
            push_dir_rz = r_wrist[2] - head[2]
            r_push_dir = np.array([push_dir_rx,push_dir_ry,push_dir_rz])

            # Determine intersection between push and screen
            push_dir_ray_l = py.ray.create(head, l_push_dir)
            intersect_l = py.geometric_tests.ray_intersect_plane(push_dir_ray_l, self.screen_plane, False)
            push_dir_ray_r = py.ray.create(head, r_push_dir)
            intersect_r = py.geometric_tests.ray_intersect_plane(push_dir_ray_r, self.screen_plane, False)

            # Determine if a push happens
            if r_wrist[y_idx] < naval[y_idx]:
                if r_curr_arm_length >= r_max_arm_length:
                    self.is_r_hand_push = 1
                    self.r_pushb_intersect = intersect_r

            if l_wrist[y_idx] < naval[y_idx]:
                if l_curr_arm_length >= l_max_arm_length:
                    self.is_l_hand_push = 1
                    self.l_pushb_intersect = intersect_l


            up_val = []
            up_val.append(self.is_l_hand_push)
            up_val.append(self.is_r_hand_push)
            self.is_hand_push = max(up_val)

        return self.is_hand_push, self.is_r_hand_push, self.is_l_hand_push #,self.l_pushb_intersect, self.r_pushb_intersect
