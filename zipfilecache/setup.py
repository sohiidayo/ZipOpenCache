from setuptools import setup, find_packages  
  
setup(  
    name='zipfilecache',  
    version='0.1',  
    packages=find_packages(),  
    install_requires=[  
    ],  
    author='AliceSohii',  
    author_email='alicesohii@outlook.com',  
    description='Provide a ZipFileCache class, which can support reading files using the compressed package path + file path in the compressed package, with memory and disk cache mechanism.',  
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  
    url='https://github.com/sohiidayo/ZipOpenCache', 
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],  
    python_requires='>=3.6',  
)