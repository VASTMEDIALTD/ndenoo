from setuptools import find_packages, setup

setup(
    name="mpesa_b2c_integration",
    version="0.0.1",
    description="M-Pesa B2C integration for ERPNext / Frappe Cloud",
    author="VASTMEDIALTD",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["requests"],
)
