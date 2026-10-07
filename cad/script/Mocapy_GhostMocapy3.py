import FreeCAD as App
import Part
import math

# 新しいドキュメントを作成
doc = App.newDocument("Mocapy_Final_FaceSafe_Clean")

# --- パラメータ設定 (単位: mm) ---
head_r = 12.0       # 頭（頭巾）の半径
face_r = 10.0       # 顔の半径
body_r = 10.0       # 胴体の半径
limb_r = 3.8        # 手足の半径

# 触角のパラメータ
steam_r = 2.2
stem_r = 1.2
stem_h = 4.5

# 頑丈で鋭い三角の爪パラメータ
claw_base_r = 1.1
claw_h = 1.5
spread_angle = 25.0

# 顔のパーツパラメータ
eye_sphere_r = 2.6
eye_thickness = 0.4

# しっかり大きく開いた縦長口のパラメータ
mouth_radius = 1.8
mouth_h_half = 2.5
tongue_r = 1.5
fang_r = 0.4
fang_h = 1.2

# --- 1. 頭巾とお顔のベース作成 ---
hood_base = Part.makeSphere(head_r)
face_cutter = Part.makeSphere(face_r + 0.5)
face_cutter.translate(App.Base.Vector(-4.5, 0, 0))
hood = hood_base.cut(face_cutter)

face = Part.makeSphere(face_r)
face_center = App.Base.Vector(-2.0, 0, 0)
face.translate(face_center)

# 目
eye_sphere_l = Part.makeSphere(eye_sphere_r)
eye_sphere_r_part = Part.makeSphere(eye_sphere_r)
eye_sphere_l.translate(App.Base.Vector(-10.2, 3.2, 1.8))
eye_sphere_r_part.translate(App.Base.Vector(-10.2, -3.2, 1.8))
raw_eyes = eye_sphere_l.fuse(eye_sphere_r_part)

inner_face_sphere = Part.makeSphere(face_r)
inner_face_sphere.translate(face_center)
cookie_back_cut = raw_eyes.cut(inner_face_sphere)

outer_face_sphere = Part.makeSphere(face_r + eye_thickness + 0.2)
outer_face_sphere.translate(face_center)
perfect_soft_eyes = cookie_back_cut.common(outer_face_sphere)

# お口
m_top = Part.makeSphere(mouth_radius)
m_top.translate(App.Base.Vector(-11.5, 0, mouth_h_half))
m_bottom = Part.makeSphere(mouth_radius)
m_bottom.translate(App.Base.Vector(-11.5, 0, -mouth_h_half))

m_mid_cyl = Part.makeCylinder(mouth_radius, mouth_h_half * 2)
m_mid_cyl.translate(App.Base.Vector(-11.5, 0, -mouth_h_half))
mouth_capsule = m_top.fuse(m_bottom).fuse(m_mid_cyl)
mouth_capsule.translate(App.Base.Vector(0, 0, -4.7))

face_with_mouth = face.cut(mouth_capsule)

# ベロ・牙
tongue = Part.makeSphere(tongue_r)
tongue.translate(App.Base.Vector(-10.2, 0, -5.5))
tongue_clean = tongue.common(mouth_capsule)

fang_l = Part.makeCone(fang_r, 0.0, fang_h)
fang_l.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 180.0)
fang_l.translate(App.Base.Vector(-10.6, 0.8, -2.4))

fang_r_part = Part.makeCone(fang_r, 0.0, fang_h)
fang_r_part.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 180.0)
fang_r_part.translate(App.Base.Vector(-10.6, -0.8, -2.4))
fangs = fang_l.fuse(fang_r_part)

face_final = face_with_mouth.fuse(tongue_clean).fuse(fangs)

# お顔マスクの切り出し
face_mask_cutter = Part.makeBox(40, 40, 40)
face_mask_cutter.translate(App.Base.Vector(-44.5, -20, -20))

# パーツ①：お顔マスク
raw_mask = face_final.fuse(perfect_soft_eyes).common(face_mask_cutter)
final_face_mask = raw_mask.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 5.0)
final_face_mask.translate(App.Base.Vector(-3.0, 0, 1.2))

# 頭部フード部分
hood_remains = hood.fuse(face_final.fuse(perfect_soft_eyes).cut(face_mask_cutter))

# 触角
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

hood_total = hood_remains.fuse(antennas)
hood_total.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 5.0)
hood_total.translate(App.Base.Vector(-3.0, 0, 1.2))


# --- 2. 胴体と手足の作成 ---
body = Part.makeSphere(body_r)
body_pos = App.Base.Vector(3.6, 0, -11.0)
body.translate(body_pos)
body.rotate(body_pos, App.Base.Vector(0,1,0), -15.0)

def make_claws_for_limb(limb_pos, direction_vector):
    v_mid_dir = direction_vector.normalize()
    rot_axis = App.Base.Vector(0, 0, 1)
    rot_left = App.Rotation(rot_axis, spread_angle)
    rot_right = App.Rotation(rot_axis, -spread_angle)
    v_left_dir = rot_left.multVec(v_mid_dir)
    v_right_dir = rot_right.multVec(v_mid_dir)

    f_mid = Part.makeCone(claw_base_r, 0.0, claw_h)
    f_mid.Placement = App.Placement(App.Base.Vector(0,0,0), App.Rotation(App.Base.Vector(0,0,1), v_mid_dir))
    f_mid.translate(limb_pos + v_mid_dir * (limb_r - 0.5))

    f_left = Part.makeCone(claw_base_r, 0.0, claw_h)
    f_left.Placement = App.Placement(App.Base.Vector(0,0,0), App.Rotation(App.Base.Vector(0,0,1), v_left_dir))
    f_left.translate(limb_pos + v_left_dir * (limb_r - 0.5))

    f_right = Part.makeCone(claw_base_r, 0.0, claw_h)
    f_right.Placement = App.Placement(App.Base.Vector(0,0,0), App.Rotation(App.Base.Vector(0,0,1), v_right_dir))
    f_right.translate(limb_pos + v_right_dir * (limb_r - 0.5))
    return f_mid.fuse(f_left).fuse(f_right)

pos_arm_l = App.Base.Vector(0.0, 8.5, -10.5)
pos_arm_r = App.Base.Vector(0.0, -9.5, -10.5)
arm_l = Part.makeSphere(limb_r)
arm_l.translate(pos_arm_l)
arm_l = arm_l.fuse(make_claws_for_limb(pos_arm_l, App.Base.Vector(-1, 0.1, 0.2)))

arm_r = Part.makeSphere(limb_r)
arm_r.translate(pos_arm_r)
arm_r = arm_r.fuse(make_claws_for_limb(pos_arm_r, App.Base.Vector(-1, -0.1, 0.2)))

pos_leg_l = App.Base.Vector(-0.5, 5.8, -20.5)
pos_leg_r = App.Base.Vector(-0.5, -5.8, -20.5)

leg_l_sphere = Part.makeSphere(limb_r)
leg_l_sphere.translate(pos_leg_l)
leg_l = leg_l_sphere.fuse(make_claws_for_limb(pos_leg_l, App.Base.Vector(-1, 0.1, 0.0)))

leg_r_sphere = Part.makeSphere(limb_r)
leg_r_sphere.translate(pos_leg_r)
leg_r = leg_r_sphere.fuse(make_claws_for_limb(pos_leg_r, App.Base.Vector(-1, -0.1, 0.0)))

body_total = body.fuse(arm_l).fuse(arm_r).fuse(leg_l).fuse(leg_r)


# --- 3. 3分割 ＆ 足の裏だけピンポイント水平カット ---
lower_body_box = Part.makeBox(100, 100, 50)
lower_body_box.translate(App.Base.Vector(-50, -50, -61.0))
lower_body_raw = body_total.common(lower_body_box)

# 足の裏（最下部）だけを水平カット
foot_cutter = Part.makeBox(100, 100, 10)
foot_cutter.translate(App.Base.Vector(-50, -50, -32.5))
final_lower_body = lower_body_raw.cut(foot_cutter)

# 胴体の上半分を抽出してフードと結合
upper_body_raw = body_total.cut(lower_body_box)
final_hood_and_back = hood_total.fuse(upper_body_raw)


# --- 4. FreeCADの画面に出力 ---
obj_face = doc.addObject("Part::Feature", "GhostMocapy_FaceMask")
obj_face.Shape = final_face_mask
obj_face.ShapeColor = (0.95, 0.95, 1.0)

obj_hood = doc.addObject("Part::Feature", "GhostMocapy_HoodAndBack")
obj_hood.Shape = final_hood_and_back
obj_hood.ShapeColor = (0.85, 0.9, 0.95)

obj_lower = doc.addObject("Part::Feature", "GhostMocapy_LowerBody")
obj_lower.Shape = final_lower_body
obj_lower.ShapeColor = (0.75, 0.8, 0.85)

doc.recompute()

if App.GuiUp:
    try:
        App.Gui.ActiveDocument.ActiveView.viewReady()
        App.Gui.SendMsgToActiveView("ViewFit")
    except Exception:
        pass

print("【処理完了】FreeCADの画面上に3つのオブジェクトを生成しました。")
