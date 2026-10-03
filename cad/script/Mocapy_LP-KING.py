import FreeCAD as App
import Part
import math

doc = App.newDocument("Mocapy_LP_King")

# --- パラメータ設定 ---
body_r = 12.0
crown_h = 4.5
staff_r = 1.2          # 腕の連動用パラメータ
arm_r = staff_r
hand_r = 3.2           # 手を一回り大きく（3.2）
staff_h = 15.0        # 杖の長さを15.0に維持
lantern_r = 3.5        # ランタンを一回り大きく（3.5）

cape_top_w = 8.0
cape_bottom_w = 20.0
cape_height = 12.0
cape_thick = 2.5       # 厚み2.5mm
round_r = 3.0
collar_sphere_r = 2.2  # マントを抑える丸ボタン（2.2）

mus_top_w = 2.0
mus_bottom_w = 7.0
mus_height = 2.2
mus_thick = 0.8

eye_sphere_r = 2.5
mouth_r = 2.2

pumpkin_sphere = Part.makeSphere(body_r)

mat = App.Matrix()
mat.scale(1.45, 1.60, 1.15)
pumpkin_base = pumpkin_sphere.transformGeometry(mat)

# カボチャの底面カット位置は Z = -9.2
bottom_cutter = Part.makeBox(50.0, 50.0, 10.0)
bottom_cutter.translate(App.Base.Vector(-25.0, -25.0, -10.0 - (body_r - 2.8)))
pumpkin_body = pumpkin_base.cut(bottom_cutter)

for angle in range(0, 360, 45):
    rib_sphere = Part.makeSphere(body_r * 0.90)
    rib_base = rib_sphere.transformGeometry(mat)
    rad = math.radians(angle)
    rib_base.translate(App.Base.Vector(math.cos(rad) * 2.8 * 1.45, math.sin(rad) * 2.8 * 1.60, 0))
    pumpkin_body = pumpkin_body.cut(pumpkin_base.cut(rib_base))

# 左右の目のX座標（奥側 -11.0）
raw_eye_l = Part.makeSphere(eye_sphere_r)
raw_eye_l.translate(App.Base.Vector(-11.0, 4.8, 1.2))
big_cutter_l = Part.makeSphere(40.0)
big_cutter_l.translate(App.Base.Vector(-50.7, 0.0, 1.2))
big_cutter_l.rotate(App.Base.Vector(-11.0, 4.8, 1.2), App.Base.Vector(0,0,1), 330.0)
eye_l = raw_eye_l.cut(big_cutter_l)

raw_eye_r = Part.makeSphere(eye_sphere_r)
raw_eye_r.translate(App.Base.Vector(-11.0, -4.8, 1.2))
big_cutter_r = Part.makeSphere(40.0)
big_cutter_r.translate(App.Base.Vector(-50.7, 0.0, 1.2))
big_cutter_r.rotate(App.Base.Vector(-11.0, -4.8, 1.2), App.Base.Vector(0,0,1), 30.0)
eye_r = raw_eye_r.cut(big_cutter_r)

combined_eyes = eye_l.fuse(eye_r)

center_p = App.Base.Vector(0, 0, 0)
edge_l_p = App.Base.Vector(0, -mouth_r, 0)
edge_r_p = App.Base.Vector(0, mouth_r, 0)
bottom_p = App.Base.Vector(0, 0, -mouth_r)

arc = Part.Arc(edge_l_p, bottom_p, edge_r_p)
line = Part.LineSegment(edge_r_p, edge_l_p)
mouth_wire = Part.Wire([arc.toShape(), line.toShape()])
mouth_face = Part.Face(mouth_wire)

true_top_edge_mouth = mouth_face.extrude(App.Base.Vector(10.0, 0, 0))

true_top_edge_mouth.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 90.0)
true_top_edge_mouth.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 270.0)

true_top_edge_mouth.translate(App.Base.Vector(-13.5, 0.0, -1.5))
smile_mouth_cutter = true_top_edge_mouth

m1 = App.Base.Vector(0, -mus_top_w / 2.0, mus_height)
m2 = App.Base.Vector(0, mus_top_w / 2.0, mus_height)
m3 = App.Base.Vector(0, mus_bottom_w / 2.0, 0)
m4 = App.Base.Vector(0, -mus_bottom_w / 2.0, 0)

mustache_wire = Part.makePolygon([m1, m2, m3, m4, m1])
mustache_face = Part.Face(mustache_wire)
true_trapezoid_mustache = mustache_face.extrude(App.Base.Vector(mus_thick, 0, 0))
true_trapezoid_mustache.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 15.0)
true_trapezoid_mustache.translate(App.Base.Vector(-12.2, 0.0, -0.7))

body_face = pumpkin_body.cut(smile_mouth_cutter).fuse(combined_eyes).fuse(true_trapezoid_mustache)

# --- 王冠（トゲと上の丸大サイズ） ---
crown_center = Part.makeCylinder(5.0, crown_h)
spikes = []
for i in range(6):
    angle_deg = i * 60.0
    rad = math.radians(angle_deg)
    
    spike_cone = Part.makeCone(2.0, 0.0, 2.8)
    spike_cone.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 15.0)
    
    tip_sphere = Part.makeSphere(1.5)
    tip_sphere.translate(App.Base.Vector(0.0, 0.0, 2.7))
    tip_sphere.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 15.0)
    
    safe_spike = spike_cone.fuse(tip_sphere)
    safe_spike.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,0,1), angle_deg)
    
    safe_spike.translate(App.Base.Vector(math.cos(rad) * 3.0, math.sin(rad) * 3.0, crown_h - 0.5))
    spikes.append(safe_spike)

real_crown = crown_center
for s in spikes:
    real_crown = real_crown.fuse(s)

real_crown.translate(App.Base.Vector(0.0, 0.0, 8.6))
body_crown = body_face.fuse(real_crown)

# --- マント（厚み2.5mm＆オリジナルカッター処理） ---
p1 = App.Base.Vector(0, -cape_top_w / 2.0, cape_height)
p2 = App.Base.Vector(0, cape_top_w / 2.0, cape_height)
p3 = App.Base.Vector(0, cape_bottom_w / 2.0, 0)
p4 = App.Base.Vector(0, -cape_bottom_w / 2.0, 0)

trapezoid_wire = Part.makePolygon([p1, p2, p3, p4, p1])
trapezoid_face = Part.Face(trapezoid_wire)
trapezoid_cape = trapezoid_face.extrude(App.Base.Vector(cape_thick, 0, 0))

r_box_l = Part.makeBox(cape_thick + 2.0, round_r, round_r)
r_box_l.translate(App.Base.Vector(-1.0, cape_bottom_w/2.0 - round_r, 0))
r_cyl_l = Part.makeCylinder(round_r, cape_thick + 4.0)
r_cyl_l.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 90.0)
r_cyl_l.translate(App.Base.Vector(-2.0, cape_bottom_w/2.0 - round_r, round_r))
corner_cutter_l = r_box_l.cut(r_cyl_l)

r_box_r = Part.makeBox(cape_thick + 2.0, round_r, round_r)
r_box_r.translate(App.Base.Vector(-1.0, -cape_bottom_w/2.0, 0))
r_cyl_r = Part.makeCylinder(round_r, cape_thick + 4.0)
r_cyl_r.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 90.0)
r_cyl_r.translate(App.Base.Vector(-2.0, -cape_bottom_w/2.0 + round_r, round_r))
corner_cutter_r = r_box_r.cut(r_cyl_r)

round_trapezoid_cape = trapezoid_cape.cut(corner_cutter_l).cut(corner_cutter_r)

round_trapezoid_cape.translate(App.Base.Vector(8.2, 0.0, -10.0))
round_trapezoid_cape.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), -15.0)

# 首元丸ボタン
collar_sphere_base_l = Part.makeSphere(collar_sphere_r)
collar_box_l = Part.makeBox(collar_sphere_r * 2.0, collar_sphere_r * 2.0, collar_sphere_r)
collar_box_l.translate(App.Base.Vector(-collar_sphere_r, -collar_sphere_r, 0.0))
collar_half_l = collar_sphere_base_l.cut(collar_box_l)
collar_half_l.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 90.0)
collar_half_l.translate(App.Base.Vector(11.2, 5.6, -2.2))
collar_half_l.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), -15.0)

collar_sphere_base_r = Part.makeSphere(collar_sphere_r)
collar_box_r = Part.makeBox(collar_sphere_r * 2.0, collar_sphere_r * 2.0, collar_sphere_r)
collar_box_r.translate(App.Base.Vector(-collar_sphere_r, -collar_sphere_r, 0.0))
collar_half_r = collar_sphere_base_r.cut(collar_box_r)
collar_half_r.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), 90.0)
collar_half_r.translate(App.Base.Vector(11.2, -5.6, -2.2))
collar_half_r.rotate(App.Base.Vector(0,0,0), App.Base.Vector(0,1,0), -15.0)

body_with_cape = body_crown.fuse(round_trapezoid_cape)
body_cape_collar = body_with_cape.fuse(collar_half_l).fuse(collar_half_r)

# --- 【修正】両腕を少し伸ばし、手の位置を外側へシフト ---
arm_len = 18.0  # 腕の長さを 16.5 から 18.0 へ延長

arm_l_cyl = Part.makeCylinder(arm_r, arm_len)
arm_l_cyl.rotate(App.Base.Vector(0,0,0), App.Base.Vector(1,0,0), 90.0)
arm_l_cyl.translate(App.Base.Vector(-2.0, 1.0, -2.0))
hand_l = Part.makeSphere(hand_r)
hand_l.translate(App.Base.Vector(-2.0, arm_len - 1.0, -2.0)) # 延長に合わせて Y=17.0 へ配置
arm_and_hand_l = arm_l_cyl.fuse(hand_l)

arm_r_cyl = Part.makeCylinder(arm_r, arm_len)
arm_r_cyl.rotate(App.Base.Vector(0,0,0), App.Base.Vector(1,0,0), -90.0)
arm_r_cyl.translate(App.Base.Vector(-2.0, -1.0, -2.0))
hand_r = Part.makeSphere(hand_r)
hand_r.translate(App.Base.Vector(-2.0, -(arm_len - 1.0), -2.0)) # 延長に合わせて Y=-17.0 へ配置
arm_and_hand_r = arm_r_cyl.fuse(hand_r)

# --- 杖・ランタン（5度傾き、新しい手の位置 Y=-17.0 に合わせて自動同期） ---
staff_angle_deg = 5.0
staff_rad = math.radians(staff_angle_deg)

target_hand_z = -2.0
pivot_z = -8.29
delta_z = target_hand_z - pivot_z
# 新しい右手位置（-17.0）を正確に貫通するようベースY座標を再計算
base_y = -17.0 + (delta_z * math.sin(staff_rad))

unified_staff_cone = Part.makeCone(1.8, 1.4, 17.0)
unified_staff_cone.rotate(App.Base.Vector(0,0,0), App.Base.Vector(1,0,0), staff_angle_deg)
unified_staff_cone.translate(App.Base.Vector(-2.0, base_y, pivot_z))

lantern = Part.makeSphere(lantern_r)
lantern.translate(App.Base.Vector(-2.0, base_y - (staff_h * math.sin(staff_rad)), staff_h * math.cos(staff_rad) + pivot_z))

magic_staff = unified_staff_cone.fuse(lantern)

untrimmed_king = body_cape_collar.fuse(arm_and_hand_l).fuse(arm_and_hand_r).fuse(magic_staff)

# カボチャの底面(Z = -9.2)の位置で水平カット
floor_cutter = Part.makeBox(100.0, 100.0, 20.0)
floor_cutter.translate(App.Base.Vector(-50.0, -50.0, -20.0 - 9.2))
full_lp_king = untrimmed_king.cut(floor_cutter)

# 地面への接地移動
full_lp_king.translate(App.Base.Vector(0.0, 0.0, 9.2))

obj_full = doc.addObject("Part::Feature", "LP_King")
obj_full.Shape = full_lp_king

doc.recompute()

if App.GuiUp:
    try:
        App.Gui.ActiveDocument.ActiveView.viewReady()
        App.Gui.ActiveDocument.ActiveView.fitAll()
    except Exception as e:
        pass

print("出力しました！")

