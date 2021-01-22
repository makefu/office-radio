from setuptools import setup, find_packages

setup(
    name="office-radio",
    version="0.2.3.4",
    license="Apache2",
    author="makefu",
    author_email="github@syntax-fehler.de",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        "Flask",
        "requests",
        "psutil",
        "python-mpd2",
    ],
    entry_points={
        'console_scripts' : [
            'stop-idle-streams = officeradio.stop_idle_streams:main',
            'office-radio = officeradio.wsgi:main'
        ]
    },
    url="http://github.com/makefu/office-radio",
)
