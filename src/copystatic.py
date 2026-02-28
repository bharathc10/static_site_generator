import os
import shutil

def copystatic(src, dst):
    src_dir = os.path.abspath(src)
    dst_dir = os.path.abspath(dst)
    
    for file in os.listdir(src_dir):
        if file.startswith('.'):
            continue
        src_path = os.path.join(src_dir, file)
        dst_path = os.path.join(dst_dir, file)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)
            copystatic(src_path, dst_path)