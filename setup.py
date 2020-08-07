from setuptools import setup

setup(name='conway',
      version='0.1',
      description='A library that includes the Game of Life created by John Conway',
      url='https://github.com/Programming-The-Next-Step/conway.git',
      author='Eren Asena',
      author_email='eren.asena@student.uva.nl',
      license='MIT',
      packages=['conway'],
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python :: 3.7.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
      ],
      python_requires='>=3.6',
      install_requires=[
          'pygame',
          'numpy',
          'random'
      ],
      test_suite='nose.collector',
      tests_require=['nose']
     )
