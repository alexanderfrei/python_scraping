from PIL import Image, ImageFilter

WaP = Image.open("page.jpg")
blurry_WaP = WaP.filter(ImageFilter.GaussianBlur)
blurry_WaP.save("page_blurred.jpg")
blurry_WaP.show()
