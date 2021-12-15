import os


def remove_labels_no_image(image_files, label_path):
    image_list = list(image_files.keys())

    for (path, dir, files) in os.walk(label_path):
        files = list(files)
        for file in files:
            if file.replace(".txt", ".jpg") not in image_list:
                os.remove(os.path.join(path, file))


def remove_no_gt(parent_dir):
    deleted_gt = []

    for path, dir, files in os.walk(parent_dir):
        if not files:
            continue

        for name in files:
            gt_path = os.path.join(path, name)

            # remove duplicated name
            if (
                name == "00C6DD18C320D0A8E8E26AFA84AB5555.txt"
                or name == "00F3E524ED9EC2FFD20BC6156EDF5BE3.txt"
            ):
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
