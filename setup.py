from setuptools import setup, find_packages

setup(
    name='myredmine',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'openai',
        'python-dotenv',
        'requests',
    ],
    url='https://github.com/lupin-oomura/myredmine.git',
    author='Shin Oomura',
    author_email='shin.oomura@gmail.com',
    description='A simple function for controling redmine via API',
)
