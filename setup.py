from setuptools import setup, find_packages

setup(name='demonlist',
      version='0.11',
      description='Asynchronous wrapper for the https://demonlist.org/ API',
      packages=find_packages(),
      install_requires=[
            'aiohttp',
            'beautifulsoup4',
            'lxml',
            'urllib3',
      ],
      author='Kirill Korolev',
      url='https://github.com/K1BeR/demonlist-api',
      author_email='k1ber@protonmail.com',
      classifiers=[
            "Programming Language :: Python :: 3.7",
      ],
)
