from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r', encoding='utf-8') as fh:
    requirements = [line.strip() for line in fh if line.strip()]

setup(
    name='secure-file-transfer-monitoring-system',
    version='1.0.0',
    author='Gaurav Malhotra',
    author_email='your.email@example.com',
    description='A comprehensive security project for monitoring and detecting unauthorized file transfers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gauravmalhotra3300-hub/secure-file-transfer-monitoring-system',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'Topic :: Security',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'file-monitor=file_monitor:main',
        ],
    },
)
