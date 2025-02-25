import tempfile
import moviepy.video.io.ImageSequenceClip

from os import listdir
from os.path import join
from multiprocessing.pool import Pool, ThreadPool
from typing import List
from tqdm import tqdm
import numpy as np
import matplotlib.pylab as plt


def save_image_to_file_fn(fname_and_data):
    fname, data = fname_and_data
    img = data["img"]
    plt.imsave(fname, img)


def create_video_from_images(
    video_fname: str,
    framerate: int,
    images: np.ndarray,
    *,
    n_workers: int = 15,
    fileext: str = "png",
    use_tqdm: bool = True,
    use_threading: bool = False,
):
    """
    :param video_fname: filename of the video to be created
    :param framerate: framerate of the video
    :param images: images to be converted to a video {t x h x w x 3}
    """
    assert video_fname.endswith(".mp4"), "video_fname must end with '.mp4'"
    assert len(images) > 0, "images must not be empty"
    assert (
        len(images.shape) == 4 and images.shape[3] == 3
    ), f"images must have shape [t x h x w x 3] but has {images.shape}"

    Data = []
    for img in images:
        Data.append({"img": img})
    create_video(
        video_fname=video_fname,
        framerate=framerate,
        per_frame_rendering_fn=save_image_to_file_fn,
        Data=Data,
        n_workers=n_workers,
        fileext=fileext,
        use_tqdm=use_tqdm,
        use_threading=use_threading,
    )


def create_video(
    video_fname: str,
    framerate: int,
    per_frame_rendering_fn,
    Data: List,
    *,
    n_workers: int = 15,
    fileext: str = "png",
    use_tqdm: bool = True,
    use_threading: bool = False,
):
    assert video_fname.endswith(".mp4"), "video_fname must end with '.mp4'"
    assert len(Data) > 0, "Data must not be empty"
    assert len(Data) < 99999999, f"Data must not be too large (#Data={len(Data)})"
    assert "." not in fileext, f"fileext '{fileext}' must not contain '.'"
    n_workers = min(n_workers, len(Data))
    if n_workers == 0 or n_workers == 1:
        use_threading = True

    with tempfile.TemporaryDirectory() as tmpdirname:
        Data_augm = []
        for i, data in enumerate(Data):
            img_fname = join(tmpdirname, f"{i:09d}.{fileext}")
            Data_augm.append((img_fname, data))

        if n_workers == 0:
            for fname_and_data in tqdm(Data_augm, disable=not use_tqdm):
                per_frame_rendering_fn(fname_and_data)
        elif use_threading:
            with ThreadPool(n_workers) as p:
                _ = list(
                    tqdm(
                        p.imap(per_frame_rendering_fn, Data_augm),
                        total=len(Data),
                        disable=not use_tqdm,
                    )
                )
        else:
            with Pool(n_workers) as p:
                _ = list(
                    tqdm(
                        p.imap(per_frame_rendering_fn, Data_augm),
                        total=len(Data),
                        disable=not use_tqdm,
                    )
                )
        images2video(
            image_dir=tmpdirname,
            video_fname=video_fname,
            framerate=framerate,
            fileext=fileext,
        )


def images2video(
    image_dir: str, video_fname: str, framerate: int, *, fileext: str = "png"
):
    image_files = [
        join(image_dir, f)
        for f in sorted(listdir(image_dir))
        if f.endswith(f".{fileext}")
    ]
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(
        image_files, fps=framerate
    )
    clip.write_videofile(video_fname)
