import os
from flask import Flask,jsonify,request
import face_recognition
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

def generateUnqiueId(name):
    return "{}_{}".format(name,uuid.uuid4().hex)
def getName(name):
    name = name.split("_")
    del name[-1]
    exact_name = "".join(name)
    return exact_name

def saveUserPhoto(name,file):
    un_id = generateUnqiueId(name)
    filename = secure_filename(file.filename)
    path_file = 'images/' +  un_id+ "." +filename.split('.')[-1]
    file.save(path_file)

@app.route('/upload',methods=['POST'])
def upload():
    try:
        file = request.files['file']
        name = request.form.get('name')
        saveUserPhoto(name,file)
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

@app.route('/check',methods=['POST'])
def check():
    try:
        images = os.listdir('images')
        if images[0] == '.DS_Store':
            del images[0]
        print(images)
        file = request.files['file']
        # English:
        #   load your image which you are recognition
        # Urdu:
        #   es line mn wo image dyn jis ko ap recognize kerna chahty hn
        image_to_be_matched = face_recognition.load_image_file(file)
        

        # English:
        #   encoded the loaded image into a feature vector
        # Urdu:
        #   jo image ap ny recognition ky liy li h y line us ko encode krti h taky usy baad mn compare kia jay dosri images ky sath
        image_to_be_matched_encoded = face_recognition.face_encodings(
            image_to_be_matched)[0]


        # English:
        #   iterate over each image
        # Urdu:
        #   Es process mn hm folder mn tamam picure ky sath apni makhsoos krda picture ko recognize krain gay
        isMatched = False
        matched_img_url = []
        for image in images:
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
                if not isMatched:
                    saveUserPhoto(name,file)

                matched_img_url.append({
                    "name":name,
                    "url":image
                })
                isMatched = True
                print("Matched: " + image)
            else:
                print("Not matched: " + image)
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