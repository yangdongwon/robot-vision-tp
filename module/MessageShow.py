import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def messageShow(image):
	root = tk.Tk()
	w = root.winfo_screenwidth()
	h = root.winfo_screenheight()

	image_tk = ImageTk.PhotoImage(Image.fromarray(image))

    # 새로운 Toplevel 창 생성
	image_window = tk.Toplevel()

    # 이미지를 Label 위젯을 사용하여 표시
	label = tk.Label(image_window, image=image_tk)
	label.image = image_tk  # 가비지 컬렉션을 피하기 위한 레퍼런스 유지
	label.pack()

	aw = 500
	ah = 500

	cw = int(w/2 - aw/2)
	ch = int(h/2 - ah/2)
	root.withdraw()
	root.geometry(f"{aw}x{ah}+{cw}+{ch}")

	result = messagebox.askquestion("Question", "Do you want preprocessing?")
	root.destroy()

	return result
#root.mainloop()
