import FreeCAD as App
import Part
import math

def create_dangoloron_attack_form():
    # 1. 新規ドキュメントの作成
    doc = App.newDocument("Mocapy_Dangoloron_Attack")
    
    # 2. アタックフォルムのベース（限界まで丸まった完璧な正円の球体、半径3.5mm）
    attack_sphere = Part.makeSphere(3.5)
    
    # 🌟 【絶対定着】完全な球体でも転がらないよう、底面（Z=-3.0以下）をわずかにカット
    # これによりベッドへしっかり密着する接地面積が生まれます
    flat_cutter = Part.makeBox(20.0, 20.0, 5.0, App.Vector(-10.0, -10.0, -5.0 - 3.0))
    attack_sphere = attack_sphere.cut(flat_cutter)
    
    # 3. 超高速回転を表現する「10本のらせん状のうねり溝」
    # 3Dプリンターで印刷したときに、本当にギュルギュル回っているように見える視覚効果を作ります
    num_cuts = 10
    for i in range(num_cuts):
        # 360度を10等分した角度
        angle = (360.0 / num_cuts) * i
        rad = math.radians(angle)
        
        # 回転軸の方向ベクトル（少し斜めにねじることでらせん状のうねりを表現）
        direction = App.Vector(math.sin(rad), math.cos(rad), 0.2).normalize()
        
        # 高速回転の風を切るような薄いカッター（厚さ0.2mm）
        cutter_box = Part.makeBox(0.2, 10.0, 10.0, App.Vector(-0.1, -5.0, -5.0))
        
        # カッターを斜めに回転させて、球体の表面にうねりを刻む
        matrix_rot = App.Matrix()
        # Z軸まわりに回転
        matrix_rot.rotateZ(rad)
        # さらに少しだけ傾ける
        matrix_rot.rotateX(math.radians(15))
        
        rotated_cutter = cutter_box.transformGeometry(matrix_rot)
        
        # 溝が深くなりすぎないように、少し外側にオフセットして球体の表面だけを薄く削る
        # 軸方向に少し引っ張る
        offset_vector = direction * 3.3
        rotated_cutter.translate(offset_vector)
        
        # お腹の定着面が削れすぎないように安全ガード
        rotated_cutter = rotated_cutter.cut(flat_cutter)
        
        # 球体から溝を引く
        attack_sphere = attack_sphere.cut(rotated_cutter)
        
    dangoloron_attack = attack_sphere.removeSplitter()
    
    # 4. 最終形状の確定と画面表示
    dangoloron_object = doc.addObject("Part::Feature", "Dangoloron_Attack_Form")
    dangoloron_object.Shape = dangoloron_attack
    
    # 5. 画面の再計算と見栄えの調整
    doc.recompute()
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.ActiveDocument.ActiveView.viewAxometric()
        Gui.ActiveDocument.ActiveView.fitAll()
        
        gui_obj = Gui.getDocument(doc.Name).getObject(dangoloron_object.Name)
        # 必殺技発動中のエネルギーをイメージした、ちょっと強そうなダークグレーやメタリックカラー
        gui_obj.ShapeColor = (0.25, 0.28, 0.35)
        gui_obj.DisplayMode = "Shaded"

# スクリプトの実行
create_dangoloron_attack_form()
