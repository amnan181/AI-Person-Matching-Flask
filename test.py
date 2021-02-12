from deepface import DeepFace
# result  = DeepFace.verify("waqas.jpg", "Waqas sabir.jpg")
#results = DeepFace.verify([['img1.jpg', 'img2.jpg'], ['img1.jpg', 'img3.jpg']])

df = DeepFace.find(img_path = "waqas.jpg", db_path = "images")


print("=========>", df)
print("=========>", type(df))
print("=========>", df['identity'].values.tolist()[0])

