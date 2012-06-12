from setuptools import setup, find_packages

README = open('README.md').read()

setup(name='miuibr_downloader',
      version='0.0.1',
      description='automatic download MIUI China develop roms',
      long_description=README,
      author='Douglas Camata',
      author_email='d.camata@gmail.com',
      packages=find_packages(exclude=['docs', 'tests', 'samples']),
      include_package_data=True,
      install_requires=['splinter', 'elixir', 'sqlalchemy'],
      )
