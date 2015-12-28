from distutils.core import setup

setup(
    name='powerlaw',
    version='0.1',
    packages=['powerlaw',],
    license='MIT',
    author='Shagun Sodhani',
    author_email='sshagunsodhani@gmail.com',
    url='http://www.github.com/shagunsodhani/powerlaw',
    requires=['numpy', 'matplotlib', 'sklearn'],
    long_description=open('README.md').read(),
)