MIUIBR Rom Downloader
=====================

A script to download development MIUI roms for the [MIUIBrasil project](http://miuibrasil.net/).


System dependencies
-------------------

This script is designed to run in any Debian-like Linux. To run it, you'll need to install a few system packages:

    [sudo] apt-get install libxml2-dev libxsl1-dev firefox

If you're running the script in text-mode only, please install *xvfb* as well:

    [sudo] apt-get install xvfb


Python dependencies
-------------------

Simply run ``python setup.py install`` to install all the script dependencies.


Configuration
-------------

For additional configuration, like log and download destination, see the constants in ``downloader.py``'s beginning.
When I have time all those constant will be turned into command line arguments to the script.


Running the script
------------------

You can start the script by just running ``python downloader.py``. In my spare time I'll try to turn this script into an egg,
put it in PyPI and create an entry point to the main function. This way it's gonna be far more easy to use it.

