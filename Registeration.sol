//--full name--//
//--user name--//
//--email--//
//--address--//

pragma solidity ^0.4.24;

contract Registeration {
    address owner;
    
    function Registeration() public {
        owner = msg.sender;
    }
    
   modifier onlyOwner {
       require(msg.sender == owner);
       _;
   }
      
    function hashCompareWithLengthCheck(string a, string b) internal returns (bool) {
    if(bytes(a).length != bytes(b).length) {
        return false;
    } else {
        return keccak256(a) == keccak256(b);
        }
    }
}

contract Buyer is Registeration {
    
    struct Buyer {
        string fullName;
        string UserName;
        string email;
       }
       
    mapping (address => Buyer) Buyers;
    address[] public buyersAccts;
    
    event buyerInfo(
        string fullName,
        string UserName,
        string email
       );
    
    function setBuyer(
        address _address,  
        string _fullName,
        string _UserName,
        string _email
       ) onlyOwner public {
        
        if ((hashCompareWithLengthCheck(Buyers[_address].fullName,""))){
        
        var buyer = Buyers[_address];
        
        buyer.fullName = _fullName;
        buyer.UserName  = _UserName;
        buyer.email = _email;
        
        buyersAccts.push(_address) -1;
        buyerInfo(_fullName, _UserName, _email);
    }
           
}
    
    function getBuyers() view public returns(address[]) {
        return buyersAccts;
    }
    
    function getBuyer(address _address) view public returns (string, string, string) {
        return (Buyers[_address].fullName, Buyers[_address].UserName, Buyers[_address].email);
    }
    
    function countBuyers() view public returns (uint) {
        return buyersAccts.length;
    }
    
}

// Developers //
contract Developer is Registeration {
    
    struct Developer {
        string fullName;
        string UserName;
        string email;
       }
       
    mapping (address => Developer) Developers;
    address[] public DevelopersAccts;
    
    event DeveloperInfo(
        string fullNam,
        string UserName,
        string email
       );
    
    function setDeveloper(
        address _address,  
        string _fullName,
        string _UserName,
        string _email
       ) onlyOwner public {
        
        if ((hashCompareWithLengthCheck(Developers[_address].fullName,""))){
        var Developer = Developers[_address];
        
        Developer.fullName = _fullName;
        Developer.UserName  = _UserName;
        Developer.email = _email;
        
        DevelopersAccts.push(_address) -1;
        DeveloperInfo(_fullName, _UserName, _email);
        }
               
    }
    
    function getDevelopers() view public returns(address[]) {
        return DevelopersAccts;
    }
    
    function getDeveloper(address _address) view public returns (string, string, string) {
        return (Developers[_address].fullName, Developers[_address].UserName, Developers[_address].email);
    }
    
    function countDevelopers() view public returns (uint) {
        return DevelopersAccts.length;
    }
    
}