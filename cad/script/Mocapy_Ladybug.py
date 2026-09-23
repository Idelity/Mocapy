import FreeCAD as App
import Part
import math

def create_perfect_chibi_ladybug():
    # 1. 新規ドキュメントの作成
    doc = App.newDocument("Mocapy_Ladybug")
    
    # 2. てんとう虫の胴体（上から見て完璧な正円ベース）
    body_sphere = Part.makeSphere(3.5)
    matrix_body = App.Matrix()
    matrix_body.scale(App.Vector(0.82, 0.82, 0.58))
    ladybug_body = body_sphere.transformGeometry(matrix_body)
    
    # 🌟 お腹のカット位置
    flat_cutter = Part.makeBox(20.0, 20.0, 5.0, App.Vector(-10.0, -10.0, -5.0 - 0.7))
    ladybug_body = ladybug_body.cut(flat_cutter)
    
    # 羽の合わせ目の溝（0.3mm幅）
    wing_line = Part.makeBox(12.0, 0.3, 5.0, App.Vector(-6.0, -0.15, 0.0))
    wing_line.translate(App.Vector(0, 0, 0.2))
    ladybug_winged_body = ladybug_body.cut(wing_line)
    
    # 3. 頭部の作成（半径2.2mmの綺麗な球体）
    head_sphere = Part.makeSphere(2.2)
    ladybug_head = head_sphere.translate(App.Vector(1.4, 0, 0.5))
    ladybug_head = ladybug_head.cut(flat_cutter)
    
    # 4. 胴体と頭部を合体
    raw_combined = ladybug_winged_body.fuse(ladybug_head)
    ladybug_raw = raw_combined.removeSplitter()
    
    # ==========================================
    # 🌟 頭のラウンドに沿った「薄く・小さい目玉」
    # ==========================================
    eye_base_left = Part.makeSphere(2.35).translate(App.Vector(1.4, 0, 0.5))
    eye_base_right = Part.makeSphere(2.35).translate(App.Vector(1.4, 0, 0.5))
    left_cutter = Part.makeSphere(0.9).translate(App.Vector(3.0, 1.0, 1.3))
    right_cutter = Part.makeSphere(0.9).translate(App.Vector(3.0, -1.0, 1.3))
    eye_left = eye_base_left.common(left_cutter)
    eye_right = eye_base_right.common(right_cutter)
    ladybug_raw = ladybug_raw.fuse(eye_left).fuse(eye_right)
    
    # ==========================================
    # 🌟 後ろ（背中側）に向かって流れる「触角」
    # ==========================================
    antenna_base_L = Part.makeCylinder(0.4, 1.8, App.Vector(2.1, 0.6, 1.7), App.Vector(-0.5, 0.5, 0.6))
    tip_sphere_L = Part.makeSphere(0.55).translate(App.Vector(2.1, 0.6, 1.7) + App.Vector(-0.5, 0.5, 0.6).normalize() * 1.8)
    antenna_left = antenna_base_L.fuse(tip_sphere_L).removeSplitter()
    
    antenna_base_R = Part.makeCylinder(0.4, 1.8, App.Vector(2.1, -0.5, 1.7), App.Vector(-0.5, -0.5, 0.6))
    tip_sphere_R = Part.makeSphere(0.55).translate(App.Vector(2.1, -0.5, 1.7) + App.Vector(-0.5, -0.5, 0.6).normalize() * 1.8)
    antenna_right = antenna_base_R.fuse(tip_sphere_R).removeSplitter()
    
    ladybug_raw = ladybug_raw.fuse(antenna_left).fuse(antenna_right)
    
    # ==========================================
    # 🌟 【足の肉厚化】ガッチリ一体化する「極太の足」（計6本）
    # 足の半径を 0.45mm -> 0.65mm（直径1.3mm）へ大幅に太くしました。
    # 胴体に深く食い込むように生え際の位置（pos）をわずかに内側に調整しています。
    # 接地面のカットを最後に適用するため、設置のフラットさは完全に維持されます。
    # ==========================================
    leg_positions = [
        {"pos": App.Vector(1.2, 1.6, 0.0), "dir": App.Vector(0.5, 1.0, -0.33)},
        {"pos": App.Vector(1.2, -1.6, 0.0), "dir": App.Vector(0.5, -1.0, -0.33)},
        {"pos": App.Vector(0.0, 1.9, 0.0), "dir": App.Vector(0.0, 1.0, -0.33)},
        {"pos": App.Vector(0.0, -1.9, 0.0), "dir": App.Vector(0.0, -1.0, -0.33)},
        {"pos": App.Vector(-1.2, 1.7, 0.0), "dir": App.Vector(-0.5, 1.0, -0.33)},
        {"pos": App.Vector(-1.2, -1.7, 0.0), "dir": App.Vector(-0.5, -1.0, -0.33)}
    ]
    
    for leg in leg_positions:
        # 半径を0.65mmにして、どっしりとした太さに変更
        leg_shaft = Part.makeCylinder(0.65, 1.2, leg["pos"], leg["dir"])
        
        u_dir = leg["dir"].normalize()
        tip_pos = leg["pos"] + u_dir * 1.2
        leg_tip_sphere = Part.makeSphere(0.65).translate(tip_pos)
        
        full_leg = leg_shaft.fuse(leg_tip_sphere).removeSplitter()
        # 底面の平らさをキープするためのカット
        full_leg = full_leg.cut(flat_cutter)
        
        # 本体へ合体
        ladybug_raw = ladybug_raw.fuse(full_leg)
        
    # 5. 最終形状の確定と画面表示
    final_ladybug = ladybug_raw
    ladybug_object = doc.addObject("Part::Feature", "Ladybug")
    ladybug_object.Shape = final_ladybug
    
    # 6. 画面の再計算と見栄えの調整
    doc.recompute()
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.ActiveDocument.ActiveView.viewAxometric()
        Gui.ActiveDocument.ActiveView.fitAll()
        
        gui_obj = Gui.getDocument(doc.Name).getObject(ladybug_object.Name)
        gui_obj.ShapeColor = (0.85, 0.15, 0.15)
        gui_obj.DisplayMode = "Shaded"

# スクリプトの実行
create_perfect_chibi_ladybug()
