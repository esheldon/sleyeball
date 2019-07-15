import fitsio
import desimage


def get_flist(campaign):
    """
    get the file list for this campaign
    """
    cache = FlistCache()
    return cache.get_flist(campaign)


class FlistCache(dict):
    _flists = {}

    def get_flist(self, campaign):
        """
        get the coadd file list
        """

        bands = ['g', 'r', 'i']

        if campaign not in FlistCache._flists:
            flist_file = desimage.files.get_flist_file(campaign)

            print("reading:", flist_file)
            data = fitsio.read(flist_file, lower=True)

            flist = {}
            for i in range(data.size):

                key = data['key'][i].strip()

                path = data['path'][i].strip()
                path = path.replace('/coadd/', '/cat/')

                if 'nobkg' in path:
                    path = path.replace('_nobkg.fits.fz', '_cat.fits')
                else:
                    path = path.replace('.fits.fz', '_cat.fits')

                tilename = key[:12]

                image_path = desimage.files.get_output_file(
                    campaign,
                    tilename,
                    bands,
                )

                flist[key] = {
                    'path': path,
                    'image_path': image_path,
                }

            FlistCache._flists[campaign] = flist

        return FlistCache._flists[campaign]
