from pretty_utils.type_functions.classes import Singleton
from py_eth_async.data.models import RawContract, DefaultABIs
from pretty_utils.miscellaneous.files import read_json

from data.config import ABIS_DIR


class Contracts(Singleton):
    ARBITRUM_WOOFI = RawContract(
        address='0x9aed3a8896a85fe9a8cac52c9b402d092b629a30', abi=read_json(path=(ABIS_DIR, 'woofi.json'))
    )

    ARBITRUM_USDC = RawContract(
        address='0xaf88d065e77c8cC2239327C5EDb3A432268e5831', abi=DefaultABIs.Token
    )

    ARBITRUM_ETH = RawContract(
        address='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', abi=DefaultABIs.Token
    )

    ARBITRUM_USDT = RawContract(
        address='0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9', abi=DefaultABIs.Token
    )

    ARBITRUM_WBTC = RawContract(
        address='0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f', abi=DefaultABIs.Token
    )

    LINEA_WOOFI = RawContract(
        address='0x39d361e66798155813b907a70d6c2e3fdafb0877', abi=read_json(path=(ABIS_DIR, 'woofi.json'))
    )

    LINEA_ETH = RawContract(
        address='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', abi=DefaultABIs.Token
    )

    LINEA_USDC = RawContract(
        address='0x176211869cA2b568f2A7D4EE941E073a821EE1ff', abi=DefaultABIs.Token
    )