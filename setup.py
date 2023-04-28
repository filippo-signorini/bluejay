import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bluejay",
    version="0.0.15",
    author="Filippo Signorini",
    description="A collection of BLE utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/filippo-signorini/bluejay",
    project_urls={"Bug Tracker": "https://github.com/filippo-signorini/bluejay/issues"},
    license="GNU GPLv3",
    packages=["bluejay", "bluejay.interfaces", "bluejay.managers"],
    install_requires=["dbus-python"],
)
