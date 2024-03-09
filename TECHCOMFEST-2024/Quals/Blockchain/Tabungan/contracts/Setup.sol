// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Tabungan.sol";

contract Setup {
    Tabungan public immutable TARGET;
    constructor() payable {
        require(msg.value == 100 ether);
        TARGET = new Tabungan();
        TARGET.setor{value: 10 ether}();
    }
    function isSolved() public view returns (bool) {
        return address(TARGET).balance == 0;
    }
}
