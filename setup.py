import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="expense_viewer",
    version="0.0.1",
    author="Subhayan Bhattacharya",
    author_email="subhayan.here@gmail.com",
    description="A small Python package to check the expenses incurred in a month",
    long_description=long_description,
    packages=setuptools.find_packages(),
    package_dir={"": "src"},
    install_requires=["fire", "pandas"],
    entry_points={"console_scripts": ["get-expense-details=expense_viewer.cli:main"]},
    python_requires=">=3.7",
)
