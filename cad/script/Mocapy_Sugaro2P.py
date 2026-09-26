import FreeCAD as App
import Part
import math
import os

try:
    App.closeDocument("Mocapy_Sugaro")
except Exception:
    pass

doc = App.newDocument("Mocapy_Sugaro")

# --- パラメータ設定 (単位: mm) ---
head_r = 10.6        # フードの横壁を肉厚にするためのベースサイズ
body_bottom_r = 12.8 # 裾のふくらみの肉厚サイズ
body_h = 16.0       # 布かぶりの高さ

# 顔のパラメータ
face_out_r = 9.3     # お顔の半径
# フードの窓を小さく（9.8 → 9.5）して境界をシャープにし、お顔との間に綺麗な段差を作ります
hood_window_r = 9.5

# 目のサイズ
eye_w = 7.8
eye_h = 4.0
eye_thick = 2.5

# くぼみ黒目（瞳）のパラメータ
kurome_r = 1.2
kurome_depth = 1.5

# 正方形(1.2mm x 1.2mm)の歯のサイズ
tooth_w = 1.20
tooth_h = 1.20
tooth_d = 1.4

# 手のパラメータ
param_hand_r = 2.4

# 人間の指のパラメータ
finger_r = 0.6
finger_len = 2.86

# 本物の丸いコイン（羽）のパラメータ
coin_r_upper = 4.4
coin_r_lower = 2.2
coin_t = 0.8

# --- 1. 布かぶりボディのベース作成 (寸胴体型) ---
head_sphere = Part.makeSphere(head_r)
head_sphere.translate(App.Base.Vector(0, 0, 8.0))

cloth_base = Part.makeCone(body_bottom_r, head_r - 0.2, body_h)
cloth_base.translate(App.Base.Vector(0, 0, -8.0))

cloth_body = head_sphere.fuse(cloth_base)

# --- 2. フードの窓をくり抜く (境界線のクッキリ段差表現) ---
# 窓カッターの位置を少し手前（X=-2.3）に引くことで、フードのフチに立体的な影（段差溝）を作ります
hood_cutter = Part.makeSphere(hood_window_r)
hood_cutter.translate(App.Base.Vector(-2.3, 0, 7.8))

body_with_hood_hole = cloth_body.cut(hood_cutter)

# --- 3. 奥に配置する顔の作成と口のくり抜き ---
# 【分離の完全解決】お顔の肉を後ろ（X=-0.8）までしっかり持たせ、X=0の分割線で絶対に千切れない強固な接続を作ります
face_with_mouth_base = Part.makeSphere(face_out_r)
face_with_mouth_base.translate(App.Base.Vector(-0.8, 0, 7.8))

# ■ 大きな口のカッター
mouth_w_half = 2.7
mouth_r = 1.3
mouth_z_base = 5.2

mouth_box = Part.makeBox(10.0, mouth_w_half * 2, mouth_r * 2)
mouth_box.translate(App.Base.Vector(-5.0, -mouth_w_half, mouth_z_base))

mouth_cyl_l = Part.makeCylinder(mouth_r, 10.0)
mouth_cyl_l.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 90.0)
mouth_cyl_l.translate(App.Base.Vector(-5.0, -mouth_w_half, mouth_z_base + mouth_r))

mouth_cyl_r = Part.makeCylinder(mouth_r, 10.0)
mouth_cyl_r.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 90.0)
mouth_cyl_r.translate(App.Base.Vector(-5.0, mouth_w_half, mouth_z_base + mouth_r))

mouth_cutter = mouth_box.fuse(mouth_cyl_l).fuse(mouth_cyl_r)
mouth_cutter.translate(App.Base.Vector(-7.6, 0, 0))

face_with_mouth = face_with_mouth_base.cut(mouth_cutter)

# --- 4. 出っ張り垂れ目（白目・メガネ） ---
# お顔の位置に合わせて目の埋め込み深さを調整
eye_left = Part.makeCylinder(eye_h / 2, eye_thick, App.Base.Vector(-7.6, 3.4, 10.1), App.Base.Vector(-1, 0, 0))
eye_left.scale(App.Base.Vector(1.0, eye_w / eye_h, 1.0))
eye_left.rotate(App.Base.Vector(-7.6, 3.4, 10.1), App.Base.Vector(1, 0, 0), -15.0)

eye_right = Part.makeCylinder(eye_h / 2, eye_thick, App.Base.Vector(-7.6, -3.4, 10.1), App.Base.Vector(-1, 0, 0))
eye_right.scale(App.Base.Vector(1.0, eye_w / eye_h, 1.0))
eye_right.rotate(App.Base.Vector(-7.6, -3.2, 10.1), App.Base.Vector(1, 0, 0), 15.0)

face_with_eyes = face_with_mouth.fuse(eye_left).fuse(eye_right)

# --- 5. 上下の歯の結合 ---
# 口の奥にきれいに並ぶよう、歯の座標を再計算
teeth_list = []
upper_y_positions = [-2.2, -0.7, 0.7, 2.2]
for y in upper_y_positions:
    tooth = Part.makeBox(tooth_d, tooth_w, tooth_h)
    tooth.translate(App.Base.Vector(-9.4, y - (tooth_w/2), mouth_z_base + 1.4))
    teeth_list.append(tooth)

lower_y_positions = [-1.5, 0.0, 1.5]
for y in lower_y_positions:
    tooth = Part.makeBox(tooth_d, tooth_w, tooth_h)
    tooth.translate(App.Base.Vector(-8.9, y - (tooth_w/2), mouth_z_base - 0.1))
    teeth_list.append(tooth)

all_teeth = teeth_list
for t in teeth_list[1:]:
    all_teeth = all_teeth.fuse(t)

complete_face = face_with_eyes.fuse(all_teeth)

# 服の本体とお顔をここで完全に結合（変な外部カットは一切行いません）
character_base = body_with_hood_hole.fuse(complete_face)

# --- 6. 右手・左手と3本指の組み立て ---
hand_left = Part.makeSphere(param_hand_r)
hand_left.translate(App.Base.Vector(-10.2, 3.3, -1.2))

hand_right = Part.makeSphere(param_hand_r)
hand_right.translate(App.Base.Vector(-10.2, -3.4, -1.2))

def make_perfect_human_finger(is_left, angle_deg):
    cyl = Part.makeCylinder(finger_r, finger_len)
    sph = Part.makeSphere(finger_r)
    sph.translate(App.Base.Vector(0, 0, finger_len))
    single_fin = cyl.fuse(sph)
    
    single_fin.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), -90.0)
    single_fin.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), -45.0)
    single_fin.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,0,1), angle_deg)
    
    hy = 3.3 if is_left else -3.4
    single_fin.translate(App.Base.Vector(-11.0, hy, -1.2))
    return single_fin

fin_l1 = make_perfect_human_finger(True, -50.0)
fin_l2 = make_perfect_human_finger(True, 0.0)
fin_l3 = make_perfect_human_finger(True, 50.0)
hand_left = hand_left.fuse(fin_l1).fuse(fin_l2).fuse(fin_l3)

fin_r1 = make_perfect_human_finger(False, -50.0)
fin_r2 = make_perfect_human_finger(False, 0.0)
fin_r3 = make_perfect_human_finger(False, 50.0)
hand_right = hand_right.fuse(fin_r1).fuse(fin_r2).fuse(fin_r3)

# --- 7. 角度を逆（内すぼまり）に傾けて刺した丸いコイン（上下計4枚） ---
angle_rad_coin = math.radians(45.0)
dir_x_coin = math.sin(angle_rad_coin)
dir_y_coin = math.cos(angle_rad_coin)

coin_l_up = Part.makeCylinder(coin_r_upper, coin_t, App.Base.Vector(9.8, 1.8, 2.5), App.Base.Vector(dir_x_coin, -dir_y_coin, 0))
coin_r_up = Part.makeCylinder(coin_r_upper, coin_t, App.Base.Vector(9.8, -1.8 - coin_t, 2.5), App.Base.Vector(dir_x_coin, dir_y_coin, 0))

coin_l_lo = Part.makeCylinder(coin_r_lower, coin_t, App.Base.Vector(10.2, 1.8, -1.5), App.Base.Vector(dir_x_coin, -dir_y_coin, 0))
coin_r_lo = Part.makeCylinder(coin_r_lower, coin_t, App.Base.Vector(10.2, -1.8 - coin_t, -1.5), App.Base.Vector(dir_x_coin, dir_y_coin, 0))

all_wings = coin_l_up.fuse(coin_r_up).fuse(coin_l_lo).fuse(coin_r_lo)

# 全体を合体
pre_sugaro_shape = character_base.fuse(hand_left).fuse(hand_right).fuse(all_wings)
pre_sugaro_shape.translate(App.Base.Vector(0, 0, 8.0))

# --- 8. 出っ張り垂れ目の表面から黒目をくり抜く ---
kurome_cutter_l = Part.makeCylinder(kurome_r, 10.0, App.Base.Vector(-14.2, 3.4, 18.1), App.Base.Vector(1, 0, 0))
kurome_cutter_r = Part.makeCylinder(kurome_r, 10.0, App.Base.Vector(-14.2, -3.4, 18.1), App.Base.Vector(1, 0, 0))
full_sugaro_shape = pre_sugaro_shape.cut(kurome_cutter_l).cut(kurome_cutter_r)

# --- 9. 前後2分割カット処理 (X=0) ---
split_box_front = Part.makeBox(40.0, 60.0, 60.0, App.Base.Vector(-40.0, -30.0, -10.0))
split_box_back = Part.makeBox(40.0, 60.0, 60.0, App.Base.Vector(0.0, -30.0, -10.0))

shape_front = full_sugaro_shape.common(split_box_front)
shape_back = full_sugaro_shape.common(split_box_back)

obj_front = doc.addObject("Part::Feature", "Sugaro_Front")
obj_front.Shape = shape_front

obj_back = doc.addObject("Part::Feature", "Sugaro_Back")
obj_back.Shape = shape_back

doc.recompute()

# カラー割り当て
if App.GuiUp:
    try:
        App.Gui.ActiveDocument.getObject("Sugaro_Front").ShapeColor = (0.85, 0.85, 0.85)
        App.Gui.ActiveDocument.getObject("Sugaro_Back").ShapeColor = (0.75, 0.75, 0.75)
        App.Gui.ActiveDocument.ActiveView.viewReady()
        App.Gui.SendMsgToActiveView("ViewFit")
    except Exception as e:
        print(f"Coloring Error: {e}")

doc.recompute()

# --- パソコンのデスクトップへ自動保存 ---
try:
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_front = os.path.join(desktop_path, "Sugaro_Front.stl")
    file_back = os.path.join(desktop_path, "Sugaro_Back.stl")
    
    Part.export([obj_front], file_front)
    Part.export([obj_back], file_back)
    print(f"🎉 口の崩れを完全防御し、構造接続をガッチリ強化した2分割ファイルをデスクトップに出力しました！")
except Exception as e:
    print(f"Export Error: {e}")

