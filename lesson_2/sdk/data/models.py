from typing import Optional
import requests

from dataclasses import dataclass
from decimal import Decimal
from typing import Union
from web3 import Web3
from eth_utils import to_wei, from_wei

from data import config


@dataclass
class DefaultABIs:
    Token = [
        {
            'constant': True,
            'inputs': [],
            'name': 'name',
            'outputs': [{'name': '', 'type': 'string'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'symbol',
            'outputs': [{'name': '', 'type': 'string'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'totalSupply',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'decimals',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [{'name': 'who', 'type': 'address'}],
            'name': 'balanceOf',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [{'name': '_owner', 'type': 'address'}, {'name': '_spender', 'type': 'address'}],
            'name': 'allowance',
            'outputs': [{'name': 'remaining', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': False,
            'inputs': [{'name': '_spender', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],
            'name': 'approve',
            'outputs': [],
            'payable': False,
            'stateMutability': 'nonpayable',
            'type': 'function'
        },
        {
            'constant': False,
            'inputs': [{'name': '_to', 'type': 'address'}, {'name': '_value', 'type': 'uint256'}],
            'name': 'transfer',
            'outputs': [], 'payable': False,
            'stateMutability': 'nonpayable',
            'type': 'function'
        }]


@dataclass
class API:
    key: str
    url: str
    docs: str


class TokenAmount:
    Wei: int
    Ether: Decimal
    decimals: int

    def __init__(self, amount: Union[int, float, str, Decimal], decimals: int = 18, wei: bool = False) -> None:
        if wei:
            self.Wei: int = amount
            self.Ether: Decimal = Decimal(str(amount)) / 10 ** decimals

        else:
            self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
            self.Ether: Decimal = Decimal(str(amount))

        self.decimals = decimals

    def __str__(self):
        return f'{self.Ether}'


class Network:
    def __init__(self, name: str, rpc: str, chain_id: Optional[int] = None, tx_type: int = 0,
                 coin_symbol: Optional[str] = None, explorer: Optional[str] = None, api: Optional[API] = None
                 ) -> None:
        self.name: str = name.lower()
        self.rpc: str = rpc
        self.chain_id: Optional[int] = chain_id
        self.tx_type: int = tx_type
        self.coin_symbol: Optional[str] = coin_symbol
        self.explorer: Optional[str] = explorer
        self.api: Optional[API] = api

        if not self.chain_id:
            try:
                self.chain_id = Web3(Web3.HTTPProvider(self.rpc)).eth.chain_id
            except:
                pass

        if not self.coin_symbol:
            try:
                response = requests.get('https://chainid.network/chains.json').json()
                for network in response:
                    if network['chainId'] == self.chain_id:
                        self.coin_symbol = network['nativeCurrency']['symbol']
                        break
            except:
                pass

        if self.coin_symbol:
            self.coin_symbol = self.coin_symbol.upper()


class Networks:
    # Mainnets
    Ethereum = Network(
        name='ethereum',
        rpc='https://eth.llamarpc.com',
        chain_id=1,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://etherscan.io/',
        api=API(key=config.ETHEREUM_API_KEY, url='https://api.etherscan.io/api', docs='https://docs.etherscan.io/'),
    )

    Arbitrum = Network(
        name='arbitrum',
        rpc='https://rpc.ankr.com/arbitrum/',
        chain_id=42161,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://arbiscan.io/',
        api=API(key=config.ARBITRUM_API_KEY, url='https://api.arbiscan.io/api', docs='https://docs.arbiscan.io/'),
    )

    ArbitrumNova = Network(
        name='arbitrum_nova',
        rpc='https://nova.arbitrum.io/rpc/',
        chain_id=42170,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://nova.arbiscan.io/',
        api=API(
            key=config.ARBITRUM_API_KEY, url='https://api-nova.arbiscan.io/api', docs='https://nova.arbiscan.io/apis/'
        )
    )

    Optimism = Network(
        name='optimism',
        rpc='https://rpc.ankr.com/optimism/',
        chain_id=10,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://optimistic.etherscan.io/',
        api=API(
            key=config.OPTIMISM_API_KEY, url='https://api-optimistic.etherscan.io/api',
            docs='https://docs.optimism.etherscan.io/'
        ),
    )

    BSC = Network(
        name='bsc',
        rpc='https://rpc.ankr.com/bsc/',
        chain_id=56,
        tx_type=0,
        coin_symbol='BNB',
        explorer='https://bscscan.com/',
        api=API(key=config.BSC_API_KEY, url='https://api.bscscan.com/api', docs='https://docs.bscscan.com/'),
    )

    Polygon = Network(
        name='polygon',
        rpc='https://rpc.ankr.com/polygon/',
        chain_id=137,
        tx_type=2,
        coin_symbol='MATIC',
        explorer='https://polygonscan.com/',
        api=API(
            key=config.POLYGON_API_KEY, url='https://api.polygonscan.com/api', docs='https://docs.polygonscan.com/'
        ),
    )

    Avalanche = Network(
        name='avalanche',
        rpc='https://rpc.ankr.com/avalanche/',
        chain_id=43114,
        tx_type=2,
        coin_symbol='AVAX',
        explorer='https://snowtrace.io/',
        api=API(key=config.AVALANCHE_API_KEY, url='https://api.snowtrace.io/api', docs='https://docs.snowtrace.io/')
    )

    Moonbeam = Network(
        name='moonbeam',
        rpc='https://rpc.api.moonbeam.network/',
        chain_id=1284,
        tx_type=2,
        coin_symbol='GLMR',
        explorer='https://moonscan.io/',
        api=API(
            key=config.MOONBEAM_API_KEY, url='https://api-moonbeam.moonscan.io/api', docs='https://moonscan.io/apis/'
        )
    )

    # todo: сделать самостоятельно
    Fantom = Network(
        name='fantom',
        rpc='https://rpc.ankr.com/fantom',
        chain_id=250,
        tx_type=0,
        coin_symbol='FTM',
        explorer='https://ftmscan.com/',
        api=API(
            key=config.FANTOM_API_KEY, url='https://api.ftmscan.com/api', docs='https://docs.ftmscan.com/'
        )
    )

    # todo: сделать самостоятельно
    Celo = Network(
        name='celo',
        rpc='https://rpc.ankr.com/celo',
        chain_id=42220,
        tx_type=2,
        coin_symbol='CELO',
        explorer='https://explorer.celo.org/mainnet/',
        api=API(
            key=config.CELO_API_KEY, url='https://explorer.celo.org/mainnet/api',
            docs='https://explorer.celo.org/mainnet/api-docs'
        )
    )

    # todo: сделать самостоятельно
    Gnosis = Network(
        name='gnosis',
        rpc='https://rpc.ankr.com/gnosis',
        chain_id=100,
        tx_type=2,
        coin_symbol='XDAI',
        explorer='https://gnosisscan.io/',
        api=API(
            key=config.GNOSIS_API_KEY, url='https://api.gnosisscan.io/api', docs='https://docs.gnosisscan.io/'
        )
    )

    # todo: сделать самостоятельно
    HECO = Network(
        name='Huobi ECO Chain Mainnet',
        rpc='https://http-mainnet.hecochain.com',
        chain_id=128,
        tx_type=2,
        coin_symbol='HT',
        explorer='https://www.hecoinfo.com/',
        api=API(
            key=config.HECO_API_KEY, url='https://api.hecoinfo.com/api', docs='https://www.hecoinfo.com/en-us/apis'
        )
    )

    # Testnets
    Goerli = Network(
        name='goerli',
        rpc='https://rpc.ankr.com/eth_goerli/',
        chain_id=5,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://goerli.etherscan.io/',
        api=API(
            key=config.GOERLI_API_KEY, url='https://api-goerli.etherscan.io/api',
            docs='https://docs.etherscan.io/v/goerli-etherscan/'
        )
    )

    # todo: сделать самостоятельно
    Sepolia = Network(
        name='Sepolia',
        rpc='https://ethereum-sepolia.blockpi.network/v1/rpc/public',
        chain_id=11155111,
        tx_type=2,
        coin_symbol='ETH',
        explorer='https://sepolia.etherscan.io/',
        api=API(
            key=config.SEPOLIA_API_KEY, url='https://api-sepolia.etherscan.io/api',
            docs='https://docs.etherscan.io/v/sepolia-etherscan'
        )
    )


class Unit:
    def __init__(self, amount: Union[int, float, str, Decimal], unit: str) -> None:
        self.unit = unit
        self.decimals = 18
        self.Wei: int = to_wei(amount, self.unit)
        self.KWei: Decimal = from_wei(self.Wei, 'kwei')
        self.MWei: Decimal = from_wei(self.Wei, 'mwei')
        self.GWei: Decimal = from_wei(self.Wei, 'gwei')
        self.Szabo: Decimal = from_wei(self.Wei, 'szabo')
        self.Finney: Decimal = from_wei(self.Wei, 'finney')
        self.Ether: Decimal = from_wei(self.Wei, 'ether')
        self.KEther: Decimal = from_wei(self.Wei, 'kether')
        self.MEther: Decimal = from_wei(self.Wei, 'mether')
        self.GEther: Decimal = from_wei(self.Wei, 'gether')
        self.TEther: Decimal = from_wei(self.Wei, 'tether')

    def __str__(self):
        return f'{self.Ether}'

    def __add__(self, other):
        if isinstance(other, (Unit, TokenAmount)):
            if self.decimals != other.decimals:
                raise ArithmeticError('The values have different decimals!')

            return Wei(self.Wei + other.Wei)

        elif isinstance(other, int):
            return Wei(self.Wei + other)

        elif isinstance(other, float):
            if self.unit == 'gwei':
                return GWei(self.GWei + GWei(other).GWei)
            else:
                return Ether(self.Ether + Ether(other).Ether)

        else:
            raise ArithmeticError(f"{type(other)} type isn't supported!")

    def __sub__(self, other):
        # todo: сделать самостоятельно
        if isinstance(other, (Unit, TokenAmount)):
            if self.decimals != other.decimals:
                raise ArithmeticError('The values have different decimals!')

            return Wei(self.Wei - other.Wei)

        elif isinstance(other, int):
            return Wei(self.Wei - Decimal(str(other)))

        elif isinstance(other, float):
            if self.unit == 'gwei':
                return GWei(self.GWei - GWei(other).GWei)

            else:
                return Ether(self.Ether - Ether(other).Ether)

        else:
            raise ArithmeticError(f"{type(other)} type isn't supported!")

    def __mul__(self, other):
        # todo: сделать самостоятельно
        if isinstance(other, (Unit, TokenAmount)):
            if self.decimals != other.decimals:
                raise ArithmeticError('The values have different decimals!')

            return Wei(self.Wei * other.Wei)

        elif isinstance(other, int):
            return Wei(self.Wei * Decimal(str(other)))

        elif isinstance(other, float):
            if self.unit == 'gwei':
                return GWei(self.GWei * GWei(other).GWei)

            else:
                return Ether(self.Ether * Ether(other).Ether)

        else:
            raise ArithmeticError(f"{type(other)} type isn't supported!")

    def __truediv__(self, other):
        if isinstance(other, (Unit, TokenAmount)):
            if self.decimals != other.decimals:
                raise ArithmeticError('The values have different decimals!')

            return Wei(self.Wei / other.Wei)

        elif isinstance(other, int):
            return Wei(self.Wei / Decimal(str(other)))

        elif isinstance(other, float):
            if self.unit == 'gwei':
                return GWei(self.GWei / GWei(other).GWei)

            else:
                return Ether(self.Ether / Ether(other).Ether)

        else:
            raise ArithmeticError(f"{type(other)} type isn't supported!")

    def __iadd__(self, other):
        return self.__add__(other)

    def __isub__(self, other):
        # todo: сделать самостоятельно
        return self.__sub__(other)

    def __imul__(self, other):
        # todo: сделать самостоятельно
        return self.__mul__(other)

    def __itruediv__(self, other):
        return self.__truediv__(other)

    def __lt__(self, other):
        if isinstance(other, (Unit, TokenAmount)):
            if self.decimals != other.decimals:
                raise ArithmeticError('The values have different decimals!')

            return self.Wei < other.Wei

        elif isinstance(other, int):
            return self.Wei < other

        elif isinstance(other, float):
            if self.unit == 'gwei':
                return self.GWei < GWei(other).GWei

            else:
                return self.Ether < Ether(other).Ether

        else:
            raise ArithmeticError(f"{type(other)} type isn't supported!")

    def __le__(self, other):
        # todo: сделать самостоятельно
        if isinstance(other, (Unit, TokenAmount)):
            if self.decimals != other.decimals:
                raise ArithmeticError('The values have different decimals!')

            return self.Wei <= other.Wei

        elif isinstance(other, int):
            return self.Wei <= other

        elif isinstance(other, float):
            if self.unit == 'gwei':
                return self.GWei <= GWei(other).GWei

            else:
                return self.Ether <= Ether(other).Ether

        else:
            raise ArithmeticError(f"{type(other)} type isn't supported!")

    def __eq__(self, other):
        if isinstance(other, (Unit, TokenAmount)):
            if self.decimals != other.decimals:
                raise ArithmeticError('The values have different decimals!')

            return self.Wei == other.Wei

        elif isinstance(other, int):
            return self.Wei == other

        elif isinstance(other, float):
            if self.unit == 'gwei':
                return self.GWei == GWei(other).GWei

            else:
                return self.Ether == Ether(other).Ether

        else:
            raise ArithmeticError(f"{type(other)} type isn't supported!")

    def __ne__(self, other):
        # todo: сделать самостоятельно
        if isinstance(other, (Unit, TokenAmount)):
            if self.decimals != other.decimals:
                raise ArithmeticError('The values have different decimals!')

            return self.Wei != other.Wei

        elif isinstance(other, int):
            return self.Wei != other

        elif isinstance(other, float):
            if self.unit == 'gwei':
                return self.GWei != GWei(other).GWei

            else:
                return self.Ether != Ether(other).Ether

        else:
            raise ArithmeticError(f"{type(other)} type isn't supported!")

    def __gt__(self, other):
        if isinstance(other, (Unit, TokenAmount)):
            if self.decimals != other.decimals:
                raise ArithmeticError('The values have different decimals!')

            return self.Wei > other.Wei

        elif isinstance(other, int):
            return self.Wei > other

        elif isinstance(other, float):
            if self.unit == 'gwei':
                return self.GWei > GWei(other).GWei

            else:
                return self.Ether > Ether(other).Ether

        else:
            raise ArithmeticError(f"{type(other)} type isn't supported!")

    def __ge__(self, other):
        # todo: сделать самостоятельно
        if isinstance(other, (Unit, TokenAmount)):
            if self.decimals != other.decimals:
                raise ArithmeticError('The values have different decimals!')

            return self.Wei >= other.Wei

        elif isinstance(other, int):
            return self.Wei >= other

        elif isinstance(other, float):
            if self.unit == 'gwei':
                return self.GWei > GWei(other).GWei

            else:
                return self.Ether >= Ether(other).Ether

        else:
            raise ArithmeticError(f"{type(other)} type isn't supported!")


class Wei(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'wei')


class KWei(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'kwei')


class MWei(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'mwei')


class GWei(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'gwei')


class Szabo(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'szabo')


class Finney(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'finney')


class Ether(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'ether')


# todo: сделать самостоятельно
class KEther(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'kether')


# todo: сделать самостоятельно
class MEther(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'mether')


# todo: сделать самостоятельно
class GEther(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'gether')


# todo: сделать самостоятельно
class TEther(Unit):
    def __init__(self, amount: Union[int, float, str, Decimal]) -> None:
        super().__init__(amount, 'tether')

# u1 = Unit(amount=0, unit='ether')
# u2 = Unit(amount=1, unit='ether')

# print(u1 + u2)
# print(u1 - u2)
# print(u1 * u2)
# print(u1 < u2)
# print(u1 <= u2)
# print(u1 == u2)
# print(u1 != u2)
# print(u1 > u2)
# print(u1 >= u2)

