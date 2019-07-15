import fitsio
from . import files

def read_candidates():
    fname = files.get_cand_file()
    print('loading candidate list:', fname)
    return fitsio.read(fname)
