import setuptools

with open('README.rst', encoding = 'utf-8') as file:
    readme = file.read()

author = 'Exahilosys'
project = 'aiocord'

url = 'https://github.com/{0}/{1}'.format(author, project)

setuptools.setup(
    name = project,
    python_requires = '>=3.11',
    use_scm_version = True,
    setup_requires = [
        'setuptools_scm'
    ],
    url = url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    long_description = readme,
    description = 'A modern API wrapper for Discord.',
    install_requires = [
        'yarl    (>= 1.9.1, < 2.0.0)',
        'aiohttp (>= 3.8.4, < 4.0.0)',
        'vessel  (>= 4.2.0, < 5.0.0)',
        'pynacl  (>= 1.5.0, < 2.0.0)'
    ],
    extras_require = {
        'docs': [
            'sphinx',
            'sphinx-paramlinks',
            'sphinx-autodoc-typehints'
        ]
    },
    entry_points = {
        'console_scripts': [
            f'{project}={project}.vendor:main'
        ]
    }
)