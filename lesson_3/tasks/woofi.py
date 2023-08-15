import asyncio
from typing import Optional
from web3.types import TxParams
from py_eth_async.data.models import TxArgs, TokenAmount

from data.models import Contracts
from tasks.base import Base


class WooFi(Base):
    async def swap_coin(self, from_token, to_token, from_token_name, to_token_name, amount, slippage):
        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_WOOFI)
        eth_price = await self.get_token_price(token='ETH')
        min_to_amount = TokenAmount(
            amount=eth_price * float(amount.Ether) * (1 - slippage / 100),
            decimals=await self.get_decimals(contract_address=to_token.address)
        )
        args = TxArgs(
            fromToken=from_token.address,
            toToken=to_token.address,
            fromAmount=amount.Wei,
            minToAmount=min_to_amount.Wei,
            to=self.client.account.address,
            rebateTo=self.client.account.address,
        )
        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple()),
            value=amount.Wei if from_token == Contracts.ARBITRUM_ETH else 0
        )
        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} {from_token_name} was swapped to {min_to_amount.Ether} {to_token_name} via WooFi: {tx.hash.hex()}'
        return f'Failed swap {from_token_name} to {to_token_name} via WooFi!'

    async def swap_token(self, from_token, to_token, from_token_name, to_token_name, amount, slippage):
        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_WOOFI)
        eth_price = await self.get_token_price(token='ETH')

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        await self.approve_interface(token_address=from_token.address, spender=contract.address, amount=amount)
        await asyncio.sleep(5)

        eth_price = await self.get_token_price(token='ETH')
        min_to_amount = TokenAmount(
            amount=float(amount.Ether) / eth_price * (1 - slippage / 100)
        )

        args = TxArgs(
            fromToken=from_token.address,
            toToken=to_token.address,
            fromAmount=amount.Wei,
            minToAmount=min_to_amount.Wei,
            to=self.client.account.address,
            rebateTo=self.client.account.address,
        )
        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple()),
            value=amount.Wei if from_token == Contracts.ARBITRUM_ETH else 0
        )
        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} {from_token_name} was swapped to {min_to_amount.Ether} {to_token_name} via WooFi: {tx.hash.hex()}'
        return f'Failed swap {from_token_name} to {to_token_name} via WooFi!'

    async def swap_eth_to_usdc(self, amount: TokenAmount, slippage: float = 1):
        return await self.swap_coin(Contracts.ARBITRUM_ETH, Contracts.ARBITRUM_USDC,
                                    'ETH', 'USDC', amount, slippage)

    async def swap_usdc_to_eth(self, amount: Optional[TokenAmount] = None, slippage: float = 1):
        return await self.swap_token(Contracts.ARBITRUM_USDC, Contracts.ARBITRUM_ETH,
                                     'USDC', 'ETH', amount, slippage)

    async def swap_eth_to_usdt(self, amount: TokenAmount, slippage: float = 1):
        return await self.swap_coin(Contracts.ARBITRUM_ETH, Contracts.ARBITRUM_USDT,
                                    'ETH', 'USDT', amount, slippage)

    async def swap_usdt_to_eth(self, amount: Optional[TokenAmount] = None, slippage: float = 1):
        return await self.swap_token(Contracts.ARBITRUM_USDT, Contracts.ARBITRUM_ETH,
                                     'USDT', 'ETH', amount, slippage)

    async def swap_eth_to_wbtc(self, amount: TokenAmount, slippage: float = 1):
        return await self.swap_token(Contracts.ARBITRUM_ETH, Contracts.ARBITRUM_WBTC,
                                     'ETH', 'WBTC', amount, slippage)

    async def swap_wbtc_to_eth(self, amount: Optional[TokenAmount] = None, slippage: float = 1):
        return await self.swap_token(Contracts.ARBITRUM_WBTC, Contracts.ARBITRUM_ETH,
                                     'WBTC', 'ETH', amount, slippage)

    async def linea_swap_eth_to_usdc(self, amount: TokenAmount, slippage: float = 1):
        failed_text = 'Failed swap ETH to USDC via WooFi'

        contract = await self.client.contracts.get(contract_address=Contracts.LINEA_WOOFI)
        from_token = Contracts.LINEA_ETH
        to_token = Contracts.LINEA_USDC

        eth_price = await self.get_token_price(token='ETH')
        min_to_amount = TokenAmount(
            amount=eth_price * float(amount.Ether) * (1 - slippage / 100),
            decimals=await self.get_decimals(contract_address=to_token.address)
        )

        args = TxArgs(
            fromToken=from_token.address,
            toToken=to_token.address,
            fromAmount=amount.Wei,
            minToAmount=min_to_amount.Wei,
            to=self.client.account.address,
            rebateTo=self.client.account.address,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple()),
            value=amount.Wei
        )
        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} ETH was swaped to {min_to_amount.Ether} USDC via WooFi: {tx.hash.hex()}'

        return f'{failed_text}!'

    async def linea_swap_usdc_to_eth(self, amount: Optional[TokenAmount] = None, slippage: float = 1):
        failed_text = 'Failed swap USDC to ETH via WooFi'
        contract = await self.client.contracts.get(contract_address=Contracts.LINEA_WOOFI)
        from_token = Contracts.LINEA_USDC
        to_token = Contracts.LINEA_ETH

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        await self.approve_interface(token_address=from_token.address, spender=contract.address, amount=amount)
        await asyncio.sleep(5)

        eth_price = await self.get_token_price(token='ETH')
        min_to_amount = TokenAmount(
            amount=float(amount.Ether) / eth_price * (1 - slippage / 100)
        )

        args = TxArgs(
            fromToken=from_token.address,
            toToken=to_token.address,
            fromAmount=amount.Wei,
            minToAmount=min_to_amount.Wei,
            to=self.client.account.address,
            rebateTo=self.client.account.address,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=args.tuple())
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} USDC was swaped to {min_to_amount.Ether} ETH via WooFi: {tx.hash.hex()}'

        return f'{failed_text}!'