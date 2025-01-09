import tempfile
import moviepy.video.io.ImageSequenceClip

from os import listdir
from os.path import join
from multiprocessing.pool import Pool, ThreadPool
from typing import List
from tqdm import tqdm


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

        if use_threading:
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
