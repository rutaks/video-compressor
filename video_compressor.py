import subprocess
import os
import time
import logging
import sys
from shutil import copyfile
from pathlib import Path

master_start_time = time.time()

# handbrake_cli_path = r"r"C:\Users\rutaks\Downloads\HandBrakeCLI-1.3.3-win-x86_64\HandBrakeCLI.exe"" # WINDOWS
handbrake_cli_path = r"/Volumes/HandBrakeCLI-1.5.1/HandBrakeCLI" # MAC, MAKE SURE CLI IS MOUNTED
root_video_directory = Path(r'/Users/apple/Downloads/compression_attempt')
root_video_output = Path(r'/Users/apple/Downloads/compression_attempt/output')
file_type = sys.argv[0] or 'mts'

# noinspection PyArgumentList
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[
                        logging.FileHandler(r"D:\export_log.log"),
                        logging.StreamHandler(sys.stdout)
                    ]
                    )

for path, directories, files in os.walk(root_video_directory):

    new_folder = root_video_output.joinpath(*Path(path).parts[1:])
    logging.info(f"Creating folder for {new_folder}")
    Path(new_folder).mkdir(parents=True, exist_ok=True)

    for file in files:
        video_file = os.path.join(path, file)
        logging.info(f"Detected .{file_type} file: {video_file}")
        output_file = str(root_video_output.joinpath(*Path(video_file).parts[1:])).replace(".avi", ".mp4")

        if Path(output_file).exists():
            logging.info("deteced mp4 already converted")
            continue
        else:

            handbrake_command = [handbrake_cli_path, '-i', f'{video_file}',"-o", output_file, "-e", "x264", "-q", "20", "-B", "260", "-Z", "Fast 1080p30"]
            logging.info(f"Converting: {video_file} to .MP4 with x264. Output MP4: {output_file}")
            start_time = time.time()

            process = subprocess.Popen(handbrake_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                print(line)

            logging.info("Done")
            logging.info('Program took {} seconds to complete..\n'.format(time.time() - start_time))

logging.info("Done")
logging.info('Program took {} seconds to complete.'.format(time.time() - master_start_time))