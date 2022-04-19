from distutils.core import setup


setup(
    name='pmodpy',
    version='0.1.0',
    author='Luis Sordo Vieira and Cory Brunson',
    author_email='l.sordovieira@gmail.com',
    scripts=[],
    url='',
    license='LICENSE.txt',
    description='Computations of the p-modulus',
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    install_requires=[
        "python-igraph",
        "cvxpy",
        "numpy",
    ],
)
