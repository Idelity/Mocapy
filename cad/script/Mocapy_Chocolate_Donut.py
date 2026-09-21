import FreeCAD as App
import Part
import math

def create_chocolate_donut():
    # 1. 新規ドキュメントの作成
    doc = App.newDocument("Mocapy_Chocolate_Donut")
    
    # 2. ドーナツの生地（直径7.4mm、厚み約2.4mmのぷっくりした輪っか）
    donut_base = Part.makeTorus(2.5, 1.2)
    
    # 3. ★完全リニューアル：とろ〜り波打つ「チョコレートコーティング」の作成
    # 40個の細かいパーツを少しずつ角度を変えながら円状に並べて、
    # 裾が「上に行ったり下に行ったり」と不規則に波打つ立体を編み上げます
    chocolate_pieces = []
    num_segments = 40
    
    for i in range(num_segments):
        angle = (2 * math.pi / num_segments) * i
        
        # チョコレートが下にとろけている波（タレ）の深さを数式で不規則に計算
        # 4箇所ほど、下に少し長く垂れる部分（波の底）を作ります
        wave_height = 0.25 * math.sin(angle * 4) + 0.1 * math.cos(angle * 2)
        
        # チョコの一片となる小さな球体を作成（生地よりほんの少し大きく膨らませる）
        piece = Part.makeSphere(1.25)
        # ドーナツの円周上に配置
        x = 2.5 * math.cos(angle)
        y = 2.5 * math.sin(angle)
        # 計算した波の高さ（とろみ）をZ軸（上下）に適用して、下半分を少しボリュームアップ
        z = 0.15 + wave_height
        
        piece.translate(App.Vector(x, y, z))
        chocolate_pieces.append(piece)
    
    # バラバラのチョコの一片を1つの大きな「とろける滑らかな液体パーツ」に合体
    raw_chocolate = chocolate_pieces[0]
    for piece in chocolate_pieces[1:]:
        raw_chocolate = raw_chocolate.fuse(piece)
        
    # ドーナツの下半分からはみ出た余計なチョコをスパッとカット
    clipper = Part.makeBox(20, 20, 10, App.Vector(-10, -10, -10.0))
    final_chocolate = raw_chocolate.cut(clipper)
    
    # 4. ドーナツ生地とチョコレートを合体させて完成！
    final_donut = donut_base.fuse(final_chocolate)
    
    # 全体を優しく面取り（フィレット）して、さらに美味しそうなとろみ感を強調
    edges_to_blend = []
    for edge in final_donut.Edges:
        edges_to_blend.append(edge)
    try:
        final_donut = final_donut.makeFillet(0.15, edges_to_blend)
    except:
        pass
        
    # 5. FreeCADの画面上に登録して表示
    donut_object = doc.addObject("Part::Feature", "Chocolate_Donut")
    donut_object.Shape = final_donut
    
    # 6. 画面の再計算と見栄えの調整（美味しそうなビターチョコ色を設定）
    doc.recompute()
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.ActiveDocument.ActiveView.viewAxometric()
        Gui.ActiveDocument.ActiveView.fitAll()
        # チョコがかかった状態がわかりやすいよう、チョコレート色（RGB）に設定
        Gui.getDocument(doc.Name).getObject(donut_object.Name).ShapeColor = (0.25, 0.15, 0.08)
        Gui.getDocument(doc.Name).getObject(donut_object.Name).DisplayMode = "Shaded"

# スクリプトの実行
create_chocolate_donut()
