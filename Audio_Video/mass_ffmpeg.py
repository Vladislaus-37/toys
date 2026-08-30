import sys
import os
import subprocess

args = list(sys.argv)[1:]

if "--help" in args:
    print("python3 mass_ffmpeg.py [FFMPEG_PATH] [INPUT_DIR] [OUTPUT_DIR] [FILE_EXTENTION] [FFMPEG_OPTIONS]")
    print("-----------------------------------------------------------------------------------------------")
    print("Script for mass recursive file processing with ffmpeg")
    print("Notes:")
    print("- Don't use shortened directory paths")
    print("- The output directory is created automatically")
    print("- Other files don't copy from input directory to out directory")


FFMPEG_PATH = args[0]
INPUT_DIR = args[1].replace("\\", "/")
if INPUT_DIR[-1] == "/":
    INPUT_DIR = INPUT_DIR[:-1]
OUTPUT_DIR = args[2].replace("\\", "/")
if OUTPUT_DIR[-1] == "/":
    OUTPUT_DIR = OUTPUT_DIR[:-1]
FILE_EXT = args[3]
OPTIONS = args[4]

# Running ffmpeg

def ffmpeg_use(path):
    try:
        print(f"The file {INPUT_DIR+"/"+path} is begin processed")
        subprocess.run([FFMPEG_PATH, 
                        "-i", (INPUT_DIR+"\\"+path).replace("/", "\\"),
                        (OUTPUT_DIR+"\\"+path).replace("/", "\\")]+
                        OPTIONS.split())
        print(f"Done")
        return 0
    except Exception as e:
        print(f"Error : {e}")
        return 1

# Recursive file scanning

def scan_files(path):
    list_dir = os.listdir(path)
    dirs = []
    wavs = []
    for i in list_dir:
        if os.path.isdir(path+"/"+i) == True:
            dirs.append(path+"/"+i)
        elif i[-4:] == f".{FILE_EXT}":
            wavs.append(path+"/"+i)
    new_wavs = []
    if dirs != []:
        for i in dirs:
            a = scan_files(i)
            new_wavs += a
    return new_wavs+wavs

# Creating a directory copy for new files

def make_dirs(wavs):
    dirs = set()
    for i in wavs:
        dirs.add(i[len(INPUT_DIR):i.rfind("/")])
    dirs = list(dirs)
    for i in dirs:
        os.mkdir(OUTPUT_DIR+i)

# Main method

def main():
    print("mass_ffmpeg 1.0")
    scan = scan_files(INPUT_DIR)
    print(f"Finded files: {scan}")
    print("Creating Output Directories While Preserving the Hierarchy")
    make_dirs(scan)
    print("Done")
    obfs_paths = []
    for i in scan:
        obfs_paths.append(i[len(INPUT_DIR):])
    print("Starting file processing in ffmpeg")
    for i in obfs_paths:
        ffmpeg_use(i)

if __name__ == "__main__":
    main()

# Copyleft Vladislaus Parusov https://github.com/Vladislaus-37/toys/ 
