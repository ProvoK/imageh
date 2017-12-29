# !/usr/bin/env python

from distutils.core import setup
setup(
    name='imageh',
    packages=[],
    version='0.1.0',
    description='Lightweight header reader for images.',
    author='Vittorio Camisa',
    license='MIT',
    author_email='vittorio.camisa@gmail.com',
    url='https://github.com/ProvoK/imageh',
    keywords=['image', 'size', 'width', 'height', 'header'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
    py_modules=['imageh'],
    entry_points='''
        [console_scripts]
        imageh=imageh.cli:cli
    '''
)
