# im2vid
This is a utility tool to render a set of images to video.

## install
```bash
pip install git+https://github.com/jutanke-sony/im2vid.git
```

## usage
Simple usage:
```python
from im2vid import images2video

image_dir = "/path/to/folder_with_images"
video_fname = "/path/to/out_video_fname.mp4"

images2video(
    image_dir=image_dir,
    video_fname=video_fname,
    framerate=25,
    fileext="png"
)
```

This tool can also be used for multi-processed rendering:
```python
import matplotlib.pyplot as plt
from im2vid import create_video


def render_fn(fname_and_data):
    # 'data' is the actual data from the List 'Data' while
    # 'fname' contains a path to a temporary file where the
    # image should be saved to.
    fname, data = fname_and_data

    # -- do any renderings you want here --
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.text(0, 0, data)
    ax.axis("off")

    # -- make sure to save the image to the given fname --
    plt.savefig(fname)

    plt.close("all")  # prevent memory leak


def run():
    # the video will be rendered in the order of the list
    Data = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    create_video(
        video_fname="test.mp4",
        framerate=1,
        per_frame_rendering_fn=render_fn,
        Data=Data,
    )


if __name__ == "__main__":
    run()

```
