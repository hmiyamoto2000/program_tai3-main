import os
import cv2
import numpy as np
import math
import pandas as pd

# ディレクトリのパスを指定
directory_path = 'measurement_before'

results = []

# 座標が格納されている配列から始点と終点を取り出す
# Retrieve the starting and ending points from the array where the coordinates are stored
def filter_coords(coords):
    start_coords = coords[0]
    end_coords = coords[-1]
    if len(coords) > 2:
        for i in range(1, len(coords)):
            if start_coords[1] > coords[i][1]:  
                start_coords = coords[i]
            if end_coords[1] < coords[i][0]:  
                end_coords = coords[i]
        return [start_coords, end_coords]
    else:
        return coords


# tifファイルの読み込みとファイル名の一覧表示
tif_files = [f for f in os.listdir(directory_path) if f.endswith('.tif')]
for file in tif_files:
    file_path = os.path.join(directory_path, file)
    image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)  # 画像を読み込む（IMREAD_UNCHANGEDを使用すると、元のフォーマットで画像が読み込まれます）
    print(f'Loaded {file}')
    filename_without_ext = os.path.splitext(file)[0]
    
    #読み取りたい色のBGR値指定
    yellow = [0,254,255]
    yellow2 = [0,254,254]
    cyan = [255,255,0]
    blue = [255,0,2]
    
    #座標の読み取り、（直線の場合、始点と終点の座標だけ取り出す）
    yellow_coords = np.argwhere(np.all(image == yellow, axis=-1))
    yellow2_coords = np.argwhere(np.all(image == yellow2, axis=-1))
    cyan_coords = np.argwhere(np.all(image == cyan, axis=-1))
    blue_coords = filter_coords(np.argwhere(np.all(image == blue, axis=-1)))
    
    yellow_dist = np.linalg.norm(yellow_coords[0] - yellow_coords[1])
    yellow2_1_dist = np.linalg.norm(np.array(yellow2_coords[0])-np.array(yellow2_coords[1])) #全体
    cyan_dist = np.linalg.norm(cyan_coords[0] - cyan_coords[1])
    blue_dist = np.linalg.norm(blue_coords[0] - blue_coords[1])

    # 胸鰭から背びれの距離を求める
    # Find the distance from the pectoral fin to the dorsal fin
    upper_dist = np.linalg.norm(yellow_coords[0] - cyan_coords[0])
    lower_dist = np.linalg.norm(yellow_coords[0] - cyan_coords[1])
    
    # 体長(横)を1としたときの体長(縦)の比率を求める
    # Find the ratio of body length (height) to body length (width) as 1
    R1_Ratio1 = yellow_dist / blue_dist

    # 体長(縦)を1としたときの胸鰭の幅の比率を求める
    # Find the ratio of the width of the pectoral fins when the body length (height) is 1
    Ratio2 = cyan_dist / yellow_dist

    # 体長(縦)を1としたときの胸鰭(上)の幅の比率を求める
    # Find the ratio of the width of the pectoral fin (upper) to the body length (height) as 1
    Ratio3 = upper_dist / yellow_dist

    # 体長(縦)を1としたときの胸鰭(下)の幅の比率を求める
    # Find the ratio of the width of the pectoral fin (lower) to the body length (height) as 1
    Ratio4 = lower_dist / yellow_dist
    
    # 体長(縦)を1としたときの胸鰭(下)の幅の比率を求める
    # Find the ratio of the width of the pectoral fin (lower) to the body length (height) as 1
    Ratio5 = 1-raito4

    # 肛門の中心部の直角ライン全体に対する全長の割合
    R2_Ratio6 = yellow2_1_dist / blue_dist
    
    # 肛門ラインと胸鰭ラインの全体に対する割合
    R3_Ratio7 = yellow2_1_dist / yellow_dist


    # 結果を表示する
    # Show results
    #print("体長(横)を1としたときの体長(縦)の比率:", round(raito1,3))
    #print("体長(縦)を1としたときの胸鰭の幅の比率:", round(raito2,3))
    #print("体長(縦)を1としたときの胸鰭(上)の幅の比率:", round(raito3,3))
    #print("体長(縦)を1としたときの胸鰭(下)の幅の比率:", round(raito4,3))
    #print("体長(縦)を1としたときの胸鰭(下)の幅の比率(Y2-C2)/(Y1-Y2):", round(raito5,3))
    #print("肛門からの体長(縦)を1としたときの肛門から中心線まで(下)の幅の比率:", round(raito6,3))
    print(round(R1_Ratio1,3))
    print(round(Ratio2,3))
    print(round(Ratio3,3))
    print(round(Ratio4,3))
    print(round(Ratio5,3))
    print(round(R2_Ratio6,3))
    print(round(R3_Ratio7,3))


    
    # 結果をリストに追加
    results.append([filename_without_ext, R1_Ratio1, Ratio2, Ratio3, Ratio4, Ratio5, raito6,raito7])

# データフレームの作成
df = pd.DataFrame(results, columns=['Filename', 'R1_Ratio1', 'Ratio2', 'Ratio3', 'Ratio4', 'Ratio5', 'R2_Ratio6','R3_Ratio7'])

# エクセルファイルに書き込み
output_path = 'output.xlsx'
df.to_excel(output_path, index=False)
