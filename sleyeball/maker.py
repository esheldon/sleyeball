import numpy as np
from PIL import Image
import fitsio
import esutil as eu
from .sync import FileSyncer
from .candidates import read_candidates
from .flist import get_flist
from . import files


def make_stamps(tilename, resize_factor=4, stamp_size=96):

    y3_flist = get_flist('y3a1_coadd')
    y6_flist = get_flist('y6a1_coadd')

    key = '%s-r' % tilename
    if key in y6_flist:
        image_path = y6_flist[key]['image_path']
    else:
        image_path = y3_flist[key]['image_path']

    im = load_image(image_path)
    nx, ny = im.size

    stamp_half_size = stamp_size//2

    cand = read_candidates()
    w, = np.where(cand['tilename'] == tilename)
    print('found %d/%d in %s' % (w.size, cand.size, tilename))

    with FileSyncer(tilename, clean=True) as syncer:
        syncer.sync()

        catname = syncer.get_cat_file()

        print('reading:', catname)
        cat = fitsio.read(catname, lower=True)

        mcat, mcand = eu.numpy_util.match(
            cat['number'],
            cand['number'][w],
        )
        assert w.size == mcand.size

        for i in range(w.size):
            icand = w[mcand[i]]
            icat = mcat[i]

            oxmin = cat['x_image'][icat] - stamp_half_size - 1
            oxmax = cat['x_image'][icat] + stamp_half_size - 1
            oymin = cat['y_image'][icat] - stamp_half_size - 1
            oymax = cat['y_image'][icat] + stamp_half_size - 1

            # we flipped rows, so y -> (ny-1)-y

            xmin = oxmin
            xmax = oxmax
            ymin = ny - 1 - oymax
            ymax = ny - 1 - oymin
            bounds = (xmin, ymin, xmax, ymax)

            cim = make_stamp(im, bounds)

            eim = expand_stamp(cim, resize_factor)

            enx, eny = eim.size

            number = cat['number'][icat]
            jpgname = files.get_stamp_file(tilename, number)

            print('writing %d/%d  %s (%d, %d)' % \
                (i+1, w.size, jpgname, enx, eny))
            write_stamp(eim, jpgname)


def make_stamp(im, bounds):
    cim = im.crop(bounds)
    return cim


def expand_stamp(im, factor):
    factor = int(factor)
    assert factor >= 1,  'factor %d < 1' % factor

    nx, ny = im.size

    new_nx, new_ny = factor*nx, factor*ny
    return im.resize( (new_nx, new_ny) )


def write_stamp(im, fname):
    im.save(fname, quality=90)


def load_image(fname):
    print('opening image:', fname)
    return Image.open(fname)
