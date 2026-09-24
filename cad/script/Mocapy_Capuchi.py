import FreeCAD as App
import Part
import math
import os

def create_perfect_capuchi_ideal_face_returned():
    # 新しいタブを作らず、今開いている画面を上書きリセットする
    doc = App.activeDocument()
    if not doc:
        doc = App.newDocument("Mocapy_Capuchi")
    else:
        # 画面に古いカプチが残っていたら一旦すべて削除して綺麗にする
        for obj in doc.Objects:
            doc.removeObject(obj.Name)
    
    # 10倍スケール用のマトリクス
    matrix_scale10 = App.Matrix()
    matrix_scale10.scale(10.0)
    
    # ==========================================
    # 1. 卵形のボディ ＆ お面の段差溝
    # ==========================================
    body_sphere = Part.makeSphere(1.0)
    matrix_body = App.Matrix()
    matrix_body.scale(App.Vector(1.2, 1.2, 1.5))
    capuchi_body = body_sphere.transformGeometry(matrix_body).translate(App.Vector(0, 0, 2.3)).transformGeometry(matrix_scale10)
    
    # 安全な角丸の足を作るロジック（円柱とボックスの合体）
    def make_rounded_foot(center_y):
        r = 0.35
        h = 0.3
        cyl_front = Part.makeCylinder(r, h, App.Vector(0.2, center_y, 0.0), App.Vector(0.0, 0.0, 1.0))
        cyl_back  = Part.makeCylinder(r, h, App.Vector(-0.2, center_y, 0.0), App.Vector(0.0, 0.0, 1.0))
        box_mid   = Part.makeBox(0.4, r * 2.0, h, App.Vector(-0.2, center_y - r, 0.0))
        return cyl_front.fuse(cyl_back).fuse(box_mid).removeSplitter()

    # 左足
    leg_L = Part.makeCylinder(0.33, 1.2, App.Vector(0.0, 0.45, 0.3), App.Vector(0.0, 0.0, 1.0))
    foot_L = Part.makeSphere(0.33).translate(App.Vector(0.0, 0.45, 0.3))
    box_foot_L = make_rounded_foot(0.45)
    full_leg_L = leg_L.fuse(foot_L).fuse(box_foot_L).transformGeometry(matrix_scale10)
    
    # 右足
    leg_R = Part.makeCylinder(0.33, 1.2, App.Vector(0.0, -0.45, 0.3), App.Vector(0.0, 0.0, 1.0))
    foot_R = Part.makeSphere(0.33).translate(App.Vector(0.0, -0.45, 0.3))
    box_foot_R = make_rounded_foot(-0.45)
    full_leg_R = leg_R.fuse(foot_R).fuse(box_foot_R).transformGeometry(matrix_scale10)
    
    # 丸い顔
    round_face = Part.makeSphere(1.1).translate(App.Vector(0.3, 0, 2.53)).transformGeometry(matrix_scale10)
    
    # 顔の境界を作るための円柱カッター
    face_cutter_cyl = Part.makeCylinder(1.15, 2.0, App.Vector(0.35, 0.0, 2.53), App.Vector(1.0, 0.0, 0.0))
    groove_cutter = face_cutter_cyl.transformGeometry(matrix_scale10)

    # Pure U-hand (🌟元の大きくて綺麗な横向きU字おててに戻しました)
    def make_pure_u_hand():
        r_outer = 0.38
        r_inner = 0.18
        thick = 0.45
        
        cyl_outer = Part.makeCylinder(r_outer, thick, App.Vector(0,0,0), App.Vector(0,0,1))
        cyl_inner = Part.makeCylinder(r_inner, thick, App.Vector(0,0,0), App.Vector(0,0,1))
        ring = cyl_outer.cut(cyl_inner)
        
        box_cutter = Part.makeBox(1.0, 1.0, 1.0, App.Vector(-0.5, -1.0, -0.1))
        u_shape = ring.cut(box_cutter)
        
        mat_base = App.Matrix()
        mat_base.rotateY(math.radians(-90))
        u_positioned = u_shape.transformGeometry(mat_base)
        
        # 横に90度回転
        mat_invert = App.Matrix()
        mat_invert.rotateX(math.radians(90))
        
        # 決定したベストな前位置（0.22）
        mat_invert.move(App.Vector(0.22, 0.0, 0.0))
        
        return u_positioned.transformGeometry(mat_invert)

    y_left_arm  = 1.2
    y_right_arm = -1.2

    # 左の肩・長さ1.00の腕・高さ0.55の横向きU字手
    shoulder_L = Part.makeSphere(0.35).translate(App.Vector(0.0, y_left_arm, 1.8))
    arm_L = Part.makeCylinder(0.18, 1.00, App.Vector(0.0, y_left_arm, 1.8), App.Vector(0.0, 0.0, -1.0))
    u_hand_L = make_pure_u_hand().translate(App.Vector(0.0, y_left_arm, 0.55))
    full_arm_L = shoulder_L.fuse(arm_L).fuse(u_hand_L.transformGeometry(mat_hand_L if 'mat_hand_L' in locals() else App.Matrix())).transformGeometry(matrix_scale10)
    
    # 右の肩・長さ1.00の腕・高さ0.55の横向きU字手
    shoulder_R = Part.makeSphere(0.35).translate(App.Vector(0.0, y_right_arm, 1.8))
    arm_R = Part.makeCylinder(0.18, 1.00, App.Vector(0.0, y_right_arm, 1.8), App.Vector(0.0, 0.0, -1.0))
    u_hand_R = make_pure_u_hand().translate(App.Vector(0.0, y_right_arm, 0.55))
    full_arm_R = shoulder_R.fuse(arm_R).fuse(u_hand_R.transformGeometry(mat_hand_R if 'mat_hand_R' in locals() else App.Matrix())).transformGeometry(matrix_scale10)
    
    # 🌟【キープ】ぷっくり点目（元の1.2倍：0.13 → 0.156 に拡大した大きめの目）
    eye_radius = 0.13 * 1.2
    eye_L = Part.makeSphere(eye_radius).translate(App.Vector(1.17, 0.35, 2.73)).transformGeometry(matrix_scale10)
    eye_R = Part.makeSphere(eye_radius).translate(App.Vector(1.17, -0.35, 2.73)).transformGeometry(matrix_scale10)
    
    # ラウンドへの字口
    mouth_torus = Part.makeTorus(0.22, 0.05, App.Vector(1.33, 0.0, 2.38), App.Vector(1.0, 0.0, 0.0))
    mouth_cutter = Part.makeBox(2.0, 2.0, 2.0, App.Vector(0.0, -1.0, 2.38))
    round_mouth = mouth_torus.cut(mouth_cutter).transformGeometry(matrix_scale10)
    
    # ==========================================
    # 結合とカット
    # ==========================================
    body_and_limbs = capuchi_body.fuse(full_leg_L).fuse(full_leg_R).fuse(full_arm_L).fuse(full_arm_R).removeSplitter()
    body_grooved = body_and_limbs.cut(groove_cutter).removeSplitter()
    capuchi_raw = body_grooved.fuse(round_face).fuse(eye_L).fuse(eye_R).removeSplitter()
    capuchi_raw = capuchi_raw.cut(round_mouth).removeSplitter()
    
    # ==========================================
    # 5. 3Dプリント安定用の底面フラットカット
    # ==========================================
    flat_cutter = Part.makeBox(300.0, 300.0, 50.0, App.Vector(-150.0, -150.0, -50.0 + 0.2))
    final_capuchi = capuchi_raw.cut(flat_cutter).removeSplitter()
    
    capuchi_object = doc.addObject("Part::Feature", "Capuchi")
    capuchi_object.Shape = final_capuchi
    
    # ==========================================
    # デスクトップへのSTL自動エクスポート機能
    # ==========================================
    try:
        desktop_path = os.path.expanduser("~/Desktop")
        file_path = os.path.join(desktop_path, "Capuchi_10x.stl")
        Part.export([capuchi_object], file_path)
        print(f"🌟 デスクトップにSTLファイルを保存しました: {file_path}")
    except Exception as e:
        print(f"⚠️ STL保存中にエラーが発生しました: {str(e)}")

    # 6. 画面の再計算と見栄えの調整
    doc.recompute()
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.ActiveDocument.ActiveView.viewAxometric()
        Gui.ActiveDocument.ActiveView.fitAll()
        
        gui_obj = Gui.getDocument(doc.Name).getObject(capuchi_object.Name)
        gui_obj.ShapeColor = (0.55, 0.4, 0.3)
        gui_obj.DisplayMode = "Shaded"
        gui_obj.Deviation = 0.005

# スクリプトの実行
create_perfect_capuchi_ideal_face_returned()
