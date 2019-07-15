import os
import numpy as np
from .candidates import read_candidates
from . import files


def make_batch():
    maker = BatchMaker()
    maker.go()


class BatchMaker(object):
    def __init__(self):
        cand = read_candidates()

        self.tilenames = np.unique(cand['tilename'])

    def go(self):

        for i, tilename in enumerate(self.tilenames):
            self._write(tilename)

    def _write(self, tilename):
        stamp_dir = files.get_stamp_dir(tilename)
        if not os.path.exists(stamp_dir):
            os.makedirs(stamp_dir)

        self._write_script(tilename)
        self._write_wq(tilename)

    def _write_script(self, tilename):

        d = files.get_script_dir()
        fname = files.get_script_file(tilename)
        if not os.path.exists(d):
            os.makedirs(d)

        text = 'sl-make-cutouts %s\n' % tilename
        print('writing:', fname)
        with open(fname, 'w') as fobj:
            fobj.write(text)

    def _write_wq(self, tilename):

        job_name = '%s-stamps' % tilename
        d = files.get_script_dir()
        script_fname = files.get_script_file(tilename)
        wq_fname = files.get_wq_file(tilename)
        if not os.path.exists(d):
            os.makedirs(d)

        text = """
command: |
    . ~/.bashrc
    source activate y5color
    bash %s

job_name: %s\n""" % (script_fname, job_name)

        print('writing:', wq_fname)
        with open(wq_fname, 'w') as fobj:
            fobj.write(text)
