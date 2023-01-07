from setuptools import setup

setup(
    name='smms',
    version='0.2.2',
    packages=['smms'],
    url='https://github.com/CNSeniorious000/SMMS4py',
    license='MIT License',
    author='Muspi Merol',
    author_email='wjj123345567@iCloud.com',
    description='unofficial python SDK for SM.MS',
    long_description=open("readme.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    install_requires=["httpx[http2]", "orjson", "pydantic"]
)
