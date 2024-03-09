// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract Tabungan {
    mapping(address => uint) public balances;
    function setor() public payable {
        require(msg.value > 0, 'Mana uangnya!?');
        balances[msg.sender] += msg.value;
    }
    function ambil() public {
        uint balance = balances[msg.sender];
        require(balance > 0, 'Anda tidak punya uang tabungan!');
        (bool resp,) = msg.sender.call{value: balance}("");
        require(resp, 'gagal mengirim uang!');
        balances[msg.sender] = 0;
    }
}
