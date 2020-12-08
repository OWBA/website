from setuptools import setup

setup(
    name='lektor-filedownload',
    py_modules=['lektor_filedownload'],
    version='1.0',
    entry_points={
        'lektor.plugins': [
            'filedownload = lektor_filedownload:FileDownloadPlugin',
        ]
    }
)
