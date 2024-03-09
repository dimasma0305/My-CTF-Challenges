// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract Chall {
    mapping(address => int) public tokens;
    mapping(address => bool) public already_claims;
    address private owner;
    bool public is_win;
    constructor(){
        owner = msg.sender;
    }
    function free_token() external payable {
        require(tokens[msg.sender] < 10, "Kamu sudah mengeclaim token ini");
        require(already_claims[msg.sender] == false, "Kamu sudah mengeclaim token ini");
        tokens[msg.sender] = 10;
        already_claims[msg.sender] = true;
    }
    function random() internal view returns (uint256) {
        return uint256(blockhash(block.number));
    }
    function start(uint256 your_guess) external payable {
        require(tokens[msg.sender] > 0, "Kamu bangkrut");
        uint256 to_guess = random();
        if (to_guess == your_guess){
            tokens[msg.sender] += 1;
        }else{
            tokens[msg.sender] -= 10;
        }
    }
    function win() external payable {
        require(tokens[msg.sender] > 100, "Kamu belum menang");
        is_win = true;
    }
}
