import numpy as np
import fitsio
from . import files


def read_candidates(orig=False):
    if orig:
        fname = files.get_cand_file_orig()
    else:
        fname = files.get_cand_file()

    return fitsio.read(fname)


def clean_candidates():
    import healpy as hp

    fname_orig = files.get_cand_file_orig()
    fname_clean = files.get_cand_file()
    assert fname_orig != fname_clean

    badreg_fname = files.get_badreg_file()

    print('loading original candidate list:', fname_orig)

    cand = fitsio.read(fname_orig)

    print('reading bad regions mask')
    badreg = hp.read_map(badreg_fname)
    pixids = hp.ang2pix(4096, cand['ra'], cand['dec'], lonlat=True)

    pixvals = badreg[pixids]

    good, = np.where(pixvals == 0)

    print('writing cleaned candidates', fname_clean)
    fitsio.write(fname_clean, cand[good], clobber=True)
