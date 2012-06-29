from setuptools import setup

setup(
    name='catalpa-aihun',
    version='1.0',
    license="",

    install_requires = [
"rapidsms",

],

    description="The common base package for catalpa's projects.",
    long_description=open('README.md').read(),
    author='Anders Hofstee, Nicoas Hoibian',
    author_email='a.hofstee@catalpainternational.org',

    url='https://github.com/catalpainternational/catalpa-aihun',
    include_package_data=True,

    packages=['aihun'],
    package_data={'aihun':['README.md']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)