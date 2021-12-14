import os
import shutil
import time
import json
import copy
import argparse

from collections import defaultdict
from utils.rotate import check_word_include_char, generate_rbox
from utils.post_processor import remove_labels_no_image

DEFAULT_AIHUB_ANNOTATION_FILE = 'textinthewild_data_info.json'

class AihubTest:
    def __init__(self, aihub_path, test_list_path, output, margin=5):
        self.aihub_json = json.load(open(os.path.join(aihub_path, DEFAULT_AIHUB_ANNOTATION_FILE), 'r', encoding='UTF8'))
        self.test_list_file = open(os.path.join(test_list_path, 'aihub_test_image_list.txt'), 'r', encoding='UTF8')

        self.aihub_word_list, self.aihub_char_list, self.aihub_ignored_list = defaultdict(list), defaultdict(list), defaultdict(list)

        self.test_list = []
        for line in self.test_list_file.readlines():
            self.test_list.append((line.strip()).split('/')[-1])

        print('initialization...')
        for anno in self.aihub_json['annotations']:
            # self.aihub_test_dict[anno['image_id']].append(anno)
            if anno['attributes']['class'] == 'character':
                self.aihub_char_list[anno['image_id']].append(anno)
            elif anno['attributes']['class'] == 'word':
                self.aihub_word_list[anno['image_id']].append(anno)
            elif anno['attributes']['class'] == 'ignored':
                self.aihub_ignored_list[anno['image_id']].append(anno)

        print(f'make rotate annotations with margin {margin}...')
        for image in self.aihub_json['images']:
            self.add_rotated_boxes(image['id'], margin)

        print(f'copy aihub test images...')
        os.makedirs(os.path.join(output, 'aihub_test_image'))
        for (path, dir, files) in os.walk(aihub_path):
            files = list(files)
            
            for file in files:
                if file in self.test_list:
                    base_dir = os.path.join(output, 'aihub_test_image')
                    shutil.copy(os.path.join(path, file), os.path.join(base_dir, file))

    def add_rotated_boxes(self, img_id, margin):
        anno_words = self.aihub_word_list[img_id]
        anno_chars = self.aihub_char_list[img_id]

        for anno_word in anno_words:
            anno_chars_in_w = []
            for anno_char in anno_chars:
                if check_word_include_char(anno_word['bbox'], anno_char['bbox'], margin):
                    anno_chars_in_w.append(anno_char)
            if len(anno_chars_in_w)==0:
                x, y, w, h = anno_word['bbox']
                anno_rbox = copy.deepcopy(anno_word)

                poly = [x,y, x+w,y, x+w,y+h, x,y+h]
                anno_rbox["poly"] = poly
            else:
                anno_rbox = generate_rbox(anno_word, anno_chars_in_w)
            
            self.aihub_ignored_list[img_id].append(anno_rbox)

    def calc_wh(self, poly):
        min_x, max_x = min(poly[0::2]), max(poly[0::2])
        min_y, max_y = min(poly[1::2]), max(poly[1::2])
        width = max_x - min_x
        height = max_y - min_y

        if width == 0 or height == 0:
            return True
        else:
            return False

    def make_rotate_gt(self, image_id, file):
        for annot in self.aihub_ignored_list[image_id]:
            if annot['text'] is not None and annot['text'].strip() == "":
                continue

            if annot['attributes']['class'] == 'rbox' or annot['attributes']['class'] == 'word':
                poly = annot['poly']
            elif annot['attributes']['class'] == 'ignored':
                [bbox_x, bbox_y, bbox_w, bbox_h] = annot['bbox']
                poly = [bbox_x, bbox_y, bbox_x+bbox_w, bbox_y, bbox_x+bbox_w, bbox_y+bbox_h, bbox_x, bbox_y+bbox_h]

            if self.calc_wh(poly):
                continue

            for p in poly:
                file.write(str(int(p))+', ')

            if annot['text'] is None: # ignored
                file.write(str('###'))
            else:
                file.write(str(annot['text']))
            file.write('\n')


    def store_gt(self, gt_path):
        os.makedirs(os.path.join(gt_path, 'gt'), exist_ok=True)

        for image in self.aihub_json['images']:
            if image['file_name'] in self.test_list:
                rf = open(os.path.join(gt_path, 'gt/{}.txt'.format(image['file_name'].split('.jpg')[0])), 'w', encoding='UTF8')
                self.make_rotate_gt(image['id'], rf)
                rf.close()

def remove_no_gt(parent_dir):
    deleted_gt = []

    for path, dir, files in os.walk(parent_dir):
        if not files: continue

        for name in files:
            gt_path = os.path.join(path, name)

            # remove duplicated name
            if name == '00C6DD18C320D0A8E8E26AFA84AB5555.txt' or name == '00F3E524ED9EC2FFD20BC6156EDF5BE3.txt':
                deleted_gt.append(gt_path)
                os.remove(gt_path)
                continue

            # remove empty gt
            with open(gt_path, "r", encoding="utf-8") as f:
                lines = f.read()
            if not lines:
                deleted_gt.append(gt_path)
                os.remove(gt_path)

    return 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--aihub', '-a', type=str, default = './', help='aihub images path')
    parser.add_argument('--list_path', '-l', type=str, default = './', help='aihub test image list txt file path')
    parser.add_argument('--output', '-o', type=str, default = './', help='output path')
    args = parser.parse_args()

    margin = 5
    aihub_test = AihubTest(args.aihub, args.list_path, args.output, margin)

    print('make gt files...')
    aihub_test.store_gt(args.output)

    print('remove gt with no annotation')
    deleted_gt = remove_no_gt(os.path.join(args.output, 'gt'))