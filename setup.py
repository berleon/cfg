#!/usr/bin/env python

from distutils.core import setup


setup(
    name='cfg',
    version='0.1',
    description='',
    author='Leon Sixt',
    author_email='mail@leon-sixt.de',
    url='https://github.com/berleon/cfg/',
    packages=['cfg'],
    entry_points={
        'console_scripts': [
            # 'nbstripout = fish_net.scripts.nbstripout:main',
            # 'fish_net = fish_net.scripts.fish_net:fish_net',
        ]
    }
)
