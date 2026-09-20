import FreeCAD as App
import Part
import math

# 新しいドキュメントを作成（キャッシュバグを完全にリセット）
doc = App.newDocument("Mocapy_Perfect_Mouth_Lower")

# --- パラメータ設定 (単位: mm) キーホルダーサイズ ---
head_r = 12.0       # 頭（頭巾）の半径
face_r = 10.0       # 顔の半径
body_r = 10.0       # 胴体の半径
limb_r = 4.0        # 手足の半径
steam_r = 2.0       # 触角の先の丸の半径
stem_r = 1.2        # 触角の「太めの線（茎）」の半径
stem_h = 4.5        # 触角の茎の長さ
hole_r = 1.0        # キーチェーン用の穴の半径

# 3本指のパラメータ
finger_r = 0.35     # 指の太さ
finger_h = 2.2      # 指の長さ
spread_angle = 30.0 # 指の開き角度

# 目・黒目のパラメータ
eye_sphere_r = 2.75 # 白目半径
eye_thickness = 0.4 # 白目厚み
pupil_sphere_r = 0.7 # 黒目半径

# お口・ベロ・牙のパラメータ
mouth_radius = 1.75 # くり抜き円柱の半径（縦幅3.5mm）
mouth_width = 4.5   # お口の横幅
tongue_r = 1.5      # 中ののぞくベロの球体半径
fang_r = 0.4        # 牙の太さ
fang_h = 1.2        # 牙の長さ

# --- 1. 頭巾（フード）とお顔の作成（左面への凹構造） ---
hood_base = Part.makeSphere(head_r)
face_cutter = Part.makeSphere(face_r + 0.5)
face_cutter.translate(App.Base.Vector(-4.5, 0, 0))
hood = hood_base.cut(face_cutter)

face = Part.makeSphere(face_r)
face_center = App.Base.Vector(-2.0, 0, 0)
face.translate(face_center)

# --- 2. お顔の曲面トレースクッキー目 ＆ まん丸見上げ黒目 ---
eye_sphere_l = Part.makeSphere(eye_sphere_r)
eye_sphere_r_part = Part.makeSphere(eye_sphere_r)
pos_l = App.Base.Vector(-10.2, 4.3, 0.8)
pos_r = App.Base.Vector(-10.2, -4.3, 0.8)
eye_sphere_l.translate(pos_l)
eye_sphere_r_part.translate(pos_r)
raw_eyes = eye_sphere_l.fuse(eye_sphere_r_part)

inner_face_sphere = Part.makeSphere(face_r)
inner_face_sphere.translate(face_center)
cookie_back_cut = raw_eyes.cut(inner_face_sphere)

outer_face_sphere = Part.makeSphere(face_r + eye_thickness + 0.2)
outer_face_sphere.translate(face_center)
perfect_soft_eyes = cookie_back_cut.common(outer_face_sphere)

pupil_l = Part.makeSphere(pupil_sphere_r)
pupil_l.translate(App.Base.Vector(-11.0, 4.1, 2.4))
pupil_r = Part.makeSphere(pupil_sphere_r)
pupil_r.translate(App.Base.Vector(-11.0, -4.1, 2.4))
pupils = pupil_l.fuse(pupil_r).cut(inner_face_sphere)

# --- 3. 【完全修正】お口の位置をさらに下（あご側）へずらしてくり抜く ---
m_cyl1 = Part.makeCylinder(mouth_radius, 10.0)
m_cyl1.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 90.0)
# 【修正】Z座標を「-1.8」から「-3.2」へ下げて配置
m_cyl1.translate(App.Base.Vector(-13.0, 1.2, -3.2))

m_cyl2 = Part.makeCylinder(mouth_radius, 10.0)
m_cyl2.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 90.0)
# 【修正】Z座標を「-1.8」から「-3.2」へ下げて配置
m_cyl2.translate(App.Base.Vector(-13.0, -1.2, -3.2))

m_box = Part.makeBox(10.0, 2.4, mouth_radius * 2)
# 【修正】Z座標を連動して引き下げ
m_box.translate(App.Base.Vector(-13.0, -1.2, -3.2 - mouth_radius))

mouth_cutter = m_cyl1.fuse(m_cyl2).fuse(m_box)

# お顔を楕円カッターで深くくり抜く
face_with_mouth = face.cut(mouth_cutter)

# 口の中から覗く「大きなベロ（球体）」
tongue = Part.makeSphere(tongue_r)
# 【修正】お口の位置に合わせてベロのZ座標も「-4.2」へ引き下げ
tongue.translate(App.Base.Vector(-10.2, 0, -4.2))
tongue_clean = tongue.common(mouth_cutter)

# 上のフチから生える「2本のちいさな牙（円錐）」
fang_l = Part.makeCone(fang_r, 0.0, fang_h)
fang_l.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 180.0)
# 【修正】お口の位置に合わせて牙のZ座標も「-1.6」へ引き下げ
fang_l.translate(App.Base.Vector(-10.5, 1.3, -1.6))

# 右の牙
fang_r_part = Part.makeCone(fang_r, 0.0, fang_h)
fang_r_part.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 180.0)
# 【修正】お口の位置に合わせて牙のZ座標も「-1.6」へ引き下げ
fang_r_part.translate(App.Base.Vector(-10.5, -1.3, -1.6))

# 牙を合体
fangs = fang_l.fuse(fang_r_part)

# くり抜いたお顔、ベロ、牙を全てドッキング
face_final = face_with_mouth.fuse(tongue_clean).fuse(fangs)

# 頭巾、完成したお顔、目をすべて合体
head_combined = hood.fuse(face_final).fuse(perfect_soft_eyes).fuse(pupils)

# --- 4. 胴体の作成と配置 ---
body = Part.makeSphere(body_r)
body_pos = App.Base.Vector(0, 0, -12.0)
body.translate(body_pos)

# 手足の位置定義
pos_arm_l = App.Base.Vector(3.0, 11.0, -10.0)
pos_arm_r = App.Base.Vector(3.0, -11.0, -10.0)
pos_leg_l = App.Base.Vector(5.5, 5.0, -20.5)
pos_leg_r = App.Base.Vector(5.5, -5.0, -20.5)

# --- 5. 手の指の生成（上下3本指：完璧バージョン） ---
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

# --- 6. 足の指の生成（左右3本指：完璧バージョン） ---
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

# --- 7. 手足と指のドッキング ---
arm_l = Part.makeSphere(limb_r)
arm_l.translate(pos_arm_l)
arm_l = arm_l.fuse(make_hand_fingers_vertical(pos_arm_l))

arm_r = Part.makeSphere(limb_r)
arm_r.translate(pos_arm_r)
arm_r = arm_r.fuse(make_hand_fingers_vertical(pos_arm_r))

leg_l = Part.makeSphere(limb_r)
leg_l.translate(pos_leg_l)
leg_l = leg_l.fuse(make_foot_fingers_horizontal_fixed(pos_leg_l))

leg_r = Part.makeSphere(limb_r)
leg_r.translate(pos_leg_r)
leg_r = leg_r.fuse(make_foot_fingers_horizontal_fixed(pos_leg_r))

# --- 8. 触角（ハの字＋前傾・接続済み：完璧バージョン） ---
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

# --- 9. キーチェーン用の横穴を開ける ---
key_hole = Part.makeCylinder(hole_r, 30.0)
key_hole.translate(App.Base.Vector(3.0, -15.0, head_r + 0.2))
antennas_with_hole = antennas.cut(key_hole)

# --- 10. すべてのパーツを合体 ---
final_mocapy = head_combined.fuse(body)
final_mocapy = final_mocapy.fuse(arm_l)
final_mocapy = final_mocapy.fuse(arm_r)
final_mocapy = final_mocapy.fuse(leg_l)
final_mocapy = final_mocapy.fuse(leg_r)
final_mocapy = final_mocapy.fuse(antennas_with_hole)

# --- 11. FreeCADの画面に出力 ---
obj = doc.addObject("Part::Feature", "Mocapy_Final_Lower_Mouth")
obj.Shape = final_mocapy

# 画面を更新して全体にフィット
doc.recompute()
App.Gui.ActiveDocument.ActiveView.viewReady()
App.Gui.SendMsgToActiveView("ViewFit")

print("お口の位置を少し下に下げて、ベストな顔立ちに再生成しました！")
