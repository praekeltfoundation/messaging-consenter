from setuptools import find_packages, setup

setup(
    name="messaging-consenter",
    version="1.0.0",
    url="http://github.com/praekeltfoundation/messaging-consenter",
    license="BSD",
    author="Praekelt Foundation",
    author_email="dev@praekeltfoundation.org",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django~=3.0",
        "django-environ>=0.4.5,<0.5",
        "rapidpro-python>=2.6.1,<2.7",
        "raven>=6.10.0,<7",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
