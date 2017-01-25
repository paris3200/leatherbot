import setuptools

setuptools.setup(
    name="leatherbot",
    version="0.1.0",
    url="https://github.com/paris3200/leatherbot",

    author="Jason Paris",
    author_email="paris3200@gmail.com",

    description="A simple bot to help moderate a reddit subreddit.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'praw'
    ],

    entry_points={
            'console_scripts': [
                        'leatherbot=leatherbot:main',
                    ],
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.5',
    ],
)
