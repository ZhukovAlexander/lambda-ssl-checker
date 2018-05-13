from setuptools import setup

setup(
    name='lambda-ssl-checker',
    url='https://github.com/ZhukovAlexander/lambda-ssl-checker',
    author='Alexander Zhukov',
    author_email='zhukovaa90@gmail.com',
    description='Serverless SSL Certificate checker',
    keywords='ssl aws lambda serverless',
    use_scm_version=True,
    python_requires=">=3.6",
    setup_requires=['setuptools_scm'],
    install_requires=['boto3'],
    packages=['checker',],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
    ],
)
