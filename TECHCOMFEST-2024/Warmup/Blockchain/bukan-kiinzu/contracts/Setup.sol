// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Chall.sol";

contract Setup {
    Chall public immutable TARGET;
    constructor() payable {
        TARGET = new Chall();
    }
    function isSolved() public view returns (bool) {
        return TARGET.is_win();
    }
}
