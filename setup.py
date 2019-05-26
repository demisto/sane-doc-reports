from setuptools import setup, find_packages

setup(
    name='sane-doc-reports',
    version='0.0.1',
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'webcolors',
        'fastjsonschema',
        'matplotlib',
        'pyquery',
        'mistune',
        'requests',
        'docx',
        'moment'
    ],
    entry_points='''
        [console_scripts]
        sane-doc=sane_doc_reports.cli:main
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

