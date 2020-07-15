from setuptools import setup

setup(
    name='lektor-cmdpublish',
    py_modules=['lektor_cmdpublish'],
    version='1.0',
    entry_points={
        'lektor.plugins': [
            'cmdpublish = lektor_cmdpublish:CmdPublishPlugin',
        ]
    }
)
