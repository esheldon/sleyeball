import os


def get_base_dir():
    """
    base directory
    """
    return os.environ['SLDIR']


def get_cand_dir():
    """
    we keep lists here
    """
    return os.path.join(get_base_dir(), 'candidates')


def get_cand_file_orig():
    """
    holds paths to coadds
    """
    d = get_cand_dir()
    return os.path.join(d, 'z4ErinSheldon.fits')


def get_cand_file():
    """
    holds paths to coadds
    """
    d = get_cand_dir()
    return os.path.join(d, 'z4ErinSheldon-clean.fits')


def get_badreg_dir():
    """
    we keep lists here
    """
    return os.path.join(get_base_dir(), 'badregions')


def get_badreg_file():
    """
    holds paths to coadds
    """
    d = get_badreg_dir()
    return os.path.join(d, 'y3a2_foreground_mask_v2.1.fits.gz')


def get_stamp_dir(tilename):
    """
    location for the image and temp files
    """

    return os.path.join(
        get_base_dir(),
        'stamps',
        tilename,
    )


def get_temp_dir():
    """
    location for the image and temp files
    """
    return os.environ['TMPDIR']


def get_stamp_file(tilename, number):
    """
    location of a output file
    """

    odir = get_stamp_dir(tilename)

    fname = '%s-%06d.jpg' % (tilename, number)
    return os.path.join(odir, fname)


#
# batch processing
#


def get_script_dir():
    """
    location for scripts
    """
    return os.path.join(get_base_dir(), 'scripts')


def get_script_file(tilename):
    """
    location for scripts
    """

    d = get_script_dir()
    fname = '%s.sh' % tilename
    return os.path.join(d, fname)


def get_wq_file(tilename, missing=False):
    """
    location for scripts
    """

    fname = '%s.yaml' % tilename

    d = get_script_dir()
    return os.path.join(d, fname)
