import cv2
import pytesseract

# Tesseractの実行ファイルへのパスを設定
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_and_extract_text():
    # Webカメラを開く
    video_source = 0 # カメラ番号（0はデフォルトのカメラ）
    vcap = cv2.VideoCapture(video_source)
    
    while True:
        # フレームを取得
        ret, frame = vcap.read()
        
        if not ret:
            break
        
        # 画像の色空間をRGBに変換
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 画像のサイズを取得
        height, width, _ = frame.shape
        print(f'height:{height}, width{width}')

        # 抽出する領域の左上と右下の座標を定義
        # ここでは、画像の中央部分を抽出する例
        # top_left = (width // 4, height // 4)
        # bottom_right = (width * 3 // 4, height * 3 // 4)
        
        # 指定した領域を抽出
        # cropped_frame = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        
        # 抽出した領域に枠を描画
        # cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        
        # ユーザーから領域の座標を入力を取得
        top_left_x = int(input("Top left X coordinate: "))
        top_left_y = int(input("Top left Y coordinate: "))
        bottom_right_x = int(input("Bottom right X coordinate: "))
        bottom_right_y = int(input("Bottom right Y coordinate: "))
        
        # 座標が画像の範囲内にあることを確認
        if top_left_x < 0 or top_left_y < 0 or bottom_right_x > width or bottom_right_y > height:
            print("Invalid coordinates. Please enter coordinates within the image dimensions.")
            continue
        
        # 指定した領域を抽出
        cropped_frame = frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
        
        # 抽出した領域に枠を描画
        cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)
        
        # 画像からテキストを抽出（数字のみ）
        config = '-c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(cropped_frame, config=config)
        
        # 抽出したテキストを表示
        # print(text)
        
        # フレームを表示
        cv2.imshow('Camera Feed', frame)
        
        # 'q'キーが押されたらループを抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # カメラとウィンドウを閉じる
    vcap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_extract_text()