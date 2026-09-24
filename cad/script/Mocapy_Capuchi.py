import FreeCAD as App
import Part
import math

def create_perfect_capuchi_ideal_face_returned():
    # 1. 新規ドキュメントの作成
    doc = App.newDocument("Mocapy_Capuchi")
    
    # 10倍スケール用のマトリクス
    matrix_scale10 = App.Matrix()
    matrix_scale10.scale(10.0)
    
    # ==========================================
    # 🌟 各パーツの作成と個別の10倍スケール処理
    # ==========================================
    
    # 卵形のボディ
    body_sphere = Part.makeSphere(1.0)
    matrix_body = App.Matrix()
    matrix_body.scale(App.Vector(1.2, 1.2, 1.5))
    capuchi_body = body_sphere.transformGeometry(matrix_body).translate(App.Vector(0, 0, 2.3)).transformGeometry(matrix_scale10)
    
    # 左足
    leg_L = Part.makeCylinder(0.33, 1.2, App.Vector(0.0, 0.45, 0.3), App.Vector(0.0, 0.0, 1.0))
    foot_L = Part.makeSphere(0.33).translate(App.Vector(0.0, 0.45, 0.3))
    full_leg_L = leg_L.fuse(foot_L).transformGeometry(matrix_scale10)
    
    # 右足
    leg_R = Part.makeCylinder(0.33, 1.2, App.Vector(0.0, -0.45, 0.3), App.Vector(0.0, 0.0, 1.0))
    foot_R = Part.makeSphere(0.33).translate(App.Vector(0.0, -0.45, 0.3))
    full_leg_R = leg_R.fuse(foot_R).transformGeometry(matrix_scale10)
    
    # 丸い顔
    round_face = Part.makeSphere(1.1).translate(App.Vector(0.3, 0, 2.53)).transformGeometry(matrix_scale10)
    
    # 左腕と左肩
    shoulder_L = Part.makeSphere(0.35).translate(App.Vector(0.0, 1.2, 1.8))
    arm_L = Part.makeCylinder(0.18, 1.1, App.Vector(0.0, 1.2, 1.8), App.Vector(0.0, 0.0, -1.0))
    hand_L = Part.makeSphere(0.18).translate(App.Vector(0.0, 1.2, 0.7))
    full_arm_L = shoulder_L.fuse(arm_L).fuse(hand_L).transformGeometry(matrix_scale10)
    
    # 右腕と右肩
    shoulder_R = Part.makeSphere(0.35).translate(App.Vector(0.0, -1.2, 1.8))
    arm_R = Part.makeCylinder(0.18, 1.1, App.Vector(0.0, -1.2, 1.8), App.Vector(0.0, 0.0, -1.0))
    hand_R = Part.makeSphere(0.18).translate(App.Vector(0.0, -1.2, 0.7))
    full_arm_R = shoulder_R.fuse(arm_R).fuse(hand_R).transformGeometry(matrix_scale10)
    
    # 顔のパーツ（点目 ＆ ラウンドへの字口）
    eye_L = Part.makeSphere(0.13).translate(App.Vector(1.3, 0.35, 2.73)).transformGeometry(matrix_scale10)
    eye_R = Part.makeSphere(0.13).translate(App.Vector(1.3, -0.35, 2.73)).transformGeometry(matrix_scale10)
    
    mouth_torus = Part.makeTorus(0.22, 0.05, App.Vector(1.33, 0.0, 2.38), App.Vector(1.0, 0.0, 0.0))
    mouth_cutter = Part.makeBox(2.0, 2.0, 2.0, App.Vector(0.0, -1.0, 2.38))
    round_mouth = mouth_torus.cut(mouth_cutter).transformGeometry(matrix_scale10)
    
    # ==========================================
    # 🌟 順序を守って安全に結合・カット
    # ==========================================
    # 1. まずベースとなる体と頭、手足をすべて合体させる
    capuchi_raw = capuchi_body.fuse(full_leg_L).fuse(full_leg_R).fuse(round_face).fuse(full_arm_L).fuse(full_arm_R).removeSplitter()
    
    # 2. 合体し終わった頑丈な体に、顔の彫り込みを入れる
    capuchi_raw = capuchi_raw.cut(eye_L).cut(eye_R).cut(round_mouth).removeSplitter()
    
    # ==========================================
    # 5. 3Dプリント安定用の底面フラットカット
    # ==========================================
    flat_cutter = Part.makeBox(300.0, 300.0, 50.0, App.Vector(-150.0, -150.0, -50.0 + 0.2))
    final_capuchi = capuchi_raw.cut(flat_cutter).removeSplitter()
    
    capuchi_object = doc.addObject("Part::Feature", "Capuchi")
    capuchi_object.Shape = final_capuchi
    
    # 6. 画面の再計算と見栄えの調整
    doc.recompute()
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.ActiveDocument.ActiveView.viewAxometric()
        Gui.ActiveDocument.ActiveView.fitAll()
        
        gui_obj = Gui.getDocument(doc.Name).getObject(capuchi_object.Name)
        gui_obj.ShapeColor = (0.55, 0.4, 0.3)
        gui_obj.DisplayMode = "Shaded"

# スクリプトの実行
create_perfect_capuchi_ideal_face_returned()
