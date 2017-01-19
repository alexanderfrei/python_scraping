from PIL import Image, ImageFilter

kitten = Image.open("page.jpg")
blurryKitten = kitten.filter(ImageFilter.GaussianBlur)
blurryKitten.save("page_blurred.jpg")
blurryKitten.show()