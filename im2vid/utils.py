import numpy as np
from einops import rearrange


def get_lims_from_3d(pts3d):
    """
    :param pts3d: 3D points [... x 3]
    """
    pts3d = rearrange(pts3d, "... d -> (...) d")
    xmin, xmax = np.min(pts3d[..., 0]), np.max(pts3d[..., 0])
    ymin, ymax = np.min(pts3d[..., 1]), np.max(pts3d[..., 1])
    zmin, zmax = np.min(pts3d[..., 2]), np.max(pts3d[..., 2])

    xlen = xmax - xmin
    ylen = ymax - ymin
    zlen = zmax - zmin

    maxlen = max(xlen, ylen, zlen)

    xlim = [
        ((xmax + xmin) / 2 - maxlen / 2).item(),
        ((xmax + xmin) / 2 + maxlen / 2).item(),
    ]
    ylim = [
        ((ymax + ymin) / 2 - maxlen / 2).item(),
        ((ymax + ymin) / 2 + maxlen / 2).item(),
    ]
    zlim = [
        ((zmax + zmin) / 2 - maxlen / 2).item(),
        ((zmax + zmin) / 2 + maxlen / 2).item(),
    ]
    return xlim, ylim, zlim


def set_xlim(ax, pts3d):
    xlim, ylim, zlim = get_lims_from_3d(pts3d=pts3d)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)
    return ax
