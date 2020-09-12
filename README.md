# Bandscore detections API

## local deploy
- docker-compose up --build

## Endpoint
- ### https://shrouded-dawn-55606.herokuapp.com/api

## Params
- ### request.files["file"] (file type is pdf.)
    - {"file": PDF file}
    - ファイルのアップロードプロセス処理
    - https://developer.mozilla.org/ja/docs/Web/API/File/Using_files_from_web_applications

## Response
- ### success
    - ### detection pass
        - {"img":['base64',...,'base64], "msg": "success"}
    - ### Not found any detection 
        - {"img":[], "msg": "Not found"}
- ### fail
    - {"img":[], "msg": "error"}

## How to use Response data
```
var resp = {"img":['base64',...,'base64], "msg": "success"}

<img src="data:image/png;base64,{{resp['img'][0]}}"/>
```

## sample application
- ### https://shrouded-dawn-55606.herokuapp.com/