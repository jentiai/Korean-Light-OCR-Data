import json
import base64
import requests
import sys
import json

import os


def naver_ocr(image_path, api_url, api_key):
    image_name = image_path.split("/")[-1]
    image_base = image_name.split(".jpg")[0]

    with open(image_path, "rb") as f:
        img = base64.b64encode(f.read())

    URL = api_url
    KEY = api_key

    headers = {
        "Content-Type": "application/json",
        "X-OCR-SECRET": KEY
    }

    data = {
        "version": "V1",
        "requestId": str(image_base),
        "timestamp": 0,
        "images": [
            {"name": str(image_name), "format": "png", "data": img.decode("utf-8")}
        ],
    }
    data = json.dumps(data)
    response = requests.post(URL, data=data, headers=headers)
    res = json.loads(response.text)

    return res


def main():
    if len(sys.argv) != 4:
        print(
            "Please run with args: $ python example.py /path/to/image api_url api_key"
        )
    image_path, api_url, api_key = sys.argv[1], sys.argv[2], sys.argv[3]
    image_name = (image_path.split("/")[-1]).split(".jpg")[0]

    json_dict = dict()
    for (path, dir, files) in os.walk(image_path):
        files = list(files)

        for file in files:
            output = naver_ocr(os.path.join(path, file), api_url, api_key)
            json_dict[file.split(".jpg")[0]] = output

    with open("./naver.json", "w", encoding="UTF8") as result:
        result.write(json.dumps(json_dict, indent="\t", ensure_ascii=False))


if __name__ == "__main__":
    main()
