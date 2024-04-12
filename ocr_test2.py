import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import pytesseract
import numpy as np

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        # ウェブカメラの設定
        self.cap = cv2.VideoCapture(0)
        
        # 初期設定
        self.selecting = False
        self.x0 = self.y0 = self.x1 = self.y1 = 0
        
        # UIの設定
        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.start_select)
        self.canvas.bind("<B1-Motion>", self.update_select)
        self.canvas.bind("<ButtonRelease-1>", self.end_select)
        
        # OCR結果のテキストボックス
        self.text = tk.StringVar()
        self.label = ttk.Label(window, textvariable=self.text)
        self.label.pack()
        
        # 撮影ボタン
        self.capture_button = ttk.Button(window, text="Capture", command=self.capture_and_ocr)
        self.capture_button.pack()

        # 更新
        self.delay = 15
        self.update()
        
        self.window.mainloop()

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
            self.text.set(text)

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
        self.window.after(self.delay, self.update)

    def on_close(self):
        print("Closing...")
        self.cap.release()
        self.window.destroy()
# GUIを開始
root = tk.Tk()
app = App(root, "Tkinter and OpenCV for OCR")
