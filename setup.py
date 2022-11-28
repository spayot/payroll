from setuptools import find_namespace_packages, setup

setup(
    name="payroll",
    version="1.0.0",
    description="Payroll Management and Recording Tool",
    author="Sylvain Payot",
    author_email="...",
    packages=["payroll"],
    package_dir={"": "src"},
    install_requires=["tk", "pyYAML"],
    extras_requires={
        "dev": [
            "pytest",
            "pytest-pep8",
            "pytest-cov",
            "ipywidgets",
        ]
    },
)
