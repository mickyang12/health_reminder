#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康提醒程式 - 每30分鐘提醒離開電腦走動，並將螢幕變黑5分鐘
"""

import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def show_reminder():
    """顯示提醒視窗"""
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗
    
    # 在最上層顯示訊息框
    root.attributes('-topmost', True)
    messagebox.showwarning(
        "健康提醒", 
        "該起來走動了！\n\n已經坐了30分鐘\n請站起來活動一下\n\n螢幕即將變黑5分鐘",
        parent=root
    )
    root.destroy()

def black_screen(duration):
    """顯示全螢幕黑色視窗"""
    root = tk.Tk()
    root.title("休息時間")
    
    # 設定全螢幕
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.configure(background='black', cursor='none')
    
    # 禁用 Alt+F4 和其他關閉方式
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    # 建立顯示文字的標籤
    time_label = tk.Label(
        root,
        text="",
        font=("Arial", 52, "bold"),
        fg="white",
        bg="black"
    )
    time_label.pack(expand=True)
    
    message_label = tk.Label(
        root,
        text="休息時間 - 請離開電腦走動一下\n\n(螢幕會自動恢復)",
        font=("Arial", 24),
        fg="gray",
        bg="black"
    )
    message_label.pack(expand=True)
    
    # 倒數計時
    remaining_time = [duration]  # 使用列表以便在內部函數中修改
    
    def update_countdown():
        if remaining_time[0] > 0:
            minutes = remaining_time[0] // 60
            seconds = remaining_time[0] % 60
            time_label.config(text=f"{minutes:02d}:{seconds:02d}")
            remaining_time[0] -= 1
            root.after(1000, update_countdown)  # 每秒更新
        else:
            root.quit()  # 改用 quit() 確保能退出 mainloop
            root.destroy()
    
    # 開始倒數
    update_countdown()
    
    # 進入主迴圈
    root.mainloop()
    
    # 確保視窗被銷毀
    try:
        root.destroy()
    except:
        pass

def main():
    """主程式"""
    work_interval = 3 * 60  # 30分鐘（秒）
    lock_duration = 1 * 60   # 5分鐘（秒）
    
    print("=" * 50)
    print("健康提醒程式已啟動")
    print(f"工作間隔: {work_interval // 60} 分鐘")
    print(f"休息時間: {lock_duration // 60} 分鐘")
    print("=" * 50)
    print("按 Ctrl+C 可以停止程式\n")
    
    try:
        while True:
            # 等待30分鐘
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 開始工作計時...")
            time.sleep(work_interval)
            
            # 顯示提醒
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 顯示提醒訊息")
            show_reminder()
            
            # 顯示黑色螢幕
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 休息時間開始（{lock_duration // 60}分鐘）")
            black_screen(lock_duration)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 休息時間結束\n")
            
    except KeyboardInterrupt:
        print("\n\n程式已停止")
        print("感謝使用健康提醒程式！")

if __name__ == "__main__":
    main()
