import matplotlib.pyplot as plt
from im2vid import create_video


def render_fn(fname_and_data):
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
    Data = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    create_video(
        video_fname="test.mp4",
        framerate=1,
        per_frame_rendering_fn=render_fn,
        Data=Data,
    )


if __name__ == "__main__":
    run()
