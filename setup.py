from setuptools import setup, find_packages

setup(
    name='lognimbus',
    version='0.1.0',
    description='A YAML-based logging library with rich formatting for container and Kubernetes environments',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Denis Tu',
    author_email='dmarshaltu@gmail.com',
    url='https://github.com/dmarshaltu/lognimbus',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
        'rich',
        'prometheus_client'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
