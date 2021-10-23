from setuptools import setup

setup(
    name='lektor-mypublish',
    py_modules=['lektor_mypublish'],
    version='1.0',
    entry_points={
        'lektor.plugins': [
            'mypublish = lektor_mypublish:MyPublishPlugin',
        ]
    }
)
