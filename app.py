from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
from flask_cors import CORS
import os
from pdf2image import convert_from_bytes
from pathlib import Path
from PIL import Image
import numpy as np
import io 
import base64

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

    # poppler/binを環境変数PATHに追加する
    poppler_dir = Path(__file__).parent.absolute() / "poppler/bin"
    os.environ["PATH"] += os.pathsep + str(poppler_dir)

    images = convert_from_bytes(request.files['file'].read())

    width=images[0].width #横幅を取得

    for i, image in enumerate(images):
      if i==0:
        im1=image.crop((0, 75, width, 250))
      else:
        im2 = image.crop((0, 75, width, 250))
        im1=get_concat_v(im1, im2)

    #バイナリーに変換
    output = io.BytesIO()
    im1.save(output, format='PNG')
    image_png = output.getvalue()
    #base64に変換
    data = base64.b64encode(image_png)
    
    return redirect(url_for('uploaded_file'))

  return '<html><body><form method = post enctype = multipart/form-data><p><input type=file name = file><input type = submit value = Upload></form></body></html>'
  #return render_template("mainpage.html")



@app.route('/uploaded/')
def uploaded_file():

  return '<html><body>あああ</body></html>'
  #return render_template("name.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
