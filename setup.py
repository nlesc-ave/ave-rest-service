from setuptools import setup

setup(
    name='avedata',
    packages=['avedata'],
    include_package_data=True,
    install_requires=[
        'flask',
        'click',
        'connexion'
    ],
    entry_points='''
        [console_scripts]
        avedata=avedata.commands:cli
    ''',
)
