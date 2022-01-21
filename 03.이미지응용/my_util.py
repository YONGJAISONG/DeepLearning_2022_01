import urllib3, json, base64
from PIL import Image, ImageDraw, ImageFont
SUCCESS, FAILURE = 0, -1
RESPONSE_OK = 200

def detect_image(img_file, return_file):    # return_file은 file 이름
    with open('etriaikey.txt') as f:
        ai_key = f.read()

    openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
    http = urllib3.PoolManager()
    img_type = img_file.split('.')[-1]
    img_type = 'jpg' if img_type == 'jfif' else img_type
    with open(img_file, 'rb') as file:
        img_contents = base64.b64encode(file.read()).decode("utf8")

    request_json = {
        "access_key": ai_key,
        "argument": {
            "type": img_type,
            "file": img_contents
        }
    }
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(request_json)
    )
    if response.status != RESPONSE_OK:
        return FAILURE

    result = json.loads(response.data)
    obj_list = result['return_object']['data']
    img = Image.open(img_file)
    draw = ImageDraw.Draw(img)
    for obj in obj_list:
        name = obj['class']
        x = int(obj['x'])
        y = int(obj['y'])
        w = int(obj['width'])
        h = int(obj['height'])
        draw.rectangle(((x, y), (x+w, y+h)), outline = (255, 0, 0), width = 3)  # 두 지점을 튜플로 묶어야 한다
        draw.text((x+10, y+3), name, font = ImageFont.truetype('malgun.ttf', 25), fill = (255, 0, 0))

    img.save(return_file)
    return SUCCESS