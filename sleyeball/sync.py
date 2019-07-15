import os
import subprocess
from . import files
from .flist import get_flist


class FileSyncer(object):
    """
    sync files
    """

    def __init__(self, tilename, clean=True):
        self.tilename = tilename
        self._clean = clean

        self._y3_flist = get_flist('y3a1_coadd')
        self._y6_flist = get_flist('y6a1_coadd')

    def get_remote_cat_file(self):
        """
        local location of coadd fits file
        """
        return os.path.join(
            os.path.expandvars('$DESREMOTE_RSYNC'),
            self._get_cat_relpath(),
        )

    def get_cat_file(self):
        """
        local location of coadd fits file
        """
        return os.path.join(
            files.get_temp_dir(),
            os.path.basename(self._get_cat_relpath()),
        )

    def _get_cat_relpath(self):
        """
        get local location for coadd file
        """
        key = '%s-%s' % (self.tilename, 'r')
        return self._y3_flist[key]['path']

    def sync(self):
        """
        sync the coadd images
        """
        odir = files.get_temp_dir()

        remote_url = self.get_remote_cat_file()

        cmd = r"""
    rsync                                   \
        -aP                                 \
        --password-file $DES_RSYNC_PASSFILE \
        %(remote_url)s \
        %(local_dir)s/
        """ % dict(
            remote_url=remote_url,
            local_dir=odir,
        )

        print(cmd)
        subprocess.check_call(cmd, shell=True)

    def clean(self):
        """
        clean up the source files
        """
        cat_file = self.get_cat_file()
        if os.path.exists(cat_file):
            print('removing catalog:', cat_file)
            os.remove(cat_file)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self._clean:
            self.clean()
