from flask import Flask, request, jsonify, flash, redirect, render_template
from flask_cors import CORS
from detect.bbox import y_positions
from PIL import Image
import numpy as np
import os
import io 
import base64
import fitz

app = Flask(__name__)
CORS(app)

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

@app.route('/', methods=['GET', 'POST'])
def uploads_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      #ファイルがなかった場合
      flash("メッセージ")
      return redirect(request.url)
    
    images = fitz.open(stream=request.files['file'].read(),filetype='pdf')

    w=images[0].getPixmap().width
    byte = images[0].getPixmap().getImageData()
    img = Image.open(io.BytesIO(byte))

    # pos empty list / tuple list
    *pos, = y_positions(img,0.6)

    if pos == []:
      return jsonify({"img":[], "msg": "Not found"})

    data = [0]*len(pos)

    for i, image in enumerate(images):
      byte = image.getPixmap().getImageData()
      img = Image.open(io.BytesIO(byte))
      if i==0:
        for j, p in enumerate(pos):
          data[j] = img.crop((0, p[0], w, p[1]))
      else:
        for j, p in enumerate(pos):
          tmp = img.crop((0, p[0], w, p[1]))
          data[j]=get_concat_v(data[j], tmp)

    output = io.BytesIO()
    data[0].save(output, format='PNG')
    image_png = output.getvalue()
    buff = base64.b64encode(image_png).decode("UTF-8")

    return render_template("name.html", data=buff)

  return '<html><body><form method = post enctype = multipart/form-data><p><input type=file name = file><input type = submit value = Upload></form></body></html>'
  #return render_template("mainpage.html")

@app.route('/api', methods=['POST'])
def uploads_file_api():
  try :
    images = fitz.open(stream=request.files['file'].read(),filetype='pdf')

    w=images[0].getPixmap().width
    byte = images[0].getPixmap().getImageData()
    img = Image.open(io.BytesIO(byte))

    # pos empty list / tuple list
    *pos, = y_positions(img,0.6)

    if pos == []:
      return jsonify({"img":[], "msg": "Not found"})

    data = [0]*len(pos)

    for i, image in enumerate(images):
      byte = image.getPixmap().getImageData()
      img = Image.open(io.BytesIO(byte))
      if i==0:
        for j, p in enumerate(pos):
          data[j] = img.crop((0, p[0], w, p[1]))
      else:
        for j, p in enumerate(pos):
          tmp = img.crop((0, p[0], w, p[1]))
          data[j]=get_concat_v(data[j], tmp)

    buff = []
    for d in data:
      output = io.BytesIO()
      d.save(output, format='PNG')
      image_png = output.getvalue()
      buff.append(base64.b64encode(image_png).decode("UTF-8"))

    return jsonify({"img":buff, "msg": "success"})

  except :
    return jsonify({"img":[], "msg": "error"})

if __name__ == '__main__':
    app.run()