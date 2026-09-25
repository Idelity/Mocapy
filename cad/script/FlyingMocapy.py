import FreeCAD as App
import Part
import math

# 新しいドキュメントを作成
doc = App.newDocument("FlyingMocapy")

# --- パラメータ設定 (単位: mm) キーホルダーサイズ ---
head_r = 12.0       # 頭（頭巾）の半径
face_r = 10.0       # 顔の半径
body_r = 10.0       # 胴体の半径
limb_r = 4.0        # 手足の半径
steam_r = 2.0       # 触角の先の丸の半径
stem_r = 1.2        # 触角の「太めの線（茎）」の半径
stem_h = 4.5        # 触角の茎の長さ
hole_r = 1.0        # キーチェーン用の穴の半径

# 指のパラメータ
finger_r = 0.55     # 指の半径
finger_h = 2.2      # 指の長さ
spread_angle = 30.0 # 指の開き角度

# 顔のパーツパラメータ
eye_sphere_r = 2.75
eye_thickness = 0.4
pupil_sphere_r = 0.7
mouth_radius = 1.75
mouth_width = 4.5
tongue_r = 1.5
fang_r = 0.4
fang_h = 1.2

# --- 1. 頭巾とお顔の作成 ---
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

pos_arm_l = App.Base.Vector(5.0, 11.0, -10.0)
pos_arm_r = App.Base.Vector(5.0, -11.0, -10.0)
pos_leg_l = App.Base.Vector(5.5, 5.0, -20.5)
pos_leg_r = App.Base.Vector(5.5, -5.0, -20.5)

# --- 指生成関数 ---
def make_fingers_horizontal(limb_pos):
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

# オブジェクトを作成してから個別にtranslateを実行 (関数名をmake_fingers_horizontalに修正)
arm_l_sphere = Part.makeSphere(limb_r)
arm_l_sphere.translate(pos_arm_l)
arm_l = arm_l_sphere.fuse(make_fingers_horizontal(pos_arm_l))

arm_r_sphere = Part.makeSphere(limb_r)
arm_r_sphere.translate(pos_arm_r)
arm_r = arm_r_sphere.fuse(make_fingers_horizontal(pos_arm_r))

leg_l_sphere = Part.makeSphere(limb_r)
leg_l_sphere.translate(pos_leg_l)
leg_l = leg_l_sphere.fuse(make_fingers_horizontal(pos_leg_l))

leg_r_sphere = Part.makeSphere(limb_r)
leg_r_sphere.translate(pos_leg_r)
leg_r = leg_r_sphere.fuse(make_fingers_horizontal(pos_leg_r))

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

# --- 3. FreeCADの画面に出力 (1つのオブジェクトとして出力) ---
obj_full = doc.addObject("Part::Feature", "FlyingMocapy_FULL")
obj_full.Shape = full_mocapy

doc.recompute()

# GUI環境のみで実行されるよう安全策を追加
if App.GuiUp:
    try:
        App.Gui.ActiveDocument.ActiveView.viewReady()
        App.Gui.SendMsgToActiveView("ViewFit")
    except Exception:
        pass

print("1つのソリッドモデルとして出力しました！")
