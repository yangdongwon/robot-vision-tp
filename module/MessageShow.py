import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def messageShow(image):
	root = tk.Tk()
	w = root.winfo_screenwidth()
	h = root.winfo_screenheight()

	'''
	image_tk = ImageTk.PhotoImage(Image.fromarray(image))

    # 새로운 Toplevel 창 생성
	image_window = tk.Toplevel()

    # 이미지를 Label 위젯을 사용하여 표시
	label = tk.Label(image_window, image=image_tk)
	label.image = image_tk  # 가비지 컬렉션을 피하기 위한 레퍼런스 유지
	label.pack()
	'''
	aw = 500
	ah = 500

	cw = int(w/2 - aw/2)
	ch = int(h/2 - ah/2)
	root.withdraw()
	root.geometry(f"{aw}x{ah}+{cw}+{ch}")
	
	image_tk = ImageTk.PhotoImage(Image.fromarray(image))

    # 새로운 Toplevel 창 생성
	image_window = tk.Toplevel()

    # 이미지를 Label 위젯을 사용하여 표시
	label = tk.Label(image_window, image=image_tk)
	label.image = image_tk  # 가비지 컬렉션을 피하기 위한 레퍼런스 유지
	label.pack()

	result = messagebox.askquestion("Question", "Do you want preprocessing?")
	root.destroy()

	return result
	root.mainloop()

def messageShow_error_paper():
	root = tk.Tk()
	w = root.winfo_screenwidth()
	h = root.winfo_screenheight()

	aw = 500
	ah = 500

	cw = int(w/2 - aw/2)
	ch = int(h/2 - ah/2)
	root.withdraw()
	root.geometry(f"{aw}x{ah}+{cw}+{ch}")
	
	messagebox.showinfo("Notification", "Paper not recognized. Select the corner of the wall, the corner of the paper, and press enter ")
	root.destroy()
	
def messageShow_error_wall():
	root = tk.Tk()
	w = root.winfo_screenwidth()
	h = root.winfo_screenheight()

	aw = 500
	ah = 500

	cw = int(w/2 - aw/2)
	ch = int(h/2 - ah/2)
	root.withdraw()
	root.geometry(f"{aw}x{ah}+{cw}+{ch}")

	messagebox.showinfo("Notification", "wall not recognized. Select the corner of the wall, the corner of the paper, and press enter ")
	root.destroy()
	
def messageShow_error_run(e):
	root = tk.Tk()
	w = root.winfo_screenwidth()
	h = root.winfo_screenheight()

	aw = 500
	ah = 500

	cw = int(w/2 - aw/2)
	ch = int(h/2 - ah/2)
	root.withdraw()
	root.geometry(f"{aw}x{ah}+{cw}+{ch}")
	
	messagebox.showinfo("Error", "Error: "+ str(e) + "\nSelect the corner of the wall, the corner of the paper, and press enter ")
	root.destroy()
	
def messageShow_self_choice():
	root = tk.Tk()
	w = root.winfo_screenwidth()
	h = root.winfo_screenheight()

	aw = 500
	ah = 500

	cw = int(w/2 - aw/2)
	ch = int(h/2 - ah/2)
	root.withdraw()
	root.geometry(f"{aw}x{ah}+{cw}+{ch}")
	
	result = messagebox.askquestion("Notification", "Do you want to set the corners on your own??")
	root.destroy()
	
	return result
	
def messageShow_length(length,direction):
	root = tk.Tk()
	w = root.winfo_screenwidth()
	h = root.winfo_screenheight()

	aw = 500
	ah = 500

	cw = int(w/2 - aw/2)
	ch = int(h/2 - ah/2)
	root.withdraw()
	root.geometry(f"{aw}x{ah}+{cw}+{ch}")
	
	messagebox.showinfo("Notification", direction + "length: " + str(length) + "m")
	root.destroy()
	
def messageShow_length_mean(len1,len2,len3):
	root = tk.Tk()
	w = root.winfo_screenwidth()
	h = root.winfo_screenheight()

	aw = 500
	ah = 500

	cw = int(w/2 - aw/2)
	ch = int(h/2 - ah/2)
	root.withdraw()
	root.geometry(f"{aw}x{ah}+{cw}+{ch}")
	
	messagebox.showinfo("Notification", "가로평균: " + str(len1) + "m\n" + "세로평균: " + str(len2) + "m\n" + "높이: " + str(len3) + "m\n")
	root.destroy()

