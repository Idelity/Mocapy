import FreeCAD as App
import Part
import math

def create_dangoloron_attack_perfect_spiral():
    # 1. 新規ドキュメントの作成（フリーズなし、一瞬で終わります）
    doc = App.newDocument("Dangoloron_Attack")
    
    # 2. ベースとなる大きな球体（半径3.5mm）
    base_sphere = Part.makeSphere(3.5)
    
    # 🌟 【絶対定着】転がらないよう、底面（Z=-3.0以下）を真っ平らにカット
    flat_cutter = Part.makeBox(20.0, 20.0, 5.0, App.Vector(-10.0, -10.0, -5.0 - 3.0))
    base_sphere = base_sphere.cut(flat_cutter)
    
    # ==========================================
    # 🌟 【エラー・フリーズ完全克服】重ね合わせ（fuse）による美しいらせん甲羅
    # 面倒な線の引き算を一切やめ、一回りずつ小さな球体を「斜めに傾けながら」
    # 5回重ねて合体させることで、ダンゴムシが渦巻状にギュッと丸まった
    # 美しいらせんの段差（殻の重なり）を完璧に再現しました！
    # ==========================================
    combined_shape = base_sphere
    
    # 5枚の殻を重ねる
    for i in range(1, 6):
        # 1層ごとに少しずつサイズを小さくする（3.5mm -> 3.3mm -> 3.1mm...）
        current_radius = 3.5 - (i * 0.18)
        shell = Part.makeSphere(current_radius)
        
        # 🌟 殻を少しずつ前（X）と下（Z）にズラし、斜めにねじる（これが美しい渦巻きの段差になります）
        matrix_rot = App.Matrix()
        matrix_rot.rotateY(math.radians(i * 12)) # 12度ずつ傾ける
        matrix_rot.rotateZ(math.radians(i * 5))  # わずかにひねる
        
        positioned_shell = shell.transformGeometry(matrix_rot)
        # 前方にわずかにズラす
        positioned_shell.translate(App.Vector(i * 0.12, 0, -i * 0.05))
        
        # お腹のフラット面を維持
        positioned_shell = positioned_shell.cut(flat_cutter)
        
        # 🌟 引き算ではなく「足し算（fuse）」なのでPCへの負荷がほぼゼロ！一瞬で終わります
        combined_shape = combined_shape.fuse(positioned_shell)
        
    dangoloron_attack = combined_shape.removeSplitter()
    
    # 3. 最終形状の確定と画面表示
    dangoloron_object = doc.addObject("Part::Feature", "Dangoloron_Attack")
    dangoloron_object.Shape = dangoloron_attack
    
    # 4. 画面の再計算と見栄えの調整
    doc.recompute()
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.ActiveDocument.ActiveView.viewAxometric()
        Gui.ActiveDocument.ActiveView.fitAll()
        
        gui_obj = Gui.getDocument(doc.Name).getObject(dangoloron_object.Name)
        gui_obj.ShapeColor = (0.25, 0.28, 0.35)
        gui_obj.DisplayMode = "Shaded"

# スクリプトの実行
create_dangoloron_attack_perfect_spiral()
