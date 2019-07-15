import os
from distutils.core import setup

scripts=[
    'sl-make-cutouts',
    'sl-make-batch',
]
scripts=[os.path.join('bin',s) for s in scripts]

setup(
    name="sleyeball", 
    packages=['sleyeball'],
    scripts=scripts,
    version="0.1.0",
    description="Make postage stamps of SL candidates",
    license = "GPL",
    author="Erin Scott Sheldon",
    author_email="erin.sheldon@gmail.com",
)




