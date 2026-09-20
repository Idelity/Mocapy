import FreeCAD as App
import Part
import math

# 新しいドキュメントを作成（バグを完全にリセット）
doc = App.newDocument("Mocapy_Split_Perfect_Fingers")

# --- パラメータ設定 (単位: mm) キーホルダーサイズ ---
head_r = 12.0       # 頭（頭巾）の半径
face_r = 10.0       # 顔の半径
body_r = 10.0       # 胴体の半径
limb_r = 4.0        # 手足の半径
steam_r = 2.0       # 触角の先の丸の半径
stem_r = 1.2        # 触角の「太めの線（茎）」の半径
stem_h = 4.5        # 触角の茎の長さ
hole_r = 1.0        # キーチェーン用の穴の半径

# 【強化】指をしっかり太くもげにくく設定！
finger_r = 0.55     # 指の半径（直径1.1mmに強化！）
finger_h = 2.2      # 指の長さ
spread_angle = 30.0 # 指の開き角度

# 角丸クッキー目・黒目・お口のパラメータ
eye_sphere_r = 2.75
eye_thickness = 0.4
pupil_sphere_r = 0.7
mouth_radius = 1.75
mouth_width = 4.5
tongue_r = 1.5
fang_r = 0.4
fang_h = 1.2

# --- 1. 頭巾とお顔の作成（左面への凹構造：完璧バージョン） ---
hood_base = Part.makeSphere(head_r)
face_cutter = Part.makeSphere(face_r + 0.5)
face_cutter.translate(App.Base.Vector(-4.5, 0, 0))
hood = hood_base.cut(face_cutter)

face = Part.makeSphere(face_r)
face_center = App.Base.Vector(-2.0, 0, 0)
face.translate(face_center)

# お顔の曲面トレースクッキー目
eye_sphere_l = Part.makeSphere(eye_sphere_r)
eye_sphere_r_part = Part.makeSphere(eye_sphere_r)
eye_sphere_l.translate(App.Base.Vector(-10.2, 4.3, 0.8))
eye_sphere_r_part.translate(App.Base.Vector(-10.2, -4.3, 0.8))
raw_eyes = eye_sphere_l.fuse(eye_sphere_r_part)
inner_face_sphere = Part.makeSphere(face_r)
inner_face_sphere.translate(face_center)
cookie_back_cut = raw_eyes.cut(inner_face_sphere)
outer_face_sphere = Part.makeSphere(face_r + eye_thickness + 0.2)
outer_face_sphere.translate(face_center)
perfect_soft_eyes = cookie_back_cut.common(outer_face_sphere)

# 見上げ黒目
pupil_l = Part.makeSphere(pupil_sphere_r)
pupil_l.translate(App.Base.Vector(-11.0, 4.1, 2.4))
pupil_r = Part.makeSphere(pupil_sphere_r)
pupil_r.translate(App.Base.Vector(-11.0, -4.1, 2.4))
pupils = pupil_l.fuse(pupil_r).cut(inner_face_sphere)

# お口・ベロ・牙
m_cyl1 = Part.makeCylinder(mouth_radius, 10.0)
m_cyl1.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 90.0)
m_cyl1.translate(App.Base.Vector(-13.0, 1.2, -3.2))
m_cyl2 = Part.makeCylinder(mouth_radius, 10.0)
m_cyl2.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 90.0)
m_cyl2.translate(App.Base.Vector(-13.0, -1.2, -3.2))
m_box = Part.makeBox(10.0, 2.4, mouth_radius * 2)
m_box.translate(App.Base.Vector(-13.0, -1.2, -3.2 - mouth_radius))
mouth_cutter = m_cyl1.fuse(m_cyl2).fuse(m_box)
face_with_mouth = face.cut(mouth_cutter)

tongue = Part.makeSphere(tongue_r)
tongue.translate(App.Base.Vector(-10.2, 0, -4.2))
tongue_clean = tongue.common(mouth_cutter)

fang_l = Part.makeCone(fang_r, 0.0, fang_h)
fang_l.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 180.0)
fang_l.translate(App.Base.Vector(-10.5, 1.3, -1.6))
fang_r_part = Part.makeCone(fang_r, 0.0, fang_h)
fang_r_part.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 180.0)
fang_r_part.translate(App.Base.Vector(-10.5, -1.3, -1.6))
fangs = fang_l.fuse(fang_r_part)

face_final = face_with_mouth.fuse(tongue_clean).fuse(fangs)
head_combined = hood.fuse(face_final).fuse(perfect_soft_eyes).fuse(pupils)

# --- 2. 胴体・手足の位置定義 ---
body = Part.makeSphere(body_r)
body_pos = App.Base.Vector(0, 0, -12.0)
body.translate(body_pos)

pos_arm_l = App.Base.Vector(3.0, 11.0, -10.0)
pos_arm_r = App.Base.Vector(3.0, -11.0, -10.0)
pos_leg_l = App.Base.Vector(5.5, 5.0, -20.5)
pos_leg_r = App.Base.Vector(5.5, -5.0, -20.5)

# --- 指生成関数（バグのない独立したソリッド結合処理） ---
def make_hand_fingers_vertical(limb_pos):
    v_dir = limb_pos - body_pos
    rot_base = App.Rotation(App.Base.Vector(0, 0, 1), v_dir)
    f_mid = Part.makeCylinder(finger_r, finger_h + 1.0)
    f_up = Part.makeCylinder(finger_r, finger_h + 1.0)
    f_up.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), -spread_angle)
    f_down = Part.makeCylinder(finger_r, finger_h + 1.0)
    f_down.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), spread_angle)
    fingers = f_mid.fuse(f_up).fuse(f_down)
    fingers.Placement = App.Placement(App.Base.Vector(0, 0, 0), rot_base)
    fingers.translate(limb_pos + v_dir.normalize() * (limb_r - 0.8))
    return fingers

def make_foot_fingers_horizontal_fixed(limb_pos):
    v_dir = limb_pos - body_pos
    v_mid_dir = v_dir.normalize()
    rot_left = App.Rotation(App.Base.Vector(0, 0, 1), spread_angle)
    rot_right = App.Rotation(App.Base.Vector(0, 0, 1), -spread_angle)
    v_left_dir = rot_left.multVec(v_mid_dir)
    v_right_dir = rot_right.multVec(v_mid_dir)
    
    f_mid = Part.makeCylinder(finger_r, finger_h + 1.0)
    f_mid.Placement = App.Placement(App.Base.Vector(0,0,0), App.Rotation(App.Base.Vector(0,0,1), v_mid_dir))
    f_mid.translate(limb_pos + v_mid_dir * (limb_r - 0.8))
    
    f_left = Part.makeCylinder(finger_r, finger_h + 1.0)
    f_left.Placement = App.Placement(App.Base.Vector(0,0,0), App.Rotation(App.Base.Vector(0,0,1), v_left_dir))
    f_left.translate(limb_pos + v_left_dir * (limb_r - 0.8))
    
    f_right = Part.makeCylinder(finger_r, finger_h + 1.0)
    f_right.Placement = App.Placement(App.Base.Vector(0,0,0), App.Rotation(App.Base.Vector(0,0,1), v_right_dir))
    f_right.translate(limb_pos + v_right_dir * (limb_r - 0.8))
    
    return f_mid.fuse(f_left).fuse(f_right)

# 【バグ完全修正】球体と強化された3本指を確実にドッキングさせてから移動・配置
arm_l_sphere = Part.makeSphere(limb_r).translate(pos_arm_l)
arm_l = arm_l_sphere.fuse(make_hand_fingers_vertical(pos_arm_l))

arm_r_sphere = Part.makeSphere(limb_r).translate(pos_arm_r)
arm_r = arm_r_sphere.fuse(make_hand_fingers_vertical(pos_arm_r))

leg_l_sphere = Part.makeSphere(limb_r).translate(pos_leg_l)
leg_l = leg_l_sphere.fuse(make_foot_fingers_horizontal_fixed(pos_leg_l))

leg_r_sphere = Part.makeSphere(limb_r).translate(pos_leg_r)
leg_r = leg_r_sphere.fuse(make_foot_fingers_horizontal_fixed(pos_leg_r))

# 触角とキーチェーン穴
stem_l = Part.makeCylinder(stem_r, stem_h)
ball_l = Part.makeSphere(steam_r)
ball_l.translate(App.Base.Vector(0, 0, stem_h))
antenna_l = stem_l.fuse(ball_l)
antenna_l.rotate(App.Base.Vector(0,0,0), App.Base.Vector(1,0,0), -20.0)
antenna_l.translate(App.Base.Vector(0, 6.5, 0))

stem_r_part = Part.makeCylinder(stem_r, stem_h)
ball_r = Part.makeSphere(steam_r)
ball_r.translate(App.Base.Vector(0, 0, stem_h))
antenna_r = stem_r_part.fuse(ball_r)
antenna_r.rotate(App.Base.Vector(0,0,0), App.Base.Vector(1,0,0), 20.0)
antenna_r.translate(App.Base.Vector(0, -6.5, 0))

antennas = antenna_l.fuse(antenna_r)
antennas.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 15.0)
antennas.translate(App.Base.Vector(3.0, 0.0, head_r - 3.2))

key_hole = Part.makeCylinder(hole_r, 30.0)
key_hole.translate(App.Base.Vector(3.0, -15.0, head_r + 0.2))
antennas_with_hole = antennas.cut(key_hole)

# 全身の完全一体化ソリッド
full_mocapy = head_combined.fuse(body).fuse(arm_l).fuse(arm_r).fuse(leg_l).fuse(leg_r).fuse(antennas_with_hole)

# --- 3. 全身モデルを前後に綺麗に2分割する ---
slice_box_front = Part.makeBox(50, 50, 60)
slice_box_front.translate(App.Base.Vector(-50, -25, -35)) # 前面（お顔・手足の指側）

slice_box_back = Part.makeBox(50, 50, 60)
slice_box_back.translate(App.Base.Vector(0, -25, -35)) # 背中側

front_part = full_mocapy.common(slice_box_front)
back_part = full_mocapy.common(slice_box_back)

# スライサーで見やすいように後面パーツを右側（Y軸+25mm）に並べる
back_part.translate(App.Base.Vector(0, 25.0, 0))

# --- 4. FreeCADの画面に出力 ---
obj_front = doc.addObject("Part::Feature", "Mocapy_FRONT_Reinforced_Fingers")
obj_front.Shape = front_part

obj_back = doc.addObject("Part::Feature", "Mocapy_BACK_Reinforced_Fingers")
obj_back.Shape = back_part

doc.recompute()
App.Gui.ActiveDocument.ActiveView.viewReady()
App.Gui.SendMsgToActiveView("ViewFit")

print("バグを修正し、頼もしく太くなった3本指付きのまま前後に2分割しました！")

