import qrcode
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from PIL import Image
from PIL import ImageTk
import io


# the URL of the server
SERVER_URL = "http://localhost:8000/generate_qr_code"

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x500")
        self.root.title("QR Code Generator")
        
        self.text_var = tk.StringVar()
        self.url_entry = tk.Entry(self.root, textvariable=self.text_var, font=("Helvetica", 16))
        self.url_entry.pack(pady=20)
        
        self.generate_btn = tk.Button(self.root, text="Generate QR Code", command=self.generate_qr_code)
        self.generate_btn.pack()
        
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=20)
        
        self.name_label = tk.Label(self.root, text="")
        self.name_label.pack(pady=10)
    
    def generate_qr_code(self):
        url = self.text_var.get()
        if not url:
            messagebox.showerror("QR Code Generator", "Please enter a URL.")
            return
        
        # send the URL to the server
        response = requests.post(SERVER_URL, data={"url": url})
        
        if response.status_code == 200:
            # get the image data from the server response
            img_data = response.content
            
            # create a PIL image from the image data
            img = Image.open(io.BytesIO(img_data))
            
            # display the image on the GUI
            self.image_label.imgtk = ImageTk.PhotoImage(img)
            self.image_label.configure(image=self.image_label.imgtk)
            
            # specify file path and name to save the image
            default_filename = f"{url.replace(' ', '_')}.png"
            filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")], initialfile=default_filename)
            
            try:
                # save the image to disk
                img.save(filename)
                self.name_label.config(text=f"QR code for {url} generated successfully and saved at {filename}")
                messagebox.showinfo(f"QR Code Generator - {url}", f"QR code for {url} generated successfully and saved at {filename}")
            except Exception as e:
                messagebox.showerror("QR Code Generator", f"Error saving QR code: {e}")
        else:
            # display the error message from the server response
            error_msg = response.text
            messagebox.showerror("QR Code Generator", error_msg)

if __name__ == '__main__':
    root = tk.Tk()
    QRCodeGenerator(root)
    root.mainloop()
