from setuptools import setup

setup(
    name='smms',
    version='0.1.1',
    packages=['smms'],
    url='https://github.com/CNSeniorious000/SMMS4py',
    license='MIT License',
    author='MuspiMerol',
    author_email='wjj123345567@iCloud.com',
    description='unofficial python SDK for SM.MS',
    long_description=open("readme.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    install_requires=open("requirements.txt", encoding="utf-8").read()
)
