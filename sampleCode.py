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

# 初期カメラ番号
video_source = 0
WIDTH = 640
HEIGHT = 480

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master.geometry("1280x550")
        self.master.title("現品票撮影アプリ")
        self.master.resizable(0, 0)
        # ---------------------------------------------------------
        # Font
        # ---------------------------------------------------------
        self.font_frame = font.Font(family='Meiryo UI', size=10, weight='normal')
        self.font_btn_big = font.Font(family='Meiryo UI', size=20, weight='bold')
        self.font_btn_small = font.Font(family='Meiryo UI', size=10, weight='bold')
        self.font_btn_too_small = font.Font(family='Meiryo UI', size=8, weight='bold')
        self.font_btn_very_small = font.Font(family='Meiryo UI', size=4, weight='bold')
        self.font_lbl_bigger = font.Font(family='Meiryo UI', size=45, weight='bold')
        self.font_lbl_big = font.Font(family='Meiryo UI', size=30, weight='bold')
        self.font_lbl_middle = font.Font(family='Meiryo UI', size=15, weight='bold')
        self.font_lbl_small = font.Font(family='Meiryo UI', size=10, weight='normal')
        # ---------------------------------------------------------
        # Open the video source
        # ---------------------------------------------------------
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
        # ボタンのサイズを検討
        self.btn_1 = tk.Button(self.frame_c, text='棒', font=self.font_btn_small)
        self.btn_1.configure(width=12, height=3, command=lambda: self.add_parts_name('T_kakuhan'))
        self.btn_1.grid(row=0, column=0, padx=10, pady=5)
        self.btn_2 = tk.Button(self.frame_c, text='板金', font=self.font_btn_small)
        self.btn_2.configure(width=12, height=3, command=lambda: self.add_parts_name('PA_bankin'))
        self.btn_2.grid(row=0, column=1, padx=10, pady=5)
        self.btn_3 = tk.Button(self.frame_c, text='板', font=self.font_btn_small)
        self.btn_3.configure(width=12, height=3, command=lambda: self.add_parts_name('AS_ban'))
        self.btn_3.grid(row=0, column=2, padx=10, pady=5)
        self.btn_4 = tk.Button(self.frame_c, text='ブレード', font=self.font_btn_small)
        self.btn_4.configure(width=12, height=3, command=lambda: self.add_parts_name('D_bure-do'))
        self.btn_4.grid(row=0, column=3, padx=10, pady=5)
        self.btn_5 = tk.Button(self.frame_c, text='スリーブ', font=self.font_btn_small)
        self.btn_5.configure(width=12, height=3, command=lambda: self.add_parts_name('SLV'))
        self.btn_5.grid(row=1, column=0, padx=10, pady=5)
        self.btn_6 = tk.Button(self.frame_c, text='ローラ', font=self.font_btn_small)
        self.btn_6.configure(width=12, height=3, command=lambda: self.add_parts_name('Mg_ro-ra-'))
        self.btn_6.grid(row=1, column=1, padx=10, pady=5)
        self.btn_7 = tk.Button(self.frame_c, text='シール非', font=self.font_btn_small)
        self.btn_7.configure(width=12, height=3, command=lambda: self.add_parts_name('ziki_si-ru_hi'))
        self.btn_7.grid(row=1, column=2, padx=10, pady=5)
        self.btn_8 = tk.Button(self.frame_c, text='シール駆', font=self.font_btn_small)
        self.btn_8.configure(width=12, height=3, command=lambda: self.add_parts_name('ziki_si-ru_ku'))
        self.btn_8.grid(row=1, column=3, padx=10, pady=5)
        self.btn_9 = tk.Button(self.frame_c, text='プルタブP', font=self.font_btn_small)
        self.btn_9.configure(width=12, height=3, command=lambda: self.add_parts_name('purutabu_HP'))
        self.btn_9.grid(row=2, column=0, padx=10, pady=5)
        self.btn_10 = tk.Button(self.frame_c, text='プルタブ', font=self.font_btn_small)
        self.btn_10.configure(width=12, height=3, command=lambda: self.add_parts_name('purutabu_CA'))
        self.btn_10.grid(row=2, column=1, padx=10, pady=5)
        self.btn_11 = tk.Button(self.frame_c, text='ホルダ駆', font=self.font_btn_small)
        self.btn_11.configure(width=12, height=3, command=lambda: self.add_parts_name('D_horuda_ku'))
        self.btn_11.grid(row=2, column=2, padx=10, pady=5)
        self.btn_none = tk.Button(self.frame_c, text='ホルダ非', font=self.font_btn_small)
        self.btn_none.configure(width=12, height=3, command=lambda: self.add_parts_name('D_horuda_hi'))
        self.btn_none.grid(row=2, column=3, padx=10, pady=5)
        self.btn_12 = tk.Button(self.frame_c, text='T容器', font=self.font_btn_small)
        self.btn_12.configure(width=12, height=3, command=lambda: self.add_parts_name('DT_youki'))
        self.btn_12.grid(row=3, column=0, padx=10, pady=5)
        self.btn_13 = tk.Button(self.frame_c, text='容器', font=self.font_btn_small)
        self.btn_13.configure(width=12, height=3, command=lambda: self.add_parts_name('C_youki'))
        self.btn_13.grid(row=3, column=1, padx=10, pady=5)
        self.btn_14 = tk.Button(self.frame_c, text='シール駆', font=self.font_btn_small)
        self.btn_14.configure(width=12, height=3, command=lambda: self.add_parts_name('C_tanbu_si-ru_ku'))
        self.btn_14.grid(row=3, column=2, padx=10, pady=5)
        self.btn_none2 = tk.Button(self.frame_c, text='シール非', font=self.font_btn_small)
        self.btn_none2.configure(width=12, height=3, command=lambda: self.add_parts_name('C_tanbu_si-ru_hi'))
        self.btn_none2.grid(row=3, column=3, padx=10, pady=5)
        self.btn_15 = tk.Button(self.frame_c, text='ブレード', font=self.font_btn_small)
        self.btn_15.configure(width=12, height=3, command=lambda: self.add_parts_name('C_bure-do'))
        self.btn_15.grid(row=4, column=0, padx=10, pady=5)
        self.btn_16 = tk.Button(self.frame_c, text='ローラ', font=self.font_btn_small)
        self.btn_16.configure(width=12, height=3, command=lambda: self.add_parts_name('C_ro-ra-'))
        self.btn_16.grid(row=4, column=1, padx=10, pady=5)
        self.btn_17 = tk.Button(self.frame_c, text='シャッタ', font=self.font_btn_small)
        self.btn_17.configure(width=12, height=3, command=lambda: self.add_parts_name('doramu_syatta'))
        self.btn_17.grid(row=4, column=2, padx=10, pady=5)
        self.btn_18 = tk.Button(self.frame_c, text='Tag', font=self.font_btn_small)
        self.btn_18.configure(width=12, height=3, command=lambda: self.add_parts_name('M-tag'))
        self.btn_18.grid(row=4, column=3, padx=10, pady=5)
        # 開始ボタン
        self.btn_job_start = tk.Button(self.frame_c, text='開始', font=self.font_btn_too_small)
        self.btn_job_start.configure(width=10, height=1, command=self.job_start)
        self.btn_job_start.grid(row=5, column=0, padx=10, pady=5)
        # 停止ボタン
        self.btn_job_stop = tk.Button(self.frame_c, text='停止', font=self.font_btn_too_small)
        self.btn_job_stop.configure(width=10, height=1, command=self.job_stop)
        self.btn_job_stop.grid(row=5, column=1, padx=10, pady=5)
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