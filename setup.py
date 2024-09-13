#!/usr/bin/env python
from setuptools import setup


setup(name='oao24',
      description='observing with adaptive optics school',
      version='0.1',
      classifiers=['Development Status :: 4 - Beta',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   ],
      long_description="didactic material for the Observing with Adaptive Optics summer school 2024",
      url='',
      license='MIT',
      keywords='adaptive optics',
      install_requires=["numpy",
                        "astropy",
                        ],
      test_suite='test',
      package_data={
          'oao24': ['data/*'],
      },
      include_package_data=True,
      )
