from distutils.core import setup

setup(name='socialblade',
      version='1.0.0',
      description='Object oriented SocialBlade API wrapper',
      long_description=open('README.rst', 'rb').read().decode(),
      author='sl4v',
      author_email='iamsl4v@protonmail.com',
      url='https://github.com/sl4vkek/python-socialblade',
      packages=['socialblade'],
      install_requires=['requests'],
      license="WTFPL"
     )
