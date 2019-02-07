pragma solidity ^0.4.24;

contract BuyerData{
    mapping(address => uint[]) totalNNs;
    mapping(address => mapping(uint => string)) totalNNsNames;
    
    function getTotalNNs() public view returns (uint[]) {
        return totalNNs[msg.sender];
    }
    
    function addNN(uint _id, string _name) public{
        totalNNs[msg.sender].push(_id);
        totalNNsNames[msg.sender][_id] = _name;
    }
    
    function hashCompareWithLengthCheck(string a, string b) internal returns (bool) {
    if(bytes(a).length != bytes(b).length) {
        return false;
    } else {
        return keccak256(a) == keccak256(b);
    }
}

    function isExist(uint _id) public view returns //(uint[], uint)
    (bool){
        // for (uint i=0; i< totalNNs[msg.sender].length ; i++){
        //     if (_id == totalNNs[msg.sender][i]){
        //         return true;
        //     }
        // }
        // return false;
        //return totalNNsNames[msg.sender][_id];
        return !(hashCompareWithLengthCheck(totalNNsNames[msg.sender][_id],""));
    }
    
    function removeNN(uint _id) public{
        uint length = totalNNs[msg.sender].length;
        
        for(uint i = 0; i < length; i++) {
            if (_id == totalNNs[msg.sender][i]) {
                if (1 < totalNNs[msg.sender].length && i < length-1) {
                    totalNNs[msg.sender][i] = totalNNs[msg.sender][length-1];
                }
                delete totalNNs[msg.sender][length-1];
                totalNNs[msg.sender].length--;
                delete totalNNsNames[msg.sender][_id];
                break;
            }
        }
    }
    
}