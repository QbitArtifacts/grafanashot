import setuptools
setuptools.setup(
      name="grafanashot",
      version="1.0.0",
      author="Lluis Santos",
      author_email="lluis@superadmin.org",
      license="MIT",
      description="Python & CLI tool to get snapshots from grafana server.",
      long_description=open("README.md", "r").read(),
      long_description_content_type="text/markdown",
      url="https://github.com/santoslluis/grafanashot",
      packages=setuptools.find_namespace_packages(where="src", include=['grafanashot.*']),
      package_dir={"": "src"},
      include_package_data=True,
      entry_points={
            "console_scripts": [
                  "grafanashot = grafanashot.cli.cli:CLI.main"
            ]
      },
      classifiers=[
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Environment :: Console",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Intended Audience :: Developers",
            "Topic :: Office/Business",
            "Topic :: Software Development",
            "Topic :: Software Development :: Build Tools",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Libraries :: Application Frameworks"
      ],
      install_requires=[line.strip() for line in open("requirements.txt").readlines() if len(line) > 1]
)

