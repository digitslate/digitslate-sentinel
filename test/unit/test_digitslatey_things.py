import pytest
import sys
import os
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))


@pytest.fixture
def valid_digitslate_address(network='mainnet'):
    return 'ScHeMAQrdB2BAMZ5V8hfrd9Xveosj2F8DN' if (network == 'testnet') else '142So3onajFZfojruob5oqtxYT7SkU5Zcs'


@pytest.fixture
def invalid_digitslate_address(network='mainnet'):
    return 'ScHeMAQrdB2BAMZ5V8hfrd9Xveosj2F8DO' if (network == 'testnet') else '142So3onajFZfojruob5oqtxYT7SkU5Zct'


@pytest.fixture
def current_block_hash():
    return '000001c9ba1df5a1c58a4e458fb6febfe9329b1947802cd60a4ae90dd754b534'


@pytest.fixture
def mn_list():
    from masternode import Masternode

    masternodelist_full = {
        u'701854b26809343704ab31d1c45abc08f9f83c5c2bd503a9d5716ef3c0cda857-1': u'  ENABLED 70210 yjaFS6dudxUTxYPTDB9BYd1Nv4vMJXm3vK 1474157572    82842 1474152618  71111 52.90.74.124:11226',
        u'69a6eddb667c510baefabb9ddab0b45518556e14ebfe3019173e5075c16df349-1': u'  ENABLED 70210 yUuAsYCnG5XrjgsGvRwcDqPhgLUnzNfe8L 1474157732  1590425 1474155175  71122 [2604:a880:800:a1::9b:0]:11226',
        u'656695ed867e193490261bea74783f0a39329ff634a10a9fb6f131807eeca744-1': u'  ENABLED 70210 yepN97UoBLoP2hzWnwWGRVTcWtw1niKwcB 1474157704   824622 1474152571  71110 178.62.203.249:11226',
    }

    mnlist = [Masternode(vin, mnstring) for (vin, mnstring) in masternodelist_full.items()]

    return mnlist


@pytest.fixture
def mn_status_good():
    # valid masternode status enabled & running
    status = {
        "vin": "CTxIn(COutPoint(4b60fce7512d2a0a6afb6377dd777c5e3ec0b54942d3b0d787f9555d47d572df, 1), scriptSig=)",
        "service": "23.101.132.37:11226",
        "pubkey": "ScHeMAQrdB2BAMZ5V8hfrd9Xveosj2F8DN",
        "status": "Masternode successfully started"
    }
    return status


@pytest.fixture
def mn_status_bad():
    # valid masternode but not running/waiting
    status = {
        "vin": "CTxIn(COutPoint(0000000000000000000000000000000000000000000000000000000000000000, 4294967295), coinbase )",
        "service": "[::]:0",
        "status": "Node just started, not yet activated"
    }
    return status


# ========================================================================


def test_valid_digitslate_address():
    from digitslatelib import is_valid_digitslate_address

    main = valid_digitslate_address()
    test = valid_digitslate_address('testnet')

    assert is_valid_digitslate_address(main) is True
    assert is_valid_digitslate_address(main, 'mainnet') is True
    assert is_valid_digitslate_address(main, 'testnet') is False

    assert is_valid_digitslate_address(test) is False
    assert is_valid_digitslate_address(test, 'mainnet') is False
    assert is_valid_digitslate_address(test, 'testnet') is True


def test_invalid_digitslate_address():
    from digitslatelib import is_valid_digitslate_address

    main = invalid_digitslate_address()
    test = invalid_digitslate_address('testnet')

    assert is_valid_digitslate_address(main) is False
    assert is_valid_digitslate_address(main, 'mainnet') is False
    assert is_valid_digitslate_address(main, 'testnet') is False

    assert is_valid_digitslate_address(test) is False
    assert is_valid_digitslate_address(test, 'mainnet') is False
    assert is_valid_digitslate_address(test, 'testnet') is False


def test_deterministic_masternode_elections(current_block_hash, mn_list):
    winner = elect_mn(block_hash=current_block_hash, mnlist=mn_list)
    assert winner == '69a6eddb667c510baefabb9ddab0b45518556e14ebfe3019173e5075c16df349-1'

    winner = elect_mn(block_hash='00000056bcd579fa3dc9a1ee41e8124a4891dcf2661aa3c07cc582bfb63b52b9', mnlist=mn_list)
    assert winner == '656695ed867e193490261bea74783f0a39329ff634a10a9fb6f131807eeca744-1'


def test_deterministic_masternode_elections(current_block_hash, mn_list):
    from digitslatelib import elect_mn

    winner = elect_mn(block_hash=current_block_hash, mnlist=mn_list)
    assert winner == '69a6eddb667c510baefabb9ddab0b45518556e14ebfe3019173e5075c16df349-1'

    winner = elect_mn(block_hash='00000056bcd579fa3dc9a1ee41e8124a4891dcf2661aa3c07cc582bfb63b52b9', mnlist=mn_list)
    assert winner == '656695ed867e193490261bea74783f0a39329ff634a10a9fb6f131807eeca744-1'


def test_parse_masternode_status_vin():
    from digitslatelib import parse_masternode_status_vin
    status = mn_status_good()
    vin = parse_masternode_status_vin(status['vin'])
    assert vin == '69a6eddb667c510baefabb9ddab0b45518556e14ebfe3019173e5075c16df349-1'

    status = mn_status_bad()
    vin = parse_masternode_status_vin(status['vin'])
    assert vin is None


def test_hash_function():
    import digitslatelib
    sb_data_hex = '5b227375706572626c6f636b222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a2022795965384b77796155753559737753596d42337133727978385854557539793755697c795965384b77796155753559737753596d4233713372797838585455753979375569222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030227d5d'
    sb_hash = '5c7c28ddec8c1ad54b49f6f1e79369e7ccaf76f5ddc30e502569d674e458ccf3'

    hex_hash = "%x" % digitslatelib.hashit(sb_data_hex)
    assert hex_hash == sb_hash


def test_blocks_to_seconds():
    import digitslatelib
    from decimal import Decimal

    precision = Decimal('0.001')
    assert Decimal(digitslatelib.blocks_to_seconds(0)) == Decimal(0.0)
    assert Decimal(digitslatelib.blocks_to_seconds(2)).quantize(precision) \
        == Decimal(254.4).quantize(precision)
    assert int(digitslatelib.blocks_to_seconds(16616)) == 2113555
