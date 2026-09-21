import FreeCAD as App
import Part

def create_optimal_mug_with_coffee():
    # 1. 新規ドキュメントの作成
    doc = App.newDocument("Mocapy_Mug")
    
    # 2. マグカップの外側（直径9mm、高さ10mmの円柱）
    outer_cylinder = Part.makeCylinder(4.5, 10.0)
    
    # 3. マグカップの内側のくぼみ（直径7.4mm、高さ9mmの円柱）
    inner_cylinder = Part.makeCylinder(3.7, 9.0)
    inner_cylinder.translate(App.Vector(0, 0, 1.0)) # 底を1mm残す
    
    # 外側から内側をくり抜いて「カップの器」にする
    mug_body = outer_cylinder.cut(inner_cylinder)
    
    # 4. 取っ手（ハンドル）の作成
    torus = Part.makeTorus(2.2, 0.6) # 少し太めで可愛い取っ手
    torus.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90.0)
    torus.translate(App.Vector(4.0, 0, 5.0)) # 側面に綺麗に配置
    
    # カップ本体と取っ手を結合（この時点では内側にとっ手が見えています）
    raw_mug = mug_body.fuse(torus)
    
    # 5. ★完全修正：内側の取っ手を隠す「飲み物（コーヒー）」の立体を作成
    # カップの内径（半径3.7mm）にピッタリはまる円柱を作ります
    # 取っ手の上部（高さ7.2mm）が完全に隠れるよう、液面の高さを「7.5mm」に設定
    coffee_liquid = Part.makeCylinder(3.7, 7.5)
    coffee_liquid.translate(App.Vector(0, 0, 1.0)) # カップの底（1mm）の上に配置
    
    # カップ本体と飲み物の液体データを一体化（これで内側の取っ手が完全に埋まります）
    filled_mug = raw_mug.fuse(coffee_liquid)
    
    # 6. 全体に「丸み（フィレット）」を持たせる処理
    edges_to_blend = []
    for edge in filled_mug.Edges:
        edges_to_blend.append(edge)
        
    try:
        # 全体のカドを優しく丸める（液面のフチも滑らかになります）
        final_mug = filled_mug.makeFillet(0.4, edges_to_blend)
    except:
        final_mug = filled_mug.makeFillet(0.2, filled_mug.Edges)
    
    # 7. FreeCADの画面上に登録して表示
    mug_object = doc.addObject("Part::Feature", "Mug")
    mug_object.Shape = final_mug
    
    # 8. 画面の再計算と見栄えの調整（液体が入ったイメージが沸きやすいように色分け）
    doc.recompute()
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.ActiveDocument.ActiveView.viewAxometric()
        Gui.ActiveDocument.ActiveView.fitAll()
        # 全体を真っ白に設定（3Dプリント時は一体成形されます）
        Gui.getDocument(doc.Name).getObject(mug_object.Name).ShapeColor = (0.95, 0.95, 0.95)
        Gui.getDocument(doc.Name).getObject(mug_object.Name).DisplayMode = "Shaded"

# スクリプトの実行
create_optimal_mug_with_coffee()
