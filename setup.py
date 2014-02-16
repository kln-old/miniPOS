import os, sys, shutil
from glob import glob

#--------------------------------------------------------------------------
# PY2EXE Setup Script
#--------------------------------------------------------------------------
if 'py2exe' in sys.argv:
    from distutils.core import setup
    import py2exe
    
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
     
    packages = ['mpos']

    # Get Data Files
    #----------------------------------------------------------------------
    # Resource Files
    res = os.path.abspath(os.path.join(os.getcwd(), 'mpos', 'resources'))
            
    paths = []
    for x in os.walk(res):
        paths.append(x[0])
    file_stuff = []
    for x in paths:
        file_stuff.append(glob(os.path.join(x, '*.*')))
    
    # Info Files
    info = os.path.abspath(os.path.join(os.getcwd(), 'mpos', 'info_files'))
    
    paths = []
    for x in os.walk(info):
        paths.append(x[0])
    info_stuff = []
    for x in paths:
        info_stuff.append(glob(os.path.join(x, '*.*')))
    
    MyDataFiles = [('resources', file_stuff[0]),
                   ('info_files', info_stuff[0]),
                   ('Microsoft.VC90.CRT', glob(r'C:/\Users/Greg Wilson/Documents/Computing/cPPdlls/*.*'))]
    
    setup(
        options = {"py2exe": {"compressed": 2,
                              "optimize": 2,
                              "packages": packages,
                              "bundle_files": 3,
                              "dist_dir": "dist",
                              "xref": False,
                              "skip_archive": False,
                              "ascii": False,
                              "custom_boot_script": '',
                             }
                  },
        windows= [
                  {'script': 'mini_pos.py',
                   'icon_resources': [(1, 'C:/\Users/Greg Wilson/Documents/Peace Corps Projects/SQ1/miniPOS/miniPOS/mpos/resources/miniPOS.ico')]
                   }
                  ],
        zipfile = "lib/library.zip",
        packages = packages,
        data_files = MyDataFiles
    )

#--------------------------------------------------------------------------
# SetupTools Setup Script
#--------------------------------------------------------------------------
else:
    try:
        from setuptools import setup, find_packages
    except ImportError:
        from ez_setup import use_setuptools
        use_setuptools()
        from setuptools import setup
        
    setup(
    name='miniPOS',
    version="1.1",
    url='http://sourceforge.net/projects/minipos',
    description='A simple POS program for record keeping.',
    long_description='A simple POS program for record keeping',
    platforms='Any',
    license='GPL3',
    author='Gregory Wilson',
    author_email='gwilson.sq1@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business :: Financial :: Point-Of-Sale',
        'Topic :: Office/Business',
        ],
    packages=['mpos'],
    package_data={'mpos': ['resources/*']},
    data_files =['doc/miniPOS_DOC.doc', 'doc/miniPOS_DOC.pdf'],
    py_modules = ['ez_setup'],
    scripts = ['mini_pos.py'],
)

        
        
        
        
    