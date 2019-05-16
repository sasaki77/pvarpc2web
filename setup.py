from setuptools import find_packages, setup

with open('README.md') as f:
        readme = f.read()

with open('LICENSE') as f:
        license = f.read()

setup(
    name='pvarpc2web',
    version='0.0.1',
    url='https://github.com/sasaki77/pvarpc2web',
    license=license,
    maintainer='Shinya Sasaki',
    maintainer_email='shinya.sasaki@kek.jp',
    description='http / pvAccess API gateway',
    long_description=readme,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-cors',
        'pvapy',
        'pytz',
        'pyyaml',
    ],
    extras_require={
        'develop': [
            'pytest',
            'pytest-cov',
            'pycodestyle'
            ]
    },
)
