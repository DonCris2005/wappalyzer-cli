from setuptools import setup, find_packages

if __name__ == "__main__":
    with open("requirements.txt", "r") as f:
        dependencies = f.read().splitlines()

    setup(
        name="wappalyzer-cli",
        version="0.1.0",
        packages=find_packages(),
        scripts=["src/wappy", "src/adyen_checker.py"],
        install_requires=dependencies,
    )
