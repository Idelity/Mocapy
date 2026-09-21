import FreeCAD as App
import Part

def create_optimal_split_coffee_bean():
    # 1. 新規ドキュメントの作成
    doc = App.newDocument("Mocapy_Bean")
    
    # 2. 豆の本体（ぷっくりとしたソリッド立体）
    base_sphere = Part.makeSphere(5.0)
    matrix = App.Matrix()
    matrix.scale(App.Vector(1.2, 0.84, 0.5)) # 長さ12mm・幅8.4mm・厚み5mm
    bean_body = base_sphere.transformGeometry(matrix)
    
    # 豆の裏面を少し平らにカット
    clipper = Part.makeBox(20, 20, 10, App.Vector(-10, -10, -11.5))
    bean_body = bean_body.cut(clipper)
    
    # 3. ★完全修正：溝の太さを「0.9mm」にジャスト調整したV字カッター
    # 太すぎず細すぎない、一番リアルに見える幅に刃の厚みを設定します
    v_cutter = Part.makeBox(20.0, 0.9, 20.0, App.Vector(-10, -0.45, -10.0))
    
    # 上下への心地よい突き抜け感と深さはそのまま維持（位置Z=10.8）
    v_cutter.translate(App.Vector(0, 0, 10.8))
    
    # お好みの2度の斜め傾きニュアンス
    v_cutter.rotate(App.Vector(0,0,0), App.Vector(0,0,1), 2.0)
    
    # 4. 豆の体から、0.9mm幅になったカッターを引き算（ブーリアンカット）
    final_bean = bean_body.cut(v_cutter)
    
    # 5. FreeCADの画面上に登録して表示
    bean_object = doc.addObject("Part::Feature", "Bean")
    bean_object.Shape = final_bean
    
    # 6. 画面の再計算と見栄えの調整（コーヒーブラウン色）
    doc.recompute()
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.ActiveDocument.ActiveView.viewAxometric()
        Gui.ActiveDocument.ActiveView.fitAll()
        Gui.getDocument(doc.Name).getObject(bean_object.Name).ShapeColor = (0.42, 0.26, 0.15)
        Gui.getDocument(doc.Name).getObject(bean_object.Name).DisplayMode = "Shaded"

# スクリプトの実行
create_optimal_split_coffee_bean()
