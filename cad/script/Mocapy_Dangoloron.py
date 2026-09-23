import FreeCAD as App
import Part
import math

def create_chibi_dangoloron_long_antennas():
    # 1. 新規ドキュメントの作成
    doc = App.newDocument("Mocapy_Dangoloron")
    
    # 2. ダンゴロロンのベース（丸まった体を表現する楕円球）
    base_sphere = Part.makeSphere(3.5)
    matrix_base = App.Matrix()
    matrix_base.scale(App.Vector(1.3, 0.9, 0.7)) # 横長で少し平べったいダンゴムシ体型
    dangoloron_body = base_sphere.transformGeometry(matrix_base)
    
    # 🌟 【絶対定着】お腹を Z=-0.5 で真っ平らにカットしてサポートレス化
    flat_cutter = Part.makeBox(20.0, 20.0, 5.0, App.Vector(-10.0, -10.0, -5.0 - 0.5))
    dangoloron_body = dangoloron_body.cut(flat_cutter)
    
    # 3. 背中の「節（セグメント）」を刻む溝
    for i in range(-2, 3):
        if i == 0: continue
        segment_line = Part.makeBox(0.25, 10.0, 5.0, App.Vector(i * 1.0, -5.0, 0.0))
        segment_line.translate(App.Vector(0, 0, 0.3))
        dangoloron_body = dangoloron_body.cut(segment_line)
        
    # ==========================================
    # 🌟 特大の丸い楕円スライス目（左右に離した位置）
    # ==========================================
    eye_sphere_L = Part.makeSphere(1.15).translate(App.Vector(3.9, 1.6, 0.1))
    eye_sphere_R = Part.makeSphere(1.15).translate(App.Vector(3.9, -1.6, 0.1))
    
    # 一回り大きい楕円スライサー
    cutter_sphere = Part.makeSphere(3.5)
    matrix_cutter = App.Matrix()
    matrix_cutter.scale(App.Vector(1.42, 1.02, 0.82))
    oval_cutter = cutter_sphere.transformGeometry(matrix_cutter)
    
    # 楕円のカーブでスライスし、お腹的フラットカットを適用
    flat_eye_L = eye_sphere_L.common(oval_cutter).cut(flat_cutter)
    flat_eye_R = eye_sphere_R.common(oval_cutter).cut(flat_cutter)
    
    dangoloron_raw = dangoloron_body.fuse(flat_eye_L).fuse(flat_eye_R).removeSplitter()
    
    # ==========================================
    # 🌟 【修正】さらに伸ばした「完全接地のロング触角」
    # 長さを 1.4 -> 『2.2』 へ大幅アップ！
    # 前方へツンと長く伸ばし、底面をお腹カッターでフラットにすることで
    # 1層目からガッチリベッドに張り付く構造を維持しています。
    # ==========================================
    # 触角の太さは0.35mm、先端の球体は0.45mm
    antenna_L = Part.makeCylinder(0.35, 2.2, App.Vector(3.2, 0.5, -0.2), App.Vector(1.0, 0.1, 0.0))
    tip_L = Part.makeSphere(0.45).translate(App.Vector(3.2, 0.5, -0.2) + App.Vector(1.0, 0.1, 0.0).normalize() * 2.2)
    full_antenna_L = antenna_L.fuse(tip_L).removeSplitter()
    
    antenna_R = Part.makeCylinder(0.35, 2.2, App.Vector(3.2, -0.5, -0.2), App.Vector(1.0, -0.1, 0.0))
    tip_R = Part.makeSphere(0.45).translate(App.Vector(3.2, -0.5, -0.2) + App.Vector(1.0, -0.1, 0.0).normalize() * 2.2)
    full_antenna_R = antenna_R.fuse(tip_R).removeSplitter()
    
    # 触角の底面をしっかりカット
    full_antenna_L = full_antenna_L.cut(flat_cutter)
    full_antenna_R = full_antenna_R.cut(flat_cutter)
    
    # 本体へドッキング
    dangoloron_raw = dangoloron_raw.fuse(full_antenna_L).fuse(full_antenna_R)
    
    # 5. 最終形状の確定と画面表示
    final_dangoloron = dangoloron_raw
    dangoloron_object = doc.addObject("Part::Feature", "Dangoloron")
    dangoloron_object.Shape = final_dangoloron
    
    # 6. 画面の再計算と見栄えの調整
    doc.recompute()
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.ActiveDocument.ActiveView.viewAxometric()
        Gui.ActiveDocument.ActiveView.fitAll()
        
        gui_obj = Gui.getDocument(doc.Name).getObject(dangoloron_object.Name)
        gui_obj.ShapeColor = (0.4, 0.45, 0.5)
        gui_obj.DisplayMode = "Shaded"

# スクリプトの実行
create_chibi_dangoloron_long_antennas()
