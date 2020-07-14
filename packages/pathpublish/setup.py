from setuptools import setup

setup(
    name='lektor-pathpublish',
    py_modules=['lektor_pathpublish'],
    version='1.0',
    entry_points={
        'lektor.plugins': [
            'pathpublish = lektor_pathpublish:PathPublishPlugin',
        ]
    }
)
