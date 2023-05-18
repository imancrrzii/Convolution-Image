import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Image Editor Convolution")
        self.frame1 = tk.Frame(self)
        self.frame1.pack(side="left")
        self.frame2 = tk.Frame(self)
        self.frame2.pack(side="right", fill="x", expand=True)
        self.addBtn = tk.Button(self.frame1, text="Add a Picture",bg='#3B71CA',
        fg='#fff', font=('cambria 12 bold'),
        command=self.addImage, width=12)
        self.sharpBtn = tk.Button(self.frame1, text="Sharpen", bg='#4a148c',
        fg='#fff', font=('cambria 12 bold'),
        command=lambda: self.useFilter("sharpen"), width=12)
        self.blurBtn = tk.Button(self.frame1, text="Blur", bg='#00b8d4', fg='#fff',
        font=('cambria 12 bold'), command=lambda:
        self.useFilter("blur"), width=12)
        self.sobelBtn = tk.Button(self.frame1, text="Sobel", bg='#ffd600',
        fg='#fff', font=('cambria 12 bold'),
        command=lambda: self.useFilter("sobel"), width=12)
        self.saveBtn = tk.Button(self.frame1, text="Save", bg='#14A44D', fg='#fff',
        font=('cambria 12 bold'),
        command=self.saveImage, width=12)

        self.addBtn.pack(side="top", padx=20, pady=20)
        self.sharpBtn.pack(side="top", padx=20, pady=20)
        self.blurBtn.pack(side="top", padx=20, pady=20)
        self.sobelBtn.pack(side="top", padx=20, pady=20)
        self.saveBtn.pack(side="top", padx=20, pady=20)

        self.canvas1 = tk.Canvas(self.frame2, width=400, height=400)
        self.canvas1.pack(side="left")
        self.canvas2 = tk.Canvas(self.frame2, width=400, height=400)
        self.canvas2.pack(side="right")
        self.startImage = None
        self.processedImage = None
    def addImage(self):
        imgPath = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("PNG file", "*.png"), ("jpg file", "*.jpg")])
        if not imgPath:
            return
        self.startImage = cv2.imread(imgPath)
        aspect_ratio = float(self.startImage.shape[1]) / float(self.startImage.shape[0])
        if self.startImage.shape[0] > self.startImage.shape[1]:
            newHeight = 400
            newWidth = int(newHeight * aspect_ratio)
        else:
            newWidth = 400
            newHeight = int(newWidth / aspect_ratio)
        self.startImage = cv2.resize(self.startImage, (newWidth,
        newHeight))
        self.showImage(self.startImage, self.canvas1)
    def showImage(self, img, canvas):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        canvas.delete("all")
        canvas.create_image(200, 200, image=img)
        canvas.img = img

    def useFilter(self, filterTypes):
        if self.startImage is None:
            messagebox.showerror("Failed, please add a photo")
            return
        if "sharpen" in filterTypes:
            self.processedImage = self.startImage.copy()
            sharpenKernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
            self.processedImage = cv2.filter2D(self.processedImage, -1,
            sharpenKernel)
        elif "blur" in filterTypes:
            kernel = np.ones((15,15),np.float32)/225
            self.processedImage = cv2.filter2D(self.startImage,-1,kernel)
        elif "sobel" in filterTypes:
            self.processedImage = cv2.cvtColor(self.startImage,
            cv2.COLOR_BGR2GRAY)
            self.processedImage = cv2.Sobel(self.processedImage, cv2.CV_64F,
            1, 0, ksize=3)
            self.processedImage = cv2.convertScaleAbs(self.processedImage)
            self.showImage(self.processedImage, self.canvas2)
    def saveImage(self):
        if self.processedImage is None:
            messagebox.showerror("Failed, Image not saved")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if not file_path:
            return 
        cv2.imwrite(file_path, self.processedImage) 
        messagebox.showinfo("Success", "Image saved successfully")

if __name__ == "__main__":
    app = App()
    app.mainloop()