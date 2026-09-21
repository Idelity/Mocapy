import FreeCAD as App
import Part
import math

def create_perfect_chibi_ladybug():
    # 1. 新規ドキュメントの作成
    doc = App.newDocument("Mocapy_Ladybug")
    
    # 2. てんとう虫の胴体（上から見て完璧な正円ベース）
    body_sphere = Part.makeSphere(3.5)
    matrix_body = App.Matrix()
    matrix_body.scale(App.Vector(0.82, 0.82, 0.55))
    ladybug_body = body_sphere.transformGeometry(matrix_body)
    
    # 羽の合わせ目の溝（0.3mm幅）は胴体だけに刻む
    wing_line = Part.makeBox(12.0, 0.3, 5.0, App.Vector(-6.0, -0.15, 0.0))
    wing_line.translate(App.Vector(0, 0, 0.2))
    ladybug_winged_body = ladybug_body.cut(wing_line)
    
    # 3. 頭部の作成（半径2.2mmの綺麗な球体）
    head_sphere = Part.makeSphere(2.2)
    ladybug_head = head_sphere.translate(App.Vector(1.4, 0, 0.6))
    
    # 4. 胴体と頭部を合体
    raw_combined = ladybug_winged_body.fuse(ladybug_head)
    ladybug_raw = raw_combined.removeSplitter()
    
    # ==========================================
    # 🌟 頭のラウンドに沿った「薄く・小さい目玉」
    # ==========================================
    eye_base_left = Part.makeSphere(2.35).translate(App.Vector(1.4, 0, 0.6))
    eye_base_right = Part.makeSphere(2.35).translate(App.Vector(1.4, 0, 0.6))
    left_cutter = Part.makeSphere(0.9).translate(App.Vector(3.0, 1.0, 1.4))
    right_cutter = Part.makeSphere(0.9).translate(App.Vector(3.0, -1.0, 1.4))
    eye_left = eye_base_left.common(left_cutter)
    eye_right = eye_base_right.common(right_cutter)
    ladybug_raw = ladybug_raw.fuse(eye_left).fuse(eye_right)
    
    # ==========================================
    # 🌟 先端に向けて太く丸くなる「流線型のへの字触角」
    # ==========================================
    # --- 左側の触角 ---
    antenna_base_L = Part.makeCylinder(0.2, 2.2, App.Vector(2.5, 0.6, 1.8), App.Vector(-0.7, 0.5, 0.5))
    tip_sphere_L = Part.makeSphere(0.3).translate(App.Vector(1.3, 2.2, 2.7))
    base_end_circle_L = Part.makeCircle(0.2, App.Vector(0.96, 1.7, 2.9), App.Vector(-0.7, 0.5, 0.5))
    base_end_face_L = Part.makeFace(Part.Wire(base_end_circle_L))
    tip_mid_circle_L = Part.makeCircle(0.3, App.Vector(1.3, 2.2, 2.7), App.Vector(0.5, 0.8, -0.2))
    tip_mid_face_L = Part.makeFace(Part.Wire(tip_mid_circle_L))
    loft_connector_L = Part.makeLoft([base_end_face_L, tip_mid_face_L], True)
    antenna_left = antenna_base_L.fuse(loft_connector_L).fuse(tip_sphere_L).removeSplitter()
    
    # --- 右側の触角 ---
    antenna_base_R = Part.makeCylinder(0.2, 2.2, App.Vector(2.5, -0.6, 1.8), App.Vector(-0.7, -0.5, 0.5))
    tip_sphere_R = Part.makeSphere(0.3).translate(App.Vector(1.3, -2.2, 2.7))
    base_end_circle_R = Part.makeCircle(0.2, App.Vector(0.96, -1.7, 2.9), App.Vector(-0.7, -0.5, 0.5))
    base_end_face_R = Part.makeFace(Part.Wire(base_end_circle_R))
    tip_mid_circle_R = Part.makeCircle(0.3, App.Vector(1.3, -2.2, 2.7), App.Vector(0.5, -0.8, -0.2))
    tip_mid_face_R = Part.makeFace(Part.Wire(tip_mid_circle_R))
    loft_connector_R = Part.makeLoft([base_end_face_R, tip_mid_face_R], True)
    antenna_right = antenna_base_R.fuse(loft_connector_R).fuse(tip_sphere_R).removeSplitter()
    
    ladybug_raw = ladybug_raw.fuse(antenna_left).fuse(antenna_right)
    
    # ==========================================
    # 🌟 【完全修正】足先を触角と同じように「丸球」で閉じ、滑らかに一体化（計6本）
    # 円柱の末端に球体をドッキングして一体化させ、角張ったカドを完全に無くしました
    # ==========================================
    leg_positions = [
        {"pos": App.Vector(1.5, 2.0, 0.1), "dir": App.Vector(0.5, 1.0, -0.3)},
        {"pos": App.Vector(1.5, -2.0, 0.1), "dir": App.Vector(0.5, -1.0, -0.3)},
        {"pos": App.Vector(0.0, 2.3, 0.1), "dir": App.Vector(0.0, 1.0, -0.3)},
        {"pos": App.Vector(0.0, -2.3, 0.1), "dir": App.Vector(0.0, -1.0, -0.3)},
        {"pos": App.Vector(-1.5, 2.1, 0.1), "dir": App.Vector(-0.5, 1.0, -0.3)},
        {"pos": App.Vector(-1.5, -2.1, 0.1), "dir": App.Vector(-0.5, -1.0, -0.3)}
    ]
    
    for leg in leg_positions:
        # 1. 足の軸（円柱）を作成（長さ1.5mm）
        leg_shaft = Part.makeCylinder(0.2, 1.5, leg["pos"], leg["dir"])
        
        # 2. 足の先端の座標を計算（位置 ＋ 方向ベクトル×長さ）
        # 円柱の向き（dir）を単位ベクトル化して長さを掛け算
        d_len = math.sqrt(leg["dir"].x**2 + leg["dir"].y**2 + leg["dir"].z**2)
        u_dir = App.Vector(leg["dir"].x/d_len, leg["dir"].y/d_len, leg["dir"].z/d_len)
        tip_pos = leg["pos"] + u_dir * 1.5
        
        # 3. 足先に「半径0.2mmの丸い球体」を配置してドッキング
        leg_tip_sphere = Part.makeSphere(0.2).translate(tip_pos)
        full_leg = leg_shaft.fuse(leg_tip_sphere).removeSplitter()
        
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
        Gui.getDocument(doc.Name).getObject(ladybug_object.Name).ShapeColor = (0.85, 0.15, 0.15)
        Gui.getDocument(doc.Name).getObject(ladybug_object.Name).DisplayMode = "Shaded"

# スクリプトの実行
create_perfect_chibi_ladybug()
