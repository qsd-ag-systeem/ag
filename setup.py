from setuptools import setup

setup(
    name='Automatisch Gelaatsherkennings Systeem',
    version='0.1.0',
    py_modules=['cli/ag.py'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'cli = ag:cli',
        ],
    },
)
