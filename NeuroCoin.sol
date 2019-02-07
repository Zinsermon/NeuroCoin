pragma solidity ^0.4.24;
import "./ERC721.sol";

contract NeuroCoin is ERC721 {
    
    struct NeuralNetwork{
        string name;
        address owner;
        string domainName;
        uint TrainingAccuracy;
        uint TestingAccuracy;
    }
    
    struct Requests{
        
        address fromAddress;
        address toAddress;
        uint tokenID;
    }
    Requests[] public allRequests;
    NeuralNetwork[] public NeuralNetworks;
    address public owner;
    
    function NeuroCoin() public{
        owner = msg.sender;
    }
    
    function pushNotification(address _fromAddress,uint _tokenID) {
        allRequests.push(Requests(_fromAddress, ownerOf(_tokenID),_tokenID
        )
    );
    }
    
    function getNotificationLength() view public returns (uint) { return uint(allRequests.length); }

    function getNofication(uint _index) view public returns (address,address,uint) {
        
        return (allRequests[_index].fromAddress,
        allRequests[_index].toAddress,
        allRequests[_index].tokenID);
    
    }
    
    function getLength() view public returns (uint) { return uint(NeuralNetworks.length); }
    
    function getValueOfModel   (uint _index)  view public returns (string, address, string, uint, uint) {
    
    return (NeuralNetworks[_index].name,
    NeuralNetworks[_index].owner,
    NeuralNetworks[_index].domainName,
    NeuralNetworks[_index].TrainingAccuracy,
    NeuralNetworks[_index].TestingAccuracy);   
    }
    
    function CreateNeuralNetwork(
        string _name,
        address _owner,
        string _domainName,
        uint _trainingAccuracy,
        uint _testingaccuracy,
        address _to
        ) public{
            
            uint id = NeuralNetworks.length;
            NeuralNetworks.push(
                NeuralNetwork(_name,_owner,_domainName,_trainingAccuracy,_testingaccuracy)
                );
                
            _mint(_to,id);
        }
}