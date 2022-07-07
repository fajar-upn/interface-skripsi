from fileinput import filename
from flask import Flask, render_template, request
from keras.backend import reshape
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
from keras.models import load_model
import numpy as np
import os
import base64

# from API import API_KEY
import requests
# import time

app = Flask(__name__)

dic = {0: "Iris Versicolor", 1: "Iris Virginica"}
model = load_model(
    './model/model_no6_dataset-tranparent-500_max-pool-8_epoch-50_v-1.h5')

# prepare image to prediction
def predict_label(img_path):
    i = image.load_img(img_path, target_size=(150,150))
    i = image.img_to_array(i)
    i = np.expand_dims(i, axis=0)
    i = np.vstack([i])
    # i = i.reshape(1, 150,150,3)
    # , batch_size=32
    classes = model.predict(i, batch_size=32)

    if classes==0:
        return 'Iris Versicolor'
    else:
        return 'Iris Virginica'
    print(classes)
    # return p[0][0]   

@app.route("/", methods=['GET', 'POST'])
def main_page():
    return render_template("index_js.html")

@app.route("/about", methods=['GET'])
def about_page():
    return "About page"

def remove_bg(img):
    response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open(img, 'rb')},
    # data={'size': 'auto', "bg_color":bg_color},
    data={'size': 'auto'},
    headers={'X-Api-Key': '<YOUR API KEY>'},
    )

    if response.status_code == requests.codes.ok:
        output = img
        with open(output, 'wb') as out:
            out.write(response.content)
            # print("Check in : "+out)
    else:
        print("Error :", response.text)

# 
ALLOWED_EXTENSION = set(['png', 'jpg', 'jpeg'])

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route('/predict', methods=['GET','POST'])
def predict_page():

    # if request.method == 'POST':
    
    img = request.files['imagefile']

    image_path = "static/" + img.filename
    
    # if not allowed_file(image_path):
    #     return render_template('not_allowed.html')
    img.save(image_path)
    # remove_bg(image_path)
    
    predict = predict_label(image_path)
    #  img_path=image_path, 'file':image_path,
    return { 'prediction':predict }
    # return render_template("index_js.html", prediction=predict, img_path=image_path, file=image_path)

if __name__ == '__main__':
    app.run(debug=True)