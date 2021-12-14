import os
import shutil
import argparse

def make_test_image(image_path, test_image_list_path, output):
    f = open(os.path.join(test_image_list_path, 'aihub_test_image_list.txt'), 'r', encoding='UTF8')

    test_image_list = []
    for line in f.readlines():
        test_image_list.append(line.strip())

    os.makedirs(os.path.join(output, 'aihub_test'))
    aihub_class = ['book', 'Goods', 'Singboard', 'Traffic_Sign']
    for acls in aihub_class:
        dir_name = os.path.join('aihub_test', acls)
        os.makedirs(os.path.join(output, dir_name))

    for (path, dir, files) in os.walk(image_path):
        files = list(files)
        
        for file in files:
            test_image_name = os.path.basename(path) + '/' + file
            if test_image_name in test_image_list:
                base_dir = os.path.join(output, 'aihub_test')
                shutil.copy(os.path.join(path, file), os.path.join(base_dir, test_image_name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--aihub', '-a', type=str, default = './', help='aihub images path')
    parser.add_argument('--list_path', '-l', type=str, default = './', help='aihub test image list txt file path')
    parser.add_argument('--output', '-o', type=str, default = './', help='output path')
    args = parser.parse_args()

    make_test_image(args.aihub, args.list_path, args.output)