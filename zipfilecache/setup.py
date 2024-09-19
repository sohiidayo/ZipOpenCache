from setuptools import setup, find_packages  
  
setup(  
    name='zipfilecache',  
    version='0.1',  
    packages=find_packages(),  
    install_requires=[  
    ],  
    author='AliceSohii',  
    author_email='alicesohii@outlook.com',  
    description='A Python package for caching zip file contents',  
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  
    url='https://github.com/your-username/zipfilecache',  # 你的项目在GitHub或其他地方的URL  
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],  
    python_requires='>=3.6',  
)