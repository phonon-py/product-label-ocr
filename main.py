import tkinter as tk
from tkinter import LEFT, TOP, ttk
from tkinter import END
from tkinter import font
import numpy as np
import time
import cv2
from PIL import ImageTk, Image
import pytesseract

# tesseractの実行ファイルへのパス
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        # 画面サイズ
        self.master.geometry("1280x960")
        # アプリタイトル
        self.master.title("現品送票依頼番号読み取りアプリ")
        # アプリのウィンドウサイズ固定
        # self.master.resizable(0, 0)
        
        '''
        各フォント設定

        各フレーム・テキスト・ボタンのフォントやサイズ��定
        '''
        
        self.font_frame = font.Font(family='Meiryo UI', size=10, weight='normal')
        self.font_btn_big = font.Font(family='Meiryo UI', size=20, weight='bold')
        self.font_btn_small = font.Font(family='Meiryo UI', size=10, weight='bold')
        self.font_btn_too_small = font.Font(family='Meiryo UI', size=8, weight='bold')
        self.font_btn_very_small = font.Font(family='Meiryo UI', size=4, weight='bold')
        self.font_lbl_bigger = font.Font(family='Meiryo UI', size=45, weight='bold')
        self.font_lbl_big = font.Font(family='Meiryo UI', size=30, weight='bold')
        self.font_lbl_middle = font.Font(family='Meiryo UI', size=15, weight='bold')
        self.font_lbl_small = font.Font(family='Meiryo UI', size=10, weight='normal')
        
        '''
        検出範囲の初期設定
        '''
        
        self.selecting = False
        self.x0 = self.y0 = self.x1 = self.y1 = 0

        '''
        Webカメラ入力ソースの設定

        入力ソースの各種設定パラメータ
        '''
        
        # 初期カメラ番号、ノートPCの場合はインカメが0
        video_source = 0
        # カメラ描写の横サイズ
        WIDTH = 400
        # カメラ描写の縦サイズ
        HEIGHT = 240
        # Webカメラを設定
        self.cap = cv2.VideoCapture(video_source)
        # Webカメラのフレームサイズ(横)を設定
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        # Webカメラのフレームサイズ(縦)を設定
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        # 設定した横のフレームサイズを取得
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # 設定した縦のフレームサイズを取得
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # キャンバス更新間隔をミリ秒単位で設定 (15ミリ秒)
        self.delay = 15

        '''
        時間の設定
        
        '''
        # 現在の日付を取得し、指定されたフォーマットで表示
        self.now_date = time.strftime("%Y/%m/%d")

        '''
        フレームやボタンなどのウィジェットの実行
        '''
        
        self.create_widgets()
        
        # キャンバスのアップデート関数の呼び出し
        self.update()

    def create_widgets(self):
        # タイトル用のフレーム
        self.frame_title = tk.Frame()
        self.frame_title.pack()
        
        # タイトル用のラベル
        self.title_lbl = tk.Label(self.frame_title, text="現品送票 依頼番号読み取り��プリ", 
                                  font=self.font_lbl_middle)
        self.title_lbl.pack()
        
        # カメラのフレーム
        self.frame_cam = tk.LabelFrame(self.master, text='入力画像', font=self.font_frame)
        self.frame_cam.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

        # Webカメラの画像を描写するキャンパスフレーム
        self.canvas = tk.Canvas(self.frame_cam)
        self.canvas.configure(width=self.width, height=self.height)
        # columnspanを調整して中央配置のための空間を作成
        self.canvas.grid(row=0, column=0, columnspan=3)
        # canvasに対してのバインド
        self.canvas.bind("<ButtonPress-1>", self.start_select)
        self.canvas.bind("<B1-Motion>", self.update_select)
        self.canvas.bind("<ButtonRelease-1>", self.end_select)

        # 撮影ボタン
        self.btn_snapshot = tk.Button(self.frame_cam, text='撮影', font=self.font_lbl_middle)
        self.btn_snapshot.configure(height=1, command=self.capture_and_ocr)
        self.btn_snapshot.grid(row=1, column=0)  

        # クリアボタン
        self.btn_clear = tk.Button(self.frame_cam, text='クリア', font=self.font_lbl_middle)
        self.btn_clear.configure(height=1, command=None)
        self.btn_clear.grid(row=1, column=2) 

        # 判定結果用のフレーム
        self.frame_judgment_result = tk.LabelFrame(self.master, text='判定結果(仮)', font=self.font_frame)
        self.frame_judgment_result.pack()

        '''
        判定結果用の項目(列単位で配置)
        '''
        self.judgment_result_lbl1 = tk.Label(self.frame_judgment_result, text="照合判定", 
                                             font=self.font_lbl_middle)
        self.judgment_result_lbl1.grid(row=0,column=0)
        # 判定結果、実際はつきあせた結果を表示する。
        self.judgment_result_lbl2 = tk.Label(self.frame_judgment_result, text="OK", 
                                             font=self.font_lbl_middle)
        self.judgment_result_lbl2.grid(row=1,column=0,padx=10, pady=10)

        self.judgment_result_lbl3 = tk.Label(self.frame_judgment_result, text="担当", 
                                             font=self.font_lbl_middle)
        self.judgment_result_lbl3.grid(row=2,column=0,padx=10, pady=10)

        self.judgment_result_lbl4 = tk.Entry(self.frame_judgment_result, font=self.font_lbl_middle,
                                             width=10)
        self.judgment_result_lbl4.insert(0, "入力してください")
        self.judgment_result_lbl4.grid(row=3,column=0, padx=10, pady=10)
        # Entryクリックしたら削除する関数の実行
        self.judgment_result_lbl4.bind("<FocusIn>", None)

        '''
        購入品情報の項目

        '''
        self.judgment_result_lbl5 = tk.Label(self.frame_judgment_result, text="購入品状況", 
                                             font=self.font_lbl_middle)
        self.judgment_result_lbl5.grid(row=0,column=1)
        
        # 購入品状況結果、照合結果を参照する
        self.judgment_result_lbl6 = tk.Label(self.frame_judgment_result, text="未", 
                                             font=self.font_lbl_middle)
        self.judgment_result_lbl6.grid(row=1,column=1, padx=10, pady=10)

        self.judgment_result_lbl7 = tk.Label(self.frame_judgment_result, text='日付', 
                                             font=self.font_lbl_middle)
        self.judgment_result_lbl7.grid(row=2,column=1, padx=10, pady=10)

        self.judgment_result_lbl8 = tk.Entry(self.frame_judgment_result,
                                             font=self.font_lbl_middle,
                                             width=10)
        self.judgment_result_lbl8.insert(0, str(self.now_date))
        
        self.judgment_result_lbl8.grid(row=3,column=1, padx=10, pady=10)

        '''
        依頼番号読��取り表示
        '''
        self.judgment_result_lbl10 = tk.Entry(self.frame_judgment_result,
                                             font=self.font_lbl_middle,
                                             width=30)
        self.judgment_result_lbl10.insert(0, "")
        self.judgment_result_lbl10.grid(row=4,column=0, padx=10, pady=10,columnspan=2)

        '''
        納入状況参照
        
        '''
        # タイトル用のフレーム
        self.display_delivery_status_frame = tk.Frame()
        self.display_delivery_status_frame.pack()
        
        # タイトル用のラベル
        self.title_lbl = tk.Label(self.display_delivery_status_frame, text="現品送票 依頼番号読み取り", 
                                  font=self.font_lbl_middle)
        self.title_lbl.pack()
        
    def start_select(self, event):
        # 選択開始
        self.selecting = True
        self.x0 = event.x
        self.y0 = event.y

    def update_select(self, event):
        # 選択範囲の更新
            if self.selecting:
                if self.x1 != event.x or self.y1 != event.y: # 選択範囲が変更された場合
                    self.selection_changed = True # フラグをTrueに設定
                    self.x1 = event.x
                    self.y1 = event.y
                    self.redraw()

    def end_select(self, event):
        # 選択終了
        self.selecting = False
        self.x1 = event.x
        self.y1 = event.y
        self.redraw() # 選択範囲を描画

    def capture_and_ocr(self):
        # 選択された範囲の画像を抽出してOCRを実行
        if self.x1 > self.x0 and self.y1 > self.y0:
            roi = self.frame[self.y0:self.y1, self.x0:self.x1]
            
            '''
            画像デバック用
            
            '''
            print(f'選択範囲roi:{roi}')
            
            # 画像を2値化する
            # _, binary_roi = cv2.threshold(roi, 90, 255, cv2.THRESH_BINARY)
            
            # ノイズ除去
            # denoised_roi = cv2.fastNlMeansDenoising(roi, None, 1, 7, 21)
            
            # ウィンドウを作成
            # cv2.namedWindow('Denoised Binary ROI', cv2.WINDOW_NORMAL)

            # ノイズ除去された2値化された画像を表示
            # cv2.imshow('Denoised Binary ROI', roi)


            # キーが押されるまで待機
            # cv2.waitKey(0)
            
            
            # 数字とハイフンのみ
            config = '--oem 3 --psm 6 -c tessedit_char_whitelist="0123456789-"'
            text = pytesseract.image_to_string(roi, config=config)
            
            # OCR結果をself.judgment_result_lbl10に設定
            self.judgment_result_lbl10.delete(0, tk.END) # 既存のテキストを削除
            self.judgment_result_lbl10.insert(0, text) # OCR結果を挿入


    def redraw(self):
        # キャンバスを更新
        self.canvas.delete("rect")
        self.canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, outline="red", tag="rect")

    def update(self):
        # カメラから画像を取得してキャンバスに表示
        ret, self.frame = self.cap.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            if self.selecting or self.x1 > self.x0 and self.y1 > self.y0: # 選択が終了しても選択範囲を描画
                self.redraw()
        self.master.after(self.delay, self.update)
    
def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
