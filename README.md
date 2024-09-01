# storyboard3-video
Example to create a much smaller video from YouTube storyboard3 thumbnails compared to downloading the entire video

## Setup

1. Install the latest Python 3.x
    - https://www.python.org/downloads/
    - On the installer be sure to check `Add Python to PATH`
2. Install required python packages
    - Use `requirements_pip_install.bat` as the quickest/easiest option
    - Alternatively, use command prompt, cd to the project, and run `pip install -r requirements.txt` manually

## Run

```sh
# Long video 34:15
$ py .\make_video.py MV6m-N4NFdA

# Short
$ py .\make_video.py gqAsw62OO_g
```

Script will create relative folders `out/{video_id}` containing folders of frames and generated `avi` videos using those frames.

- default
- 80x45
- 160x90
- 320x180