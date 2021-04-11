import os
import glob
import shlex, subprocess


def run_command(command):
    print('running command: {0}'.format(command))
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        print(output.strip())
        if output == b'' and process.poll() is not None:
            print('Done running the command.')
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc


cameraVoip_filepaths = []
for filepaths in sorted(glob.glob(os.path.join(output_folder, 'cameraVoip_*.flv'))):
    cameraVoip_filepaths.append(filepaths)
print('cameraVoip_filepaths: {0}'.format(cameraVoip_filepaths))

screenshare_filepaths = []
for filepaths in sorted(glob.glob(os.path.join(output_folder, 'screenshare_*.flv'))):
    screenshare_filepaths.append(filepaths)

part = 0
output_filepaths = []
for cameraVoip_filepath, screenshare_filepath in zip(cameraVoip_filepaths, screenshare_filepaths):
    output_filepath = os.path.join(
        main_output_folder, '{0}_{1:04d}.flv'.format(video_filename, part))
    #output_filepath = '{0}_{1:04d}.flv'.format(video_filename, part)
    output_filepaths.append(output_filepath)
    # ffmpeg command from Oliver Wang / Yannick Hold-Geoffroy / Aaron Hertzmann
    conversion_command = 'ffmpeg -i "%s" -i "%s" -c copy -map 0:a:0 -map 1:v:0 -shortest -y "%s"' % (
        cameraVoip_filepath, screenshare_filepath, output_filepath)
    # -y: override output file if exists
    run_command(conversion_command)
    part += 1

# Concatenate all videos into one single video
# https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg
video_list_filename = 'video_list.txt'
video_list_file = open(video_list_filename, 'w')
for output_filepath in output_filepaths:
    video_list_file.write("file '{0}'\n".format(output_filepath))
video_list_file.close()
final_output_filepath = '{0}.flv'.format(video_filename)
# ffmpeg command from Oliver Wang / Yannick Hold-Geoffroy / Aaron Hertzmann
conversion_command = 'ffmpeg -safe 0 -y -f concat -i "{1}" -c copy "{0}"'.format(
    final_output_filepath, video_list_filename)
run_command(conversion_command)
# os.remove(video_list_filename)
