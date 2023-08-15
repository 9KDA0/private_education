import asyncio
from typing import Optional
from loguru import logger

from web3.types import TxParams
from py_eth_async.data.models import Networks, TokenAmount, Unit, Ether
from py_eth_async.client import Client
from pretty_utils.miscellaneous.files import read_json
from py_eth_async.transactions import Tx

from tasks.woofi import WooFi
from data.models import Contracts
from data.config import ABIS_DIR
from private_data import private_key1, proxy


async def check_balance():
    client = Client(network=Networks.Ethereum, proxy=proxy, check_proxy=False)
    balance = await client.wallet.balance()
    print(f'balance: {balance.Ether} | {client.account.key.hex()} | {client.account.address}')
    if balance.Wei > 0:
        exit(1)


async def bruteforce(count_tasks: int):
    u1 = Unit(amount=1, unit='ether')
    u2 = Unit(amount=2, unit='ether')
    res = u1 * u2
    print(res.Ether)

    # while True:
    #     tasks = []
    #     for _ in range(count_tasks):
    #         tasks.append(asyncio.create_task(check_balance()))
    #     await asyncio.wait(tasks)


async def main():
    client = Client(private_key=private_key1, network=Networks.Arbitrum)

    # print(client.account.address)
    # print(await client.contracts.get_signature(hex_signature='0x7dc20382'))
    # print(await client.contracts.parse_function(text_signature='swap(address,address,uint256,uint256,address,address)'))
    # print(await client.contracts.get_contract_attributes(contract=Contracts.ARBITRUM_USDC))
    # print(await client.contracts.get_abi(contract_address=Contracts.ARBITRUM_USDC.address))

    # contract = await client.contracts.get(
    #     contract_address=Contracts.ARBITRUM_WOOFI.address,
    #     abi=read_json(path=(ABIS_DIR, 'woofi.json'))
    # )

    # print(await client.contracts.get_functions(contract=Contracts.ARBITRUM_USDC))

    # print((await client.wallet.balance()).Ether)
    # print(await client.wallet.nonce())

    # print((await client.transactions.gas_price(w3=client.w3)).Wei)
    # print(await client.transactions.max_priority_fee(w3=client.w3))

    # print(await client.transactions.decode_input_data(
    #     client=client,
    #     contract=Contracts.ARBITRUM_WOOFI,
    #     input_data='0x7dc20382000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000af88d065e77c8cc2239327c5edb3a432268e583100000000000000000000000000000000000000000000000000038d7ea4c6800000000000000000000000000000000000000000000000000000000000001be86500000000000000000000000069c1dc6d723f15d7ef8154ba7194977fcc90d85b00000000000000000000000069c1dc6d723f15d7ef8154ba7194977fcc90d85b'
    # ))

    # woofi = WooFi(client=client)
    # res = await woofi.swap_eth_to_usdc(amount=TokenAmount(amount=0.001))
    # res = await woofi.swap_usdc_to_eth()
    # if 'Failed' in res:
    #     logger.error(res)
    # else:
    #     logger.success(res)

    tx_hash = '0xf9bd50990974b8107a8ef1a2d2dc79c5de6114b42d5533827068ddccabe35240'
    tx = Tx(tx_hash=tx_hash)
    print(tx)
    print(await tx.parse_params(client=client))
    print(await tx.decode_input_data(client=client, contract=Contracts.ARBITRUM_WOOFI))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
