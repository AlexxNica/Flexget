# FlexGet

[![travis](https://api.travis-ci.org/Flexget/Flexget.png?branch=master)](https://travis-ci.org/Flexget/Flexget)
[![pypi](https://img.shields.io/pypi/v/Flexget.svg)](https://pypi.python.org/pypi/Flexget)
[![downloads](https://img.shields.io/pypi/dm/Flexget.svg)](https://pypi.python.org/pypi/Flexget)
[![codacy grade](https://api.codacy.com/project/badge/Grade/81e8ae42c7544dc48853102b1b7f88d5)](https://www.codacy.com/app/Flexget/Flexget?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Flexget/Flexget&amp;utm_campaign=Badge_Grade)
[![codacy coverage](https://api.codacy.com/project/badge/Coverage/81e8ae42c7544dc48853102b1b7f88d5)](https://www.codacy.com/app/Flexget/Flexget?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Flexget/Flexget&amp;utm_campaign=Badge_Coverage)
[![gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/Flexget/Flexget)
[![isitmaintained.com](http://isitmaintained.com/badge/resolution/Flexget/Flexget.svg)](http://isitmaintained.com/project/Flexget/Flexget)

[FlexGet](https://flexget.com) is a multipurpose automation tool for content like torrents, nzbs,
podcasts, comics, series, movies, etc. It can use different kinds of sources
like RSS-feeds, html pages, csv files, search engines and there are even
plugins for sites that do not provide any kind of useful feeds.

## Example

Flexget uses a [YAML](http://www.yaml.org/) based configuration file.
The following example will look in the RSS feed in the link, will match any item that match the listes series names and download it::
```yaml
tasks:
  tv_task:
    rss: http://example.com/torrents.xml
    series:
    - some series
    - another series
    download: /tvshows
```

There are numerous plugins that allow utilizing FlexGet in interesting ways
and more are being added continuously.

FlexGet is extremely useful in conjunction with applications which have watch
directory support or provide interface for external utilities like FlexGet.
To get a sense of the many things that can be done with FlexGet you can take a look in our [cookbook](https://flexget.com/Cookbook)


**ChangeLog:** https://flexget.com/ChangeLog

**Help:** https://discuss.flexget.com/

**Chat:** http://webchat.freenode.net/?channels=#flexget or https://gitter.im/Flexget/Flexget

**Bugs:** https://github.com/Flexget/Flexget/issues

## Install


FlexGet is installable via pip with the command::

    pip install flexget
  

For more detailed instructions see the [installation guide](https://flexget.com/Install)

## How to use GIT checkout

Check that you have Python 2.7 / 3.3 or newer available with command `python -V`.

In some environments newer python might be available under another name like 
`python2.7` or `python3` in which case you need to use that one instead of 
plain 'python'.

To start using FlexGet from this directory:

First, install (a recent version of) the [virtualenv](https://pypi.python.org/pypi/virtualenv) package to your system.


Now, in your checkout directory, run::

    virtualenv .

Or, if you need deluge or transmission libraries from system wide python use::

    virtualenv --system-site-packages .

This will initialize python virtualenv. This doesn't need to be directly in
your checkout directory, but these instructions assume that's where it is.

Next we need to install dependencies and FlexGet itself, this can be done simply::

    bin/pip install -e .

This does an editable (`-e`) development install of the current directory (`.`).

After that FlexGet is usable via ``<checkout directory>/bin/flexget``. Verify
installation by running::

    bin/flexget -V

You may place the config file in your checkout directory, or in ``~/.flexget``
(Unix, Mac OS X) or ``C:\Documents and Setting\<username>\flexget`` (Windows).

If you don't want to use virtualenv there's ``flexget_vanilla.py`` file which
can be used to run FlexGet without virtualenv, note that you will need to
install all required dependencies yourself.

## Install using Docker 

Docker can be used to install and run FlexGet::

    docker run -it -v /home/<username>/.flexget:/root/.flexget --rm toilal/flexget

