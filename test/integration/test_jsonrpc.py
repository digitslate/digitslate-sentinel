import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from digitslated import DigitSlateDaemon
from digitslate_config import DigitSlateConfig


def test_digitslated():
    config_text = DigitSlateConfig.slurp_config_file(config.digitslate_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000009f0353e76cd91b30ccb8cdc75a8fe32577c8a24b6984d4bb4abd802c04b'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c'

    creds = DigitSlateConfig.get_rpc_creds(config_text, network)
    digitslated = DigitSlateDaemon(**creds)
    assert digitslated.rpc_command is not None

    assert hasattr(digitslated, 'rpc_connection')

    # DigitSlate testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = digitslated.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert digitslated.rpc_command('getblockhash', 0) == genesis_hash
