from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="buslog",
    version="0.1.0",
    author="PoulpYBifle",
    author_email="contact@sachapreneur.fr",
    description="Business Logic Documentation Tool - Visualize and document your codebase workflows with AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/buslog",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "typer[all]>=0.12.0",
        "rich>=13.7.0",
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "jinja2>=3.1.0",
        "python-multipart>=0.0.9",
        "pyyaml>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "buslog=buslog.cli:app",
        ],
    },
    include_package_data=True,
    package_data={
        "buslog": [
            "templates/*.md",
            "web/templates/*.html",
            "web/static/*.css",
            "web/static/*.js",
        ],
    },
)
