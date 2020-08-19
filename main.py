from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
from werkzeug import secure_filename
import os
from pdf2image import convert_from_path
from pathlib import Path
from PIL import Image
import numpy as np
import io 
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def uploads_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      #ファイルがなかった場合
      flash("メッセージ")
      return redirect(request.url)
    
    file = request.files['file']
    filename = secure_filename(file.filename)

    if filename == '':
      #ファイル名がなかった場合
      flash("メッセージ")
      return redirect(request.url)

    #ファイルを保存
    file.save('./uploads/'+ filename)

    # poppler/binを環境変数PATHに追加する
    poppler_dir = Path(__file__).parent.absolute() / "poppler/bin"
    os.environ["PATH"] += os.pathsep + str(poppler_dir)

    # PDF -> Image に変換（250dpi）
    images = convert_from_path('./uploads/'+ filename, 250)
    os.remove('./uploads/'+ filename)
    
    #画像を結合する関数
    def get_concat_v(im1, im2):
      dst = Image.new('RGB', (im1.width, im1.height + im2.height))
      dst.paste(im1, (0, 0))
      dst.paste(im2, (0, im1.height))
      return dst

    width=images[0].width #横幅を取得

    #各パートでループする?
    index=0

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
    data=base64.b64encode(image_png)
    print(data)
    
    return redirect(url_for('uploaded_file', filename=filename))

  return '<html><body><form method = post enctype = multipart/form-data><p><input type=file name = file><input type = submit value = Upload></form></body></html>'
  #return render_template("mainpage.html")



@app.route('/uploads/<filename>')
def uploaded_file(filename):

  return '<html><body>あああ</body></html>'
  #return render_template("name.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000)