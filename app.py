import os
from flask import Flask,jsonify,request
import face_recognition
import uuid
from werkzeug.utils import secure_filename
import shutil
from db import db
app = Flask(__name__)


Imagegallary = db["Imagegallary"]

def saveImageGalleryToDB(data):
    Imagegallary.insert_one(data)


class TestFailed(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

def generateUnqiueId(name):
    return "{}_{}".format(name,uuid.uuid4().hex)
def getName(name):
    name = name.split("_")
    del name[-1]
    exact_name = "".join(name)
    return exact_name

def saveUserPhoto(name,file,location):
    un_id = generateUnqiueId(name)
    filename = secure_filename(file.filename)
    path_file = 'images/' +  un_id+ "." +filename.split('.')[-1]
    saveImageGalleryToDB({
                "file":path_file,
                "name":name,
                "location":location
            })
    file.save(path_file)

def applyAI(path_file):

    images_ = os.listdir('images')
    images = []
    for i in images_:
        if not i == '.DS_Store':
            images.append(i)
     
        # English:
        #   load your image which you are recognition
        # Urdu:
        #   es line mn wo image dyn jis ko ap recognize kerna chahty hn
    image_to_be_matched = face_recognition.load_image_file(path_file)
        
        

        # English:
        #   encoded the loaded image into a feature vector
        # Urdu:
        #   jo image ap ny recognition ky liy li h y line us ko encode krti h taky usy baad mn compare kia jay dosri images ky sath
    image_to_be_matched_encoded = face_recognition.face_encodings(
            image_to_be_matched)
    if not len(image_to_be_matched_encoded):
        raise TestFailed("We cann't found face in this picture please check your image and make sure image is not rotated!")
    
    image_to_be_matched_encoded = image_to_be_matched_encoded[0]
        # English:
        #   iterate over each image
        # Urdu:
        #   Es process mn hm folder mn tamam picure ky sath apni makhsoos krda picture ko recognize krain gay
    isMatched = False
    matched_img_url = []
    for image in images:
        try:
                
                # English:
                #   load the image
                # Urdu:
                #   y hamary folder sy tamam image bari bari load kry ga
            current_image = face_recognition.load_image_file("images/" + image)
                # |----------------SAME----------------|
                # encode the loaded image into a feature vector
            current_image_encoded = face_recognition.face_encodings(current_image)[0]
                # English:
                #   match your image with the image and check if it matches
                # Urdu:
                #   Y hamari makhsoos image ko hamry folder ki tamam image ky sath bari bari compare kry ga
            result = face_recognition.compare_faces(
                    [image_to_be_matched_encoded], current_image_encoded)
                # English:
                #   check if it was a match
                # Urdu:
                #   yaha hm apna result check krain gay
            
            if result[0] == True:
                name = getName(image)
                    

                matched_img_url.append({
                        "name":name,
                        "url":image
                    })
                isMatched = True
                print("Matched: " + image)
            else:
                print("Not matched: " + image)
        except Exception as e:
            print("error is comming========>",e)
            pass
            
    return isMatched,matched_img_url
    

@app.route('/upload',methods=['POST'])
def upload():
    try:
        file = request.files['file']
        name = request.form.get('name')
        location = request.form.get('location',"")
        saveUserPhoto(name,file,location)
        # un_id = generateUnqiueId(name)
        # path_file = 'images/' + un_id
        # file.save(path_file)
        
        return jsonify({
            "success":True,
        })
    except Exception as e:
        return jsonify({
            "message":str(e),
            "success":False,
        })

@app.route('/gallery')
def getImagegallary():
    cursor = Imagegallary.find({})
    data = []
    for user in cursor:
        user['_id'] = str(user['_id'])
        data.append(user)
    
    return jsonify({
        "data":data
    })


@app.route('/check',methods=['POST'])
def check():
    try:
        file = request.files['file']
        un_id = generateUnqiueId("unknown")
        location = request.form.get('location',"")

        ext = secure_filename(file.filename).split('.')[-1]
        path_file =  un_id+ "." +ext
        file.save(path_file)

        isMatched,matched_img_url = applyAI(path_file)

        if isMatched:
            name = getName(matched_img_url[0]["url"])
            un_id = generateUnqiueId(name)
            destination = "images/" + un_id+ "." +ext
            saveImageGalleryToDB({
                "file":destination,
                "name":name,
                "location":location
            })
            shutil.move(path_file, destination)

        return jsonify({
            "success":True,
            "isMatched":isMatched,
            "matchedUrl":matched_img_url
        })
    except Exception as e:
        return jsonify({
            "message":str(e),
            "success":False,
            "isMatched":None,
            "matchedUrl":None
        })
if __name__ == '__main__':
    
    app.run(host='0.0.0.0', debug=True, port=5000)