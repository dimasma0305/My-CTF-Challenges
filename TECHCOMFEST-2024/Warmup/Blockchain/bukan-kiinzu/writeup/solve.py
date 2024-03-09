from web3 import Web3
from web3 import HTTPProvider
import solcx
import os


"""
https://github.com/foundry-rs/foundry

- Init new Project: forge init
- testing: forge test -vvv

UUID	9caea57f-101a-4c15-b982-f80e2359c2d6
RPC Endpoint	http://103.152.242.78:11661/9caea57f-101a-4c15-b982-f80e2359c2d6
Private Key	0x4c4692b78f95afe36b706dc2786a010af3e2a18ff7365788dd837b8c4f4aef31
Setup Contract	0x528c2887146f63621E49643a36AB6fd92720b5Df
Wallet	0x2C23650f91f4bc962e68DdF4590Fd4D56eE7482a
"""

RPC_URL = "http://localhost:11661/9caea57f-101a-4c15-b982-f80e2359c2d6"
PRIVKEY = "0x4c4692b78f95afe36b706dc2786a010af3e2a18ff7365788dd837b8c4f4aef31"
SETUP_CONTRACT_ADDR = "0x528c2887146f63621E49643a36AB6fd92720b5Df"

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

    def target(self):
        return self.contract.functions.TARGET().call()

    def is_solved(s):
        result = s.contract.functions.isSolved().call()
        print("is solved:", result)

class ChallContract(BaseDeployedContract):
    def __init__(self, addr) -> None:
        super().__init__(addr, "../contracts/Chall.sol:Chall")

    def free_token(self):
        self.contract.functions.free_token().transact()

    def start(self, your_guess):
        self.contract.functions.start(your_guess).transact()

    def check_tokens(self):
        token = self.contract.functions.tokens(self.account_address).call()
        print("token:", token)

class HackContract(BaseUndeployedContract):
    def __init__(self) -> None:
        super().__init__("./Hack.sol:Hack")

if __name__ == "__main__":
    setup = SetupContract()
    target = setup.target()
    chall = ChallContract(target)
    hack_base = HackContract()
    hack = hack_base.deploy_to_target(target)
    hack.contract.functions.hack().transact()
    setup.is_solved()


