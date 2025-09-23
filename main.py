import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter

pdf_paths = [None] * 9
buttons = []
frames = []

def select_file(idx):
    filetypes = [("PDF files", "*.pdf"), ("All files", "*.*")]
    path = filedialog.askopenfilename(title=f"选择文件 {idx + 1}", filetypes=filetypes)
    if path:
        pdf_paths[idx] = path
        buttons[idx].config(text=os.path.basename(path), bg='lightcoral', fg='white')
        # 修改边框样式：确保 highlightthickness > 0
        frames[idx].config(highlightbackground="red", highlightthickness=3, highlightcolor="red")  # 增加厚度并设置高亮颜色

def clear_one(idx):
    pdf_paths[idx] = None
    buttons[idx].config(text=f"选择文件 {idx + 1}", bg='SystemButtonFace', fg='SystemButtonText')
    frames[idx].config(highlightthickness=0)  # 取消边框

import datetime

def merge_pdfs():
    valid = [p for p in pdf_paths if p]
    if not valid:
        messagebox.showwarning("提示", "请先选择至少一个 PDF 文件！")
        return

    merger = PdfWriter()
    try:
        for p in valid:
            merger.append(p)

        # 构造输出文件名：第一个被选中的文件名 + 时间戳
        first_name = os.path.splitext(os.path.basename(valid[0]))[0]
        time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_name = f"{first_name}_{time_stamp}.pdf"

        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), out_name)
        merger.write(out_path)
        messagebox.showinfo("完成", f"合并成功！\n已保存到：{out_path}")
    except Exception as e:
        messagebox.showerror("错误", str(e))
    finally:
        merger.close()

def clear_all():
    for i in range(9):
        pdf_paths[i] = None
        buttons[i].config(text=f"选择文件 {i + 1}")
        frames[i].config(highlightthickness=0)

# -------------------- GUI 部分 --------------------
root = tk.Tk()
root.title("PDF 合并小工具")
root.resizable(False, False)

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

for i in range(9):
    # 创建Frame作为容器，并初始化边框属性
    fr = tk.Frame(main_frame, highlightthickness=0, highlightbackground="red")  # 初始化时无边框
    fr.pack(pady=5, fill=tk.X, padx=5)  # 添加一些padx让布局更宽松
    frames.append(fr)

    btn = tk.Button(fr, text=f"选择文件 {i + 1}", width=25, command=lambda x=i: select_file(x))
    btn.pack(side=tk.LEFT, padx=(0, 5))
    buttons.append(btn)

    x_btn = tk.Button(fr, text="×", fg="white", bg="red", width=2, command=lambda x=i: clear_one(x))
    x_btn.pack(side=tk.LEFT)

merge_btn = tk.Button(main_frame, text="合并输出", width=25, bg="lightblue", command=merge_pdfs)
merge_btn.pack(pady=8)

clear_btn = tk.Button(main_frame, text="清除所有文件", width=25, bg="orange", command=clear_all)
clear_btn.pack(pady=5)

root.mainloop()