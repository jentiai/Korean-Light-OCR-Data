import os
import sys
import json
import requests
from tqdm import tqdm

def main():
    url = "http://27.255.77.102:5000/evaluation"
    img_dir = sys.argv[1]

    with open('./jenti.json', 'w', encoding = 'UTF-8-sig') as json_res:
        res_dict = {}
        for img_name in tqdm(list(filter(lambda x: x.find('.jpg') != -1 or x.find('.png') != -1, os.listdir(img_dir)))):
            img_path = os.path.join(img_dir, img_name)
            files = {'file': open(img_path, 'rb').read()}
            r = requests.post(url, files = files)
            res_dict[os.path.splitext(img_name)[0]] = r.json()
        
        json.dump(res_dict, json_res, ensure_ascii = False, indent = '\t')

if __name__ == '__main__':
    main()    