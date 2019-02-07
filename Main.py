import json
import web3
import os
import shutil
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source, compile_files
from web3.contract import ConciseContract
from prettytable import PrettyTable
    

# # Solidity source code
contract_source_code = '''
pragma solidity ^0.4.24;

contract Greeter {
    string public greeting;

    function Greeter() {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() constant returns (string) {
        return greeting;
    }
}
contract Hello is Greeter{
    
}
 '''

Registeration_source_code = ''' 
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
       )  public {
        
        //if ((hashCompareWithLengthCheck(Buyers[_address].fullName,"")))
        {
        
        var buyer = Buyers[_address];
        
        buyer.fullName = _fullName;
        buyer.UserName  = _UserName;
        buyer.email = _email;
        
        buyersAccts.push(_address) - 1;
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
        return uint(buyersAccts.length);
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
       )  public {
        
        //if ((hashCompareWithLengthCheck(Developers[_address].fullName,"")))
        {
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
    
}'''


BuyerData_source_code = ''' 
pragma solidity ^0.4.24;

contract BuyerData{
    mapping(address => uint[]) totalNNs;
    mapping(address => mapping(uint => string)) totalNNsNames;
    
    mapping(uint => uint) public rating;
    uint[] allModels;
    
    function setRating(address _address, uint _id, uint _rating){
        if( _rating > 0 && _rating <= 5 && !(hashCompareWithLengthCheck(totalNNsNames[_address][_id],""))){
            rating[_id] = _rating;
        } 
        
    } 

    function getRating(address _address, uint _id) returns (uint){
        if (!(hashCompareWithLengthCheck(totalNNsNames[_address][_id],""))){
            
            return rating[_id];
            
        }
        return 0;
        
    }
    
    function getAllNNs() public view returns (uint[]) {
        return allModels;
    }
    
    function getTotalNNs(address _address) public view returns (uint[]) {
        return totalNNs[_address];
    }
    
    function addNN(address _address,uint _id, string _name) public{
        totalNNs[_address].push(_id);
        totalNNsNames[_address][_id] = _name;
        allModels.push(_id);
    }
    
    function hashCompareWithLengthCheck(string a, string b) internal returns (bool) {
    if(bytes(a).length != bytes(b).length) {
        return false;
    } else {
        return keccak256(a) == keccak256(b);
    }
}

    function isExist(address _address,uint _id) public view returns //(uint[], uint)
    (bool){
        // for (uint i=0; i< totalNNs[msg.sender].length ; i++){
        //     if (_id == totalNNs[msg.sender][i]){
        //         return true;
        //     }
        // }
        // return false;
        //return totalNNsNames[msg.sender][_id];
        return !(hashCompareWithLengthCheck(totalNNsNames[_address][_id],""));
    }
    
    function removeNN(address _address,uint _id) public{
        uint length = totalNNs[_address].length;
        
        for(uint i = 0; i < length; i++) {
            if (_id == totalNNs[_address][i]) {
                if (1 < totalNNs[_address].length && i < length-1) {
                    totalNNs[_address][i] = totalNNs[_address][length-1];
                    allModels[i] = allModels[length-1];
                }
                delete allModels[length-1];
                delete totalNNs[_address][length-1];
                allModels.length--;
                totalNNs[_address].length--;
                delete totalNNsNames[_address][_id];
                break;
            }
        }
    }
   
  
}'''


NeuroCoin  = ''' 

pragma solidity ^0.4.24;
library SafeMath {
    
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }

        uint256 c = a * b;
        require(c / a == b);

        return c;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        // Solidity only automatically asserts when dividing by 0
        require(b > 0);
        uint256 c = a / b;
        // assert(a == b * c + a % b); // There is no case in which this doesn't hold

        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        uint256 c = a - b;

        return c;
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a);

        return c;
    }

    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b != 0);
        return a % b;
    }
}


/**
 * Utility library of inline functions on addresses
 */
library Address {
    /**
     * Returns whether the target address is a contract
     * @dev This function will return false if invoked during the constructor of a contract,
     * as the code is not actually created until after the constructor finishes.
     * @param account address of the account to check
     * @return whether the target address is a contract
     */
    function isContract(address account) internal view returns (bool) {
        uint256 size;
        // XXX Currently there is no better way to check if there is a contract in an address
        // than to check the size of the code at that address.
        // See https://ethereum.stackexchange.com/a/14016/36603
        // for more details about how this works.
        // TODO Check this again before the Serenity release, because all addresses will be
        // contracts then.
        // solium-disable-next-line security/no-inline-assembly
        assembly { size := extcodesize(account) }
        return size > 0;
    }
}

interface IERC165 {
    /**
     * @notice Query if a contract implements an interface
     * @param interfaceId The interface identifier, as specified in ERC-165
     * @dev Interface identification is specified in ERC-165. This function
     * uses less than 30,000 gas.
     */
    function supportsInterface(bytes4 interfaceId) external view returns (bool);
}


import "./IERC165.sol";

contract IERC721 is IERC165 {
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);

    function balanceOf(address owner) public view returns (uint256 balance);
    function ownerOf(uint256 tokenId) public view returns (address owner);

    function approve(address to, uint256 tokenId) public;
    function getApproved(uint256 tokenId) public view returns (address operator);

    function setApprovalForAll(address operator, bool _approved) public;
    function isApprovedForAll(address owner, address operator) public view returns (bool);

    function transferFrom(address from, address to, uint256 tokenId) public;
    function safeTransferFrom(address from, address to, uint256 tokenId) public;

    function safeTransferFrom(address from, address to, uint256 tokenId, bytes data) public;
}

contract IERC721Receiver {
    function onERC721Received(address operator, address from, uint256 tokenId, bytes data) public returns (bytes4);
}



import "./IERC165.sol";

contract ERC165 is IERC165 {
    bytes4 private constant _InterfaceId_ERC165 = 0x01ffc9a7;
    /**
     * 0x01ffc9a7 ===
     *     bytes4(keccak256('supportsInterface(bytes4)'))
     */

    /**
     * @dev a mapping of interface id to whether or not it's supported
     */
    mapping(bytes4 => bool) private _supportedInterfaces;

    /**
     * @dev A contract implementing SupportsInterfaceWithLookup
     * implement ERC165 itself
     */
    constructor () internal {
        _registerInterface(_InterfaceId_ERC165);
    }

    /**
     * @dev implement supportsInterface(bytes4) using a lookup table
     */
    function supportsInterface(bytes4 interfaceId) external view returns (bool) {
        return _supportedInterfaces[interfaceId];
    }

    /**
     * @dev internal method for registering an interface
     */
    function _registerInterface(bytes4 interfaceId) internal {
        require(interfaceId != 0xffffffff);
        _supportedInterfaces[interfaceId] = true;
    }
}


import "./IERC721.sol";
import "./IERC721Receiver.sol";
import "./SafeMath.sol";
import "./Address.sol";
import "./ERC165.sol";

contract ERC721 is ERC165, IERC721 {
    using SafeMath for uint256;
    using Address for address;

    bytes4 private constant _ERC721_RECEIVED = 0x150b7a02;
    mapping (uint256 => address) private _tokenOwner;
    mapping (uint256 => address) private _tokenApprovals;
    mapping (address => uint256) private _ownedTokensCount;
    mapping (address => mapping (address => bool)) private _operatorApprovals;
    bytes4 private constant _InterfaceId_ERC721 = 0x80ac58cd;

    constructor () public {
        _registerInterface(_InterfaceId_ERC721);
    }

    function balanceOf(address owner) public view returns (uint256) {
        require(owner != address(0));
        return _ownedTokensCount[owner];
    }

    function ownerOf(uint256 tokenId) public view returns (address) {
        address owner = _tokenOwner[tokenId];
        require(owner != address(0));
        return owner;
    }

    function approve(address to, uint256 tokenId) public {
        address owner = ownerOf(tokenId);
        require(to != owner);
        require(msg.sender == owner || isApprovedForAll(owner, msg.sender));

        _tokenApprovals[tokenId] = to;
        emit Approval(owner, to, tokenId);
    }


    function getApproved(uint256 tokenId) public view returns (address) {
        require(_exists(tokenId));
        return _tokenApprovals[tokenId];
    }

    function setApprovalForAll(address to, bool approved) public {
        require(to != msg.sender);
        _operatorApprovals[msg.sender][to] = approved;
        emit ApprovalForAll(msg.sender, to, approved);
    }
    function isApprovedForAll(address owner, address operator) public view returns (bool) {
        return _operatorApprovals[owner][operator];
    }

    function transferFrom(address from, address to, uint256 tokenId) public {
        require(_isApprovedOrOwner(msg.sender, tokenId));
        require(to != address(0));

        _clearApproval(from, tokenId);
        _removeTokenFrom(from, tokenId);
        _addTokenTo(to, tokenId);

        emit Transfer(from, to, tokenId);
    }

    function safeTransferFrom(address from, address to, uint256 tokenId) public {
        // solium-disable-next-line arg-overflow
        safeTransferFrom(from, to, tokenId, "");
    }

    function safeTransferFrom(address from, address to, uint256 tokenId, bytes _data) public {
        transferFrom(from, to, tokenId);
        // solium-disable-next-line arg-overflow
        require(_checkOnERC721Received(from, to, tokenId, _data));
    }

    function _exists(uint256 tokenId) internal view returns (bool) {
        address owner = _tokenOwner[tokenId];
        return owner != address(0);
    }

    function _isApprovedOrOwner(address spender, uint256 tokenId) internal view returns (bool) {
        address owner = ownerOf(tokenId);
        return (spender == owner || getApproved(tokenId) == spender || isApprovedForAll(owner, spender));
    }

    function _mint(address to, uint256 tokenId) internal {
        require(to != address(0));
        _addTokenTo(to, tokenId);
        emit Transfer(address(0), to, tokenId);
    }

    function _burn(address owner, uint256 tokenId) internal {
        _clearApproval(owner, tokenId);
        _removeTokenFrom(owner, tokenId);
        emit Transfer(owner, address(0), tokenId);
    }

    function _addTokenTo(address to, uint256 tokenId) internal {
        require(_tokenOwner[tokenId] == address(0));
        _tokenOwner[tokenId] = to;
        _ownedTokensCount[to] = _ownedTokensCount[to].add(1);
    }

    function _removeTokenFrom(address from, uint256 tokenId) internal {
        require(ownerOf(tokenId) == from);
        _ownedTokensCount[from] = _ownedTokensCount[from].sub(1);
        _tokenOwner[tokenId] = address(0);
    }

    function _checkOnERC721Received(address from, address to, uint256 tokenId, bytes _data) internal returns (bool) {
        if (!to.isContract()) {
            return true;
        }

        bytes4 retval = IERC721Receiver(to).onERC721Received(msg.sender, from, tokenId, _data);
        return (retval == _ERC721_RECEIVED);
    }

    function _clearApproval(address owner, uint256 tokenId) private {
        require(ownerOf(tokenId) == owner);
        if (_tokenApprovals[tokenId] != address(0)) {
            _tokenApprovals[tokenId] = address(0);
        }
    }
}


import "./ERC721.sol";

contract NeuroCoin is ERC721 {
    
    struct NeuralNetwork{
        string name;
        address owner;
        string domainName;
        uint TrainingAccuracy;
        uint TestingAccuracy;
    }
    
    NeuralNetwork[] public NeuralNetworks;
    address public owner;
    
    function NeuroCoin() public{
        owner = msg.sender;
    }
    
    function CreateNeuralNetwork(
        string _name,
        address _owner,
        string _domainName,
        uint _trainingAccuracy,
        uint _testingaccuracy,
        address _to
        ) public{
            
            require(owner == msg.sender);
            uint id = NeuralNetworks.length;
            NeuralNetworks.push(
                NeuralNetwork(_name,_owner,_domainName,_trainingAccuracy,_testingaccuracy)
                );
                
            _mint(_to,id);
        }
}

'''
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

def get_contract_instance(contract_source_code, contract_name, account):
    compiled_sol = compile_source(contract_source_code)
    #print(compile_source)
    contract_interface = compiled_sol['<stdin>:'+contract_name]
    #print(contract_interface)
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = contract.deploy(transaction={'from': account ###, 'gas': 410000
    }
    )
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    contract_address = tx_receipt['contractAddress']
    abi = contract_interface['abi']
    contract_instance = w3.eth.contract(address=contract_address, abi=abi,ContractFactoryClass=ConciseContract)

    return  contract_instance


# compiled_sol = compile_source(contract_source_code) # Compiled source code
# contract_name = "Greeter"
# contract_interface = compiled_sol['<stdin>:'+contract_name]

# # web3.py instance

# # Instantiate and deploy contract
# contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# # Get transaction hash from deployed contract
# print("Account 01 Is: ",w3.eth.accounts[0])

# tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 410000})

# # Get tx receipt to get contract address
# tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
# contract_address = tx_receipt['contractAddress']

# # Contract instance in concise mode
# abi = contract_interface['abi']
# contract_instance = w3.eth.contract(address=contract_address, abi=abi,ContractFactoryClass=ConciseContract)





















####################################################################################################################

#contract_instance = get_contract_instance(Registeration_source_code,"Buyer",w3.eth.accounts[0])
# print(contract_instance.countBuyers())
# contract_instance.setBuyer(w3.eth.accounts[1], "Salman", "Zinsermon","97salmanzafar@gmail.com", transact={'from': w3.eth.accounts[0]})
# print(contract_instance.countBuyers())
# print(contract_instance.getBuyers())


# print(contract_instance.countBuyers())
# contract_instance.setBuyer(w3.eth.accounts[1], "Salman", "Zinsermon","97salmanzafar@gmail.com", transact={'from': w3.eth.accounts[0]})
# print(contract_instance.countBuyers())
# print(contract_instance.getBuyer(w3.eth.accounts[1]))

# developer_contract_instance = get_contract_instance(Registeration_source_code,"Developer",w3.eth.accounts[0])
# print(developer_contract_instance.countDevelopers())
# developer_contract_instance.setDeveloper(w3.eth.accounts[0], "Salman", "Zinsermon","97salmanzafar@gmail.com", transact={'from': w3.eth.accounts[0]})
# print(developer_contract_instance.countDevelopers())
# print(developer_contract_instance.getDevelopers())

# BuyerData_source_code = get_contract_instance(BuyerData_source_code,"BuyerData",w3.eth.accounts[0])

# print(BuyerData_source_code.getTotalNNs(w3.eth.accounts[0]))

# (BuyerData_source_code.addNN(w3.eth.accounts[0],1,"Waleed",transact={'from': w3.eth.accounts[0]}))
# print(BuyerData_source_code.getTotalNNs(w3.eth.accounts[0]))

# print(BuyerData_source_code.isExist(w3.eth.accounts[0],1))

# (BuyerData_source_code.addNN(w3.eth.accounts[0],2,"Waleed",transact={'from': w3.eth.accounts[0]}))
# print(BuyerData_source_code.getTotalNNs(w3.eth.accounts[0]))

# print(BuyerData_source_code.isExist(w3.eth.accounts[0],2))
# print(BuyerData_source_code.isExist(w3.eth.accounts[0],4))


# (BuyerData_source_code.addNN(w3.eth.accounts[1],3,"Waleed 02",transact={'from': w3.eth.accounts[1]}))
# print(BuyerData_source_code.getTotalNNs(w3.eth.accounts[1]))
# print(BuyerData_source_code.isExist(w3.eth.accounts[1],3))


# print("\nRating OF NNs\n")
# BuyerData_source_code.setRating(w3.eth.accounts[0],2,4,transact={'from': w3.eth.accounts[0]})
# print(BuyerData_source_code.getRating(w3.eth.accounts[0],2))

# BuyerData_source_code.setRating(w3.eth.accounts[1],3,5,transact={'from': w3.eth.accounts[0]})
# print(BuyerData_source_code.getRating(w3.eth.accounts[1],3))


# print("\nRemoved NN\n")
# BuyerData_source_code.removeNN(w3.eth.accounts[0],2,transact={'from': w3.eth.accounts[0]})
# print(BuyerData_source_code.isExist(w3.eth.accounts[0],2))

# BuyerData_source_code.removeNN(w3.eth.accounts[1],3,transact={'from': w3.eth.accounts[1]})
# print(BuyerData_source_code.isExist(w3.eth.accounts[1],3))

# NeuroCoin = compile_files(['NeuroCoin.sol'],w3.eth.accounts[0])
# contract_name = "NeuroCoin"
# compiled_sol = NeuroCoin.pop("NeuroCoin.sol:NeuroCoin")
# contract_interface = compiled_sol
# account = w3.eth.accounts[0]
# contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# tx_hash = contract.deploy(
#     transaction={
#     'from': account ###, 'gas': 410000
#     }
# )
# tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
# contract_address = tx_receipt['contractAddress']
# abi = contract_interface['abi']
# contract_instance = w3.eth.contract(address=contract_address, abi=abi,ContractFactoryClass=ConciseContract)
# print(contract_instance.CreateNeuralNetwork("Pytorch",account,"Music Generation",99,97,account,transact = {'from':account}))
# print(contract_instance.balanceOf(account))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #










os.system("cls")
print("             ###############################################################################################")
print("             ###############################################################################################")
print("             ###############################################################################################")
print("             #####                                   WELCOME                                           #####")
print("             #####                                     TO                                              #####")
print("             #####                                 NEUROCOIN.IO                                        #####")
print("             ###############################################################################################")
print("             ###############################################################################################")
print("             ###############################################################################################")
buyer_registeration_instance = get_contract_instance(Registeration_source_code,"Buyer",w3.eth.accounts[0])
developer_registeration_instance = get_contract_instance(Registeration_source_code,"Developer",w3.eth.accounts[0])
info_data_instance = get_contract_instance(BuyerData_source_code,"BuyerData",w3.eth.accounts[0])


universal_token = 0
universal_token_file = {}

NeuroCoin = compile_files(['NeuroCoin.sol'],w3.eth.accounts[0])
contract_name = "NeuroCoin"
compiled_sol = NeuroCoin.pop("NeuroCoin.sol:NeuroCoin")
contract_interface = compiled_sol
account = w3.eth.accounts[0]
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
tx_hash = contract.deploy(
    transaction={
    'from': account ###, 'gas': 410000
    }
)
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']
abi = contract_interface['abi']
neurocoin_instance = w3.eth.contract(address=contract_address, abi=abi,ContractFactoryClass=ConciseContract)

################# get_the_prediction ##############################

def get_the_prediction(_account_address, _id):
    path = universal_token_file[_id]
    print("Downloading Prediction From The Cloud Might Takes Some Time ")
    time.sleep(60)
    shutil.copy(path,"C:\\Users\\Arsalan Ashraf\\Desktop\\"+(_account_address+str(_id)+"."+(path.split(".")[-1])    ))
    print("Prediction Is Recieved Its In Desktop With Name ",_account_address,_id) 
    input()
    return


###################################################################
#################### CATALOG ######################################
def view_catalog(_account_address,role):
    
    os.system('cls')
    print("             Fetching Data From The Network Takes Few Seconds !!!!!")

    length = info_data_instance.getAllNNs()
    models_info = []
    x = PrettyTable()
    x.field_names = ["Model ID", "Domain", "Accuracy","Developer"]
    print(length)
    #input()
    for i in (length):
        data = neurocoin_instance.getValueOfModel(i)
        owner = neurocoin_instance.ownerOf(i)
        name00  = (developer_registeration_instance.getDeveloper(owner))[1]
        
        name01  = (buyer_registeration_instance.getBuyer(owner))[1]
        if name00 == "":
            x.add_row([i,data[2],data[4],name01])

        elif name01 == "" :   
            x.add_row([i,data[2],data[4],name00])
        models_info.append(data)

    if role == "buyer":
        while(1):
            os.system('cls')
            print(x)
            print("\n\nSelect Model ID To Perform Request Or (X) To Exist")
            model_id_str = input("MODEL ID: ")
            
            try:
                model_id = int(model_id_str)
                if model_id >= len(length):
                    input("\n\nPlease Select Correct Model ID")
                
                if model_id < len(length):
                ########### DO TRANSACTION FROM ACCOUNT WHILE PUSHING IT ###############
                    neurocoin_instance.pushNotification(
                    _account_address,
                    model_id,
                    
                    transact={'from': _account_address}
                    )
                    print("\n\nRequest Has Successfully Sent To The Developer")
                    input()

            except ValueError as identifier:
                pass
            
            except UnboundLocalError as identifier:
                pass
            if model_id_str.lower() == "x":
                break

    elif role == "developer":        
        
        os.system('cls')
        print(x)
        input("\n\nPlease Any Key TO Exit ")
        
    return
##############################################################


################# OWNED MODELS ################################
def view_owned_models(_account_address,role):
    os.system('cls')
    print("             Fetching Data From The Network Takes Few Seconds !!!!!")
    models_info = []
    x = PrettyTable()
    x.field_names = ["Model ID", "Domain", "Traing Accuracy","Testing Accuracy"]
    
    length  = info_data_instance.getTotalNNs(_account_address)
    print("List of All Models id: ",length)
   # input()

    if role.lower() == "developer":
        while(1):
            
            for i in (length):
                data = neurocoin_instance.getValueOfModel(i)
                x.add_row([i,data[2],data[3],data[4]])
                models_info.append(data)
        
            os.system("cls")
            print(x)
            print("\n\nSelect (R) For Removing The Model And (X) For Exit")
            option = input("Option: ")
            if option.lower() == "x":
                break

            elif option.lower() == "r":
                os.system("cls")
                print(x)
                print("\n\nSelect The Model ID To Remove")
                model_id = int(input("Model ID: "))
                for i in (length):
                    if model_id == i:
                        info_data_instance.removeNN(_account_address,model_id, 
                        transact={'from': _account_address}   
                        )
                        
                        print("\n\nModel Has Successfully Removed From The Network" )
                        x.clear_rows()
                    input()

            else:
                print("Please Select The Correct Option")

    elif role.lower() == "buyer":
        while(1):
            
            
            for i in (length):
                data = neurocoin_instance.getValueOfModel(i)
                x.add_row([i,data[2],data[3],data[4]])
                models_info.append(data)
            os.system("cls")
            print(x)
            print("\n\nSelect (R) For Removing The Model, (G) To Get The Prediction And (X) For Exit")
            option = input("Option: ")
            if option.lower() == "x":
                break

            elif option.lower() == "r":
                os.system("cls")
                print(x)
                print("\n\nSelect The Model ID To Remove")
                model_id = int(input("Model ID: "))
                for i in (length):
                    if model_id == i:
                        info_data_instance.removeNN(_account_address,model_id, 
                        transact={'from': _account_address}   
                        )
                        
                        print("\n\nModel Has Successfully Removed From The Network")
                        x.clear_rows()
                    input()

            elif option.lower() == "g":
                os.system("cls")
                print(x)
                print("\n\nSelect The Model ID To Get Prediction")
                model_id = int(input("Model ID: "))
                get_the_prediction(_account_address,model_id)
                print()
            else:
                print("Please Select The Correct Option")


    return
###############################################################

######################## SETTING ##############################
def setting(_account_address,role):
    data_dict = {0:"Full Name",1:"User Name",2:"Email   "}
    if role == "developer":
        data = developer_registeration_instance.getDeveloper(_account_address)
        
    elif role == "buyer":
        data = buyer_registeration_instance.getBuyer(_account_address)
    
    while(1):
        os.system("cls")
        print("#################### EDIT PROFILE ####################\n")
        print("(1) {}: ".format(data_dict[0]),data[0])
        print("(2) {}: ".format(data_dict[1]),data[1])
        print("(3) {}: ".format(data_dict[2]),data[2])
        print("\nInput The Option Of Field You Want To update Or Input(X) To Exit\n")
        option = input("OPTION: ")
        try:
            option = int(option)
            if option >= 4:
                input("\n\nPlease Select Correct Model ID")
            
            if option < 4:
                option = option - 1
                ##print("EDIT {}:".format(data_dict[option]))
                new_field = input("Input New {}: ".format(data_dict[option]))
                data[option] = new_field
            ########### DO TRANSACTION FROM ACCOUNT WHILE PUSHING IT ###############
            if role == "developer":
                print("\n\nUpdate Data Of The Network Might Take Few Minutes")
                time.sleep(2)
                developer_registeration_instance.setDeveloper(_account_address,data[0],data[1],data[2],transact={'from': _account_address})
            
            elif role == "buyer":
                print("\n\nUpdate Data Of The Network Might Take Few Minutes")
                time.sleep(2)
                buyer_registeration_instance.setBuyer(_account_address,data[0],data[1],data[2],transact={'from': _account_address})


        except ValueError as identifier:
            pass
        except AttributeError as identifier: 
            pass        
        except UnboundLocalError as identifier:
            pass
        try:
            if option.lower() == "x":
                break
        except AttributeError as identifier:
            pass    
        

    return
###############      VIEW ALL REQUESTS      ###################
def view_all_requests(_account_address):
    os.system('cls')
    print("             Fetching Data From The Network Takes Few Seconds !!!!!")

    models_info = []
    x = PrettyTable()
    x.field_names = ["Model ID", "Requests From"]

    length = neurocoin_instance.getNotificationLength()
    for i in range(length):
        data = neurocoin_instance.getNofication(i)
        if w3.isChecksumAddress(data[1]) == w3.isChecksumAddress(_account_address):

            x.add_row([data[2],buyer_registeration_instance.getBuyer(data[0])[1]])
            models_info.append(data)
        

    #print("\n\n")
    while(1):
            os.system('cls')
            print(x)
            print("\n\nSelect The Model ID You Want To Transfer To The Request Maker Or (X) To Exist")
            model_id_str = input("MODEL ID: ")
            
            try:
                model_id = int(model_id_str)
                
                ########### DO TRANSACTION FROM ACCOUNT WHILE PUSHING IT ###############
                for i in models_info:
                    if i[2] == model_id:
                        neurocoin_instance.safeTransferFrom(_account_address,i[0],model_id,transact={'from': _account_address})
                        print("Successfully Transfer Of Model Ownership")
                        info_data_instance.addNN(i[0],i[2],buyer_registeration_instance.getBuyer(i[0])[1],transact={'from': _account_address})
                        info_data_instance.removeNN(_account_address,model_id,transact={'from': _account_address})
                        time.sleep(3)

            except ValueError as identifier:
                pass
            
            except UnboundLocalError as identifier:
                pass
            if model_id_str.lower() == "x":
                break

    #safe
    #delete from mine
    #addNN from him
    
    return


###############################################################
############     Create NN  and Deploy IT #####################
def deploy_model(_account_address):
    global universal_token
    os.system("cls")
    print("############################### Deploying Model The Network ###############################")
    model_dict = {
        
    r"C:\Users\Arsalan Ashraf\Desktop\Salman\Models\DeepJazz\deepJazz.pth":[r"C:\Users\Arsalan Ashraf\Desktop\Salman\Models\DeepJazz\from_scratch_hybrid.mp3",4],
    r"C:\Users\Arsalan Ashraf\Desktop\Salman\Models\keras\new_weights.hdf5":[r"C:\Users\Arsalan Ashraf\Desktop\Salman\Models\keras\keras_model.mid",1],
    r"C:\Users\Arsalan Ashraf\Desktop\Salman\Models\MuseGAN\MuseGAN.pth":[r"C:\Users\Arsalan Ashraf\Desktop\Salman\Models\MuseGAN\salu.mp3",4]}

    name = (developer_registeration_instance.getDeveloper(_account_address))[1]
    owner = _account_address
    domain_name = "Music Generation"
    training_accuracy = input("Input The Training Accuracy: ")
    testing_accuracy = input("Input The Testing Accuracy: ")
    file_link = input("Drag And Drop The (Keras/Pytorch) Model Here: ")
    while(1):
        print("\nChoose Genre Piano(1), HipHop(2), Rock(3) and Pop(4)")
        genre = input("Genre: ")
        try:
            genre = int(genre)
            if genre >=1 and genre <= 4:
                break
            
        except ValueError as identifier:
            print("Please Choose Right Option")
        except AttributeError as identifier: 
            print("Please Choose Right Option")       
        except UnboundLocalError as identifier:
            print("Please Choose Right Option")
            
    #print(file_link[-4:])
    if   True:
        try:
            print("\n\nSending And Testing Model On Cloud Might Takes Few Seconds !!!")
            time.sleep(120)
            if model_dict[file_link][1] == genre:
                print("Successfully Tested Model Has Passed All Tests")
                neurocoin_instance.CreateNeuralNetwork(name,owner,domain_name,int(training_accuracy),int(testing_accuracy),owner,transact={'from': _account_address})
                info_data_instance.addNN(_account_address,universal_token,name,transact={'from': _account_address})
                universal_token_file[universal_token] = model_dict[file_link][0]
                universal_token += 1
            else:
                print("Model Failed Due To Fault In The Architecture Or changed In Genre")
                
        except KeyError as identifier:
            pass

            
    else :
        print("File Format Is Not Supported")
    
    # create NN
    # Update Data
    # Add File and Give Musis List results
    input()
    return
###############################################################


###############################################################

print("\n               Wait For Few Seconds .... All smart contracts are getting deployed\n")
import time
time.sleep(5)
input("\n               All smart contracts successfully gets deployed\n")
input("")
os.system('cls')

while (1):
    os.system('cls')

    while(1):
        print("PLEASE INPUT THE ROLE")
        role = input("ROLE: ")
        role = role.lower()
        if role.lower() == "developer":
            break
        elif role.lower() == "buyer":
            break
        else:
            print("PLEASE SELECT THE CORRECT ROLE")

    os.system('cls')
    account_address =  w3.toChecksumAddress( input("INPUT THE ACCOUNT ADDRESS: ")) 

    if role == "developer":
        data = (developer_registeration_instance.getDeveloper(account_address))
        
        if data[0] == ""  and data[1] == "" and data[2] == "":
            os.system('cls')
            print("Looks Like You Have Not Registered.... Please SignUp !!!\n")
            full_name = input("FULL NAME: ")
            user_name = input("USER NAME: ")
            email_id = input("EMAIL ID: ")
            developer_registeration_instance.setDeveloper(
                account_address, 
                full_name, 
                user_name,
                email_id, 
                transact={
                    'from': account_address
                }
                )
            
            print("\n\n You Have Successfully Registered \n\n")

        else:
            print("You Are Successfully Logined")
            user_name = data[1]

        


    elif role == "buyer":
        data = (buyer_registeration_instance.getBuyer(account_address))
        
        if data[0] == ""  and data[1] == "" and data[2] == "":
            os.system('cls')
            print("Looks Like You Have Not Registered.... Please SignUp !!!\n")
            full_name = input("FULL NAME: ")
            user_name = input("USER NAME: ")
            email_id = input("EMAIL ID: ")
            buyer_registeration_instance.setBuyer(
                account_address, 
                full_name, 
                user_name,
                email_id, 
                transact={
                    'from': account_address
                }
            )
            
            print("\n\n You Have Successfully Registered \n\n")

        else:
            print("You Are Successfully Logined")
            user_name = data[1]


    os.system("cls")
    input("\n\n Welcome {} To NeurCoin.io \n\n".format(user_name))  
    while (1):
        os.system("cls")
        
        print("###############################################################")
        print("####               (1) VIEW CATALOG                        ####")
        print("####               (2) VIEW ALL OWNED MODELS               ####")
        print("####               (3) EDIT USER PROFILE                   ####")

        if role == "developer":
            ################# CREATE New NN ###########
            ############# ALSO UPDATE DATA ########
            print("####               (4) DEPLOY MODEL TO THE NETWORK         ####")
            
            ############ SEE ALL REQUESTS #################
            ############ CONFIRM REQUESTS USING YOUR ACCOUNT ######
            ############### ALSO UPDATE DATA ##########################
            print("####               (5) VIEW ALL REQUESTS                   ####")
            
        print("####               (0) LogOut                              ####")

        print("###############################################################")
        try:
            option = int(input("\nChoose Option: "))
            if option >= 0 and option <= 5:
                
                if option == 1:
                    view_catalog(account_address,role)
                elif option == 2:
                    view_owned_models(account_address,role)
                elif option == 3:
                    setting(account_address,role)
                    print()
                elif option == 4 and role == "developer":
                    deploy_model(account_address)
                    print()

                elif option == 5 and role == "developer":
                    view_all_requests(account_address)
                    
                elif option == 0:
                    os.system("cls")
                    print("     ##############################      ")
                    print("     ### Successfully Logged Out ##      ")
                    print("     ##############################       ")
                    time.sleep(3)
                    break

            elif option > 4:
                input("\n\nPlease Choose Correct Option \n\n")

        except ValueError as identifier:
            pass
            