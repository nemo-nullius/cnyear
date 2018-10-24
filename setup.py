from setuptools import setup, find_packages

setup(
        name='cnyear',
        version = '0.0.10',
        description = 'A tool for conversion between Chinese year and CE.',
        author = 'Nemo',
        author_email = 'nonellf@gmail.com',
        url = 'https://github.com/nemo-nullius/cnyear',
        license = 'GPLv3',
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Topic :: Database',
            'Programming Language :: Python :: 3.7',
            ],
        keywords = 'Chinese regnal year CE conversion',
        packages = find_packages(exclude=['tests']),
        package_data = {
            # If package cnyeardb contains *.db, include it
            'cnyear':['*.db']},
        )

