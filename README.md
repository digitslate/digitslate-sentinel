# DigitSlate Sentinel

An all-powerful toolset for DigitSlate.

Sentinel is an autonomous agent for persisting, processing and automating DigitSlate v1.2.0 governance objects and tasks.

Sentinel is implemented as a Python application that binds to a local version 1.2.0 digitslate instance on each DigitSlate v1.2.0 Masternode.

This guide covers installing Sentinel onto an existing 1.2.0 DigitSlate masternode in Ubuntu 18.04.

## Installation

### 1. Install Prerequisites

Make sure Python version 3.x.x or above is installed:

    python --version

Update system packages and ensure virtualenv and git are installed:

    sudo apt-get update
    sudo apt-get -y install python-virtualenv virtualenv git

Make sure the local DigitSlate daemon running is at least version 1.2.0

    ./digitslate-cli getinfo | grep version

### 2. Install Sentinel

Clone the Sentinel repo and install Python dependencies.

    git clone https://github.com/apollomatheus/sentinel.git && cd sentinel
    virtualenv ./venv
    ./venv/bin/pip install -r requirements.txt

### 3. Set up Cron

Set up a crontab entry to call Sentinel every minute:

    crontab -e

In the crontab editor, add the line below, replacing '/home/YOURUSERNAME/sentinel' to the path where you cloned sentinel to.

    * * * * * cd /home/YOURUSERNAME/sentinel && SENTINEL_DEBUG=1 ./venv/bin/python bin/sentinel.py >> sentinel.log 2>&1

If you followed a guide where it had you install DigitSlate to the root directory your path to where you cloned sentiel will be:

    * * * * * cd /root/sentinel && SENTINEL_DEBUG=1 ./venv/bin/python bin/sentinel.py >> sentinel.log 2>&1

## Configuration

An alternative (non-default) path to the `digitslate.conf` file can be specified in `sentinel.conf`:

    digitslate_conf=/path/to/digitslate.conf

## Troubleshooting

To view debug output, set the `SENTINEL_DEBUG` environment variable to anything non-zero, then run the script manually:

    SENTINEL_DEBUG=1 ./venv/bin/python bin/sentinel.py

To view the debug output in real time enter:

    tail -f sentinel.log

### License

Released under the MIT license, under the same terms as DigitSlate itself. See [LICENSE](digitslate.io) for more info.
