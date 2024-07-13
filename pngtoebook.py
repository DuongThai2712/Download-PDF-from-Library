import requests
import os
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4      #thay đổi import pagesize tuỳ theo mong muốn
from reportlab.lib.utils import ImageReader

def download(url, page):                    #tải ảnh từ url, tham số trang
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        png_filename = f"page_{page}.png"
        img.save(png_filename, 'PNG')  # Lưu lại dưới dạng ảnh PNG (không bị vỡ ảnh)
        return png_filename
    else:
        print(f"Không tải được ảnh trong url")
        return None
    
def toPDF(image_list, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=A4) #Thay pagesize tuỳ thuộc vào cỡ xuất mong muốn
    width, height = A4

    for img_path in image_list:
        img = Image.open(img_path)
        img_width, img_height = img.size
        aspect = img_height / img_width
        new_height = (width * aspect)
        img = img.resize((int(width), int(new_height)), Image.LANCZOS)
        c.drawImage(ImageReader(img_path), 0, height - new_height, width=width, height=new_height)
        c.showPage()

    c.save()

def main():

    # Phần này có thể tuỳ biến hoặc thay đổi base_url phù hợp với nhu cầu (vd sử dụng input() thay vì gán trực tiếp)
    base_url = "https://ir.vnulib.edu.vn/flowpaper/services/view.php?doc={}&format=jpg&page={}&subfolder={}"
    num_pages = 8
    doc= 141209814028176636452558868677022990123
    subfolder = "14/12/09/"

    images = []  # Lưu trữ ảnh đã tải
    for i in range(1, num_pages+1):
        url = base_url.format(doc, i, subfolder)
        img = download(url, i)
        if img:
            images.append(img)

    if images:
        toPDF(image_list=images, pdf_filename="DS102.pdf")              
        for img in images:
            os.remove(img)     # Xoá ảnh đã tải sau khi ghép PDF lại xong

        print("Đã tải PDF thành công")
    else:
        print("Tải PDF không thành công")

main()
