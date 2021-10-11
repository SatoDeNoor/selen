import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='selen',
    version='0.1.1',
    author='Illia Abielientsev',
    author_email='abelencev.ik@gmail.com',
    description='Selenium wrapper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/SatoDeNoor/selen',
    project_urls={
        "Bug Tracker": "https://github.com/SatoDeNoor/selen/issues"
    },
    license='MIT',
    packages=['selen'],
    install_requires=[
        'pytest-selenium',
        'allure-pytest'
    ],
    include_package_data=True
)
