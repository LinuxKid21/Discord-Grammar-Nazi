# Installation / Setup / Usage

This project is meant for Python 3.5 and up. Please insure that you have that
Python 3.5 or higher installed. You can check this using `python --version`
or `python3 --version`.

Python 3.5 is shipped by default in the latest versions of Ubuntu.

## Prerequisitess
You'll need to install some packages first. These are included in the
`requirements.txt` file for you.

Linux:
```bash
python3 -m pip install -r requirements.txt
# only required for doing voice on Linux environments
sudo apt-get install libffi-dev python3-dev
```

See the [discord.py documentation](http://discordpy.readthedocs.io/en/rewrite/intro.html#installing)
for why the additional tools are necessary.

Windows:
```
py -3 -m pip install -r requirements.txt
```

Mac:
```
python3 -m pip install -r requirements.txt
```

## Usage

Run the following command:
```bash
python3 main.py
```

The first lines should read something like:
```
using discordpy version 1.0.0a
Logged in SomeUser - 1234567890
Version 1.0.0a
```

# Contributing

Create a branch and PR. Or submit an issue.

