import tkinter as tk
from tkinter import LEFT, TOP, ttk
from tkinter import END
from tkinter import filedialog
from tkinter import font
import time
import os
import shutil
import cv2
import PIL.Image, PIL.ImageTk

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        # 画面サイズ
        self.master.geometry("1280x550")
        # アプリタイトル
        self.master.title("現品送票依頼番号読み取りアプリ")
        # アプリのウィンドウサイズ固定
        self.master.resizable(0, 0)
        
        '''
        各フォント設定

        各フレーム・テキスト・ボタンのフォントやサイズの設定
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
        Webカメラ入力ソースの設定

        入力ソースの各種設定パラメータ
        '''
        # 初期カメラ番号
        video_source = 0
        # カメラ描写の横サイズ
        WIDTH = 640
        # カメラ描写の縦サイズ
        HEIGHT = 480

        self.vcap = cv2.VideoCapture(video_source)
        self.vcap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        self.width = self.vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(self.width, self.height)
        # ---------------------------------------------------------
        # Widget
        # ---------------------------------------------------------
        self.create_widgets()
        # ---------------------------------------------------------
        # Canvas Update
        # ---------------------------------------------------------
        self.delay = 15 #[mili seconds]
        # self.update()
    
    def create_widgets(self):
        #Frame_Camera
        self.frame_cam = tk.LabelFrame(self.master, text = 'カメラ画像', font=self.font_frame)
        self.frame_cam.pack(side=LEFT, anchor=tk.NW)
        #Canvas
        self.canvas1 = tk.Canvas(self.frame_cam)
        self.canvas1.configure(width= self.width, height=self.height)
        self.canvas1.pack()
        
        # 部品名用のフレーム
        self.frame_c = tk.LabelFrame(self.master, text='部品名', font=self.font_frame)
        self.frame_c.pack()
        # ディレクトリ用フレーム
        self.frame_dir = tk.Frame(self.master)
        self.frame_dir.pack(side=TOP)
        # dir参照先を配置
        self.entry_ws = tk.StringVar()
        self.dir_entry = ttk.Entry(self.frame_dir, textvariable=self.entry_ws, width=50)
        # self.dir_entry.insert(0)
        self.dir_entry.pack(side=LEFT)
        # 参照ボタン
        self.dir_button = ttk.Button(self.frame_dir, text="保存先参照", command=self.dirdialog_clicked)
        self.dir_button.pack(side=LEFT)
        
        # 撮影用のフレーム
        self.frame_snap = tk.LabelFrame(self.master, text='撮影', font=self.font_frame)
        self.frame_snap.pack(anchor=tk.S)
        # 部品名の表示
        self.show_parts_name = tk.Listbox(self.frame_snap, width=30, height=1, font=self.font_btn_small)
        self.show_parts_name.grid(row=0, column=0)
        # 撮影ボタン
        self.btn_snapshot = tk.Button(self.frame_snap, text='撮影', font=self.font_lbl_middle)
        self.btn_snapshot.configure(width=40, height=1, command=self.press_snapshot_button)
        self.btn_snapshot.grid(row=1, column=0, columnspan=2)
    
        ''' 
        def update(self):
            # カメラの設定
            self.vcap.set(cv2.CAP_PROP_AUTOFOCUS, 1) # オートフォーカスの制御 0でOFF
            #self.vcap.set(cv2.CAP_PROP_FOCUS, 35) # フォーカス値は0~250の範囲で5刻みに設定
            _, frame = self.vcap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            #self.photo -> Canvas
            self.canvas1.create_image(0,0, image= self.photo, anchor = tk.NW)
            self.master.after(self.delay, self.update)
        '''    
    
    def dirdialog_clicked(self):
        global now_path
        dir_path = filedialog.askdirectory(initialdir=r'C:\Users')
        # pathの移動
        os.chdir(dir_path)
        self.entry_ws.set(dir_path)
        now_path = os.getcwd()
        print(f'現在のパスは{now_path}です')
    
    def add_parts_name(self, string):
        global parts_name
        parts_name = string
        self.show_parts_name.delete(0, END)
        self.show_parts_name.insert(END, parts_name)
    
    def reset(self):
        self.show_parts_name.delete(0, END)
        self.btn_1.configure(state='normal')
        self.btn_2.configure(state='normal')
        self.btn_3.configure(state='normal')
        self.btn_4.configure(state='normal')
        self.btn_5.configure(state='normal')
        self.btn_6.configure(state='normal')
        self.btn_7.configure(state='normal')
        self.btn_8.configure(state='normal')
        self.btn_9.configure(state='normal')
        self.btn_10.configure(state='normal')
        self.btn_11.configure(state='normal')
        self.btn_12.configure(state='normal')
        self.btn_13.configure(state='normal')
        self.btn_14.configure(state='normal')
        self.btn_15.configure(state='normal')
        self.btn_16.configure(state='normal')
        self.btn_17.configure(state='normal')
        self.btn_18.configure(state='normal')
        self.btn_none.configure(state='normal')
    
    def press_snapshot_button(self):
        # ディレクトリインスタンス化
        dir_name = f'./{parts_name + "_" + time.strftime("%Y-%m")}'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        # Get a frame from the video source
        _, frame = self.vcap.read()
        # イメージネームのインスタンス
        img_name = parts_name + '_' + time.strftime( "%Y-%m-%d-%H-%M-%S" ) + ".jpg"
        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite(img_name,
                    cv2.cvtColor( frame1, cv2.COLOR_BGR2RGB ) )
        # リストボックスの削除
        self.show_parts_name.delete(0, END)
        self.reset()
        try:
            shutil.move(now_path + '\\' + img_name,
                            now_path + '\\' + dir_name)
        except:
            shutil.move(r'C:\Users' + '\\' + img_name,
                        r'C:\Users' + '\\' + dir_name)
    def app_close(self):
        self.master.destroy()
        self.vcap.release()
    
    def job_start(self):
        self.job_enable = True
    
    def job_stop(self):
        self.job_enable = False
        print('停止しました。')
    
def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()