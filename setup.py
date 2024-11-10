from setuptools import setup, find_packages

setup(
    name='Slack_Query_Zania',
    version='0.1',
    author='Ajay',
    author_email='ajayphanin@gmail.com',
    description='An AI agent which will give responses to the user queries based on the document given',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi',
        'slack_sdk',
        'langchain',
        'openai',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
