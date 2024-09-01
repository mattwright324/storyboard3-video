import sys, os, re, json, innertube, cv2
from io import BytesIO
from PIL import Image
from urllib.request import urlopen

print(sys.argv)

video_id = None
if match := re.search("[A-Za-z0-9_-]{10}[AEIMQUYcgkosw048]", sys.argv[1], re.NOFLAG):
    video_id = match.group(0)
if video_id is None:
    print("Input was not a valid video id [%s]")
    exit(1)

os.makedirs("out/%s" % video_id, exist_ok=True)

client = innertube.InnerTube("WEB")
data = client.player(video_id)

file = open("out/%s/player.json" % video_id, "w")
file.write(json.dumps(data, indent=2))
file.close()

def make_sb_urls(specUrl):
    data = [item.split("#") for item in specUrl.split("|")]
    output = {}
    for i in range(1, len(data)):
        frames = int(data[i][2])
        step = int(data[i][3]) * int(data[i][4])
        sigh = data[i][7].split("$")
        url = data[0][0].replace("$L", str(i - 1)).replace("$N", data[i][6]) + "&sigh=" + sigh[0] + "%24" + sigh[1]

        key = "default" if data[i][6] == "default" else "%sx%s" % (data[i][0], data[i][1])
        output[key] = {
            "urls": [url.replace("$M", str(j)) for j in range(frames // step)],
            "width": int(data[i][0]),
            "height": int(data[i][1]),
            "frames": frames,
            "gridWidth": int(data[i][3]),
            "gridHeight": int(data[i][4]),
            "frameMs": int(data[i][5]),
        }
    return output

durationSec = int(data["videoDetails"]["lengthSeconds"])
sbSpecUrl = data["storyboards"]["playerStoryboardSpecRenderer"]["spec"]
output = make_sb_urls(sbSpecUrl)

print(sbSpecUrl)
print()

for key, value in output.items():
    print(key)
    print(value)
    os.makedirs("out/%s/%s" % (video_id, key), exist_ok=True)

    framesPerUrl = value["gridWidth"] * value["gridHeight"]
    i = 0
    for url in value["urls"]:
        image = Image.open(BytesIO(urlopen(url).read()))
        for y in range(value["gridHeight"]):
            for x in range(value["gridWidth"]):
                w = value["width"]
                h = value["height"]
                tx = x * w
                ty = y * h
                tw = tx + w
                th = ty + h
                # print("%s,%s,%s,%s" % (tx, ty, tw, th))
                temp = image.crop((tx, ty, tw, th))
                temp.save("out/%s/%s/%s.jpg" % (video_id, key, (i * framesPerUrl) + ((y * value["gridHeight"]) + x)))
        i += 1


    image_folder = 'out/%s/%s' % (video_id, key)
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    fps = 1 / (durationSec / (len(images)-1)) if key == "default" else 1000 / value["frameMs"]
    video = cv2.VideoWriter("out/%s/%s.avi" % (video_id, key), 0, fps, (width, height))
    print("video=%s.avi videoLength=%s frames=%s fps=%s" % (key, durationSec, len(images), fps))

    for image in images:
        video.write(cv2.imread(os.path.join("out/%s/%s" % (video_id, key), image)))
    cv2.destroyAllWindows()
    video.release()
    print()

print()
