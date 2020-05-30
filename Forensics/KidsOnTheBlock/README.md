# Kids on the Block

## Forensics: 400 points

## Solve
Help! I was ransomwared and payed the ransom. Now I want to track my coins down and [find the culprit][1].

## Hints
* You can access transactions pragmatically with geth's javascript API
* All ransom transactions will move the ransom value or a logical fraction of it (such as a half or a fourth)
* Contracts take arguments from the transaction input data

## Webpage: Find the Culprit 

[challenge.acictf.com:10132/][1]

![webpage][6]

**The interesting pieces are:**

> I am giving you a copy of a Ethereum blockchain. [You can download it here][2]. Your task is to find the path of blockchain addresses which the **2.5** Ethereum followed, starting at `0xb4ba4b90df51d42a7c6093e92e1c7d22874c14f2`. Each address in this list is where the **2.5** Ethereum was placed.

> Note: Make sure to include contract addresses. Only include a contract address once if multiple operations were performed on it in a row. ([Here is the source of a contract on the chain][3])

## Solution
Untar the blockchain file. This unpacks all files into the **geth_data_dir**:
```
$ tar -xvf chain.tar.gz
```

Install [geth][4]:
```
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install ethereum
```

Geth's `--datadir` option allows a local geth_data_dir directory to be used. The `--preload` option allows JavaScript code to be loaded into geth. Run geth with the following options:
```
$ geth console --datadir ./geth_data_dir --nodiscover --preload KidsOnTheBlock.js
```

Get a feel for the eth console. Try `eth.blockNumber` or `eth.getBlock(1)`. The different eth commands are essential for the preloaded scripts.
```javascript
> eth.blockNumber
62
> eth.getBlock(0)
{
  difficulty: 1024,
  extraData: "0x00",
  gasLimit: 4294967295,
  gasUsed: 0,
  hash: "0x5342cca904e1613917a0689e67e7aa0588729287cca17bd3b7df96593441c86a",
  logsBloom: "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
  miner: "0x3333333333333333333333333333333333333333",
  mixHash: "0x0000000000000000000000000000000000000000000000000000000000000000",
  nonce: "0x0000000000000000",
  number: 0,
  parentHash: "0x0000000000000000000000000000000000000000000000000000000000000000",
  receiptsRoot: "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
  sha3Uncles: "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
  size: 507,
  stateRoot: "0x46b1493a695d12c8211de58a5f08f731d6212e5da8713de5b9915ddc062460d4",
  timestamp: 0,
  totalDifficulty: 1024,
  transactions: [],
  transactionsRoot: "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
  uncles: []
}
```

The [KidsOnTheBlock.js][5] script has a `getAllTransactions` function. It loops through all known blocks and gets every single transaction and prints it to the console. The `gtba()` function stands for Get Transaction By Account. It gets all transactions to/from a specified account. Trace the **2.5** eth via the `gtba()` function:
```
> gtba("0xb4ba4b90df51d42a7c6093e92e1c7d22874c14f2")
Searching for transactions to/from account "0xb4ba4b90df51d42a7c6093e92e1c7d22874c14f2" within blocks 0 and 62

  tx hash          : 0x8fbf818cf1ebf1c319aa970c2a2f7e9718169a724b79504d4f0051a48118c42f
   nonce           : 0
   blockHash       : 0xe117fa8d2405ca3fbf7682bc0be8db74472aa3c8ab4f72d8f5218b83349a0344
   blockNumber     : 2
   transactionIndex: 1
   from            : 0xb4ba4b90df51d42a7c6093e92e1c7d22874c14f2
   to              : 0xae5165d3d0c9aa682557fe964c6da645b84e9e1d
   value           : 2500000000000000000
   time            : 1571618183
   gasPrice        : 1000000000
   gas             : 21000
   input           : 0x
```

Note that the **value** property is shown in the unit [wei][7]. One ether is worth 1e18 wei (1,000,000,000,000,000,000 wei). Therefore, the value shown is equal to 2.5 eth.

The eth is now at address `0xae5165d3d0c9aa682557fe964c6da645b84e9e1d`. Trace the eth to the 3rd address:
```
> gtba("0xae5165d3d0c9aa682557fe964c6da645b84e9e1d")
...
from            : 0xae5165d3d0c9aa682557fe964c6da645b84e9e1d
to              : 0xf387f84b74e05416679ebbdbc79b509f7f2caa47
value           : 2500000000000000000
...
```

Trace to the 4th address:
```
> gtba("0xf387f84b74e05416679ebbdbc79b509f7f2caa47")
...
from            : 0xf387f84b74e05416679ebbdbc79b509f7f2caa47
to              : 0x3ec2a3d11e177ea8bff7d6cd9df360ebcc52d584
value           : 2500000000000000000
...
```

Trace to the 5th address. This time the 2.5 eth was sent via two transactions in 1.25 eth increments to the same destination address:
```
> gtba("0x3ec2a3d11e177ea8bff7d6cd9df360ebcc52d584")
...
from            : 0x3ec2a3d11e177ea8bff7d6cd9df360ebcc52d584
to              : 0x4da56f7f58bc14c785cee861d25b2c417fe6853f
value           : 1250000000000000000
...
from            : 0x3ec2a3d11e177ea8bff7d6cd9df360ebcc52d584
to              : 0x4da56f7f58bc14c785cee861d25b2c417fe6853f
value           : 1250000000000000000
...
```

Trace to the 6th address:
```
> gtba("0x4da56f7f58bc14c785cee861d25b2c417fe6853f")
...
from            : 0x4da56f7f58bc14c785cee861d25b2c417fe6853f
to              : 0x167f7969ae2ecf157306f798f63929903a02d771
value           : 2500000000000000000
...
```

Trace to the 7th address. This time there are no transactions going from this account. However, address `0x4da56f7f58bc14c785cee861d25b2c417fe6853f` did sent a value of `0` to `0x167f7969ae2ecf157306f798f63929903a02d771`. This transactions needs further investigation.
```
> gtba("0x167f7969ae2ecf157306f798f63929903a02d771")
...
tx hash         : 0xf678663343298496dcb73f77c0500ec1f19ec94554a73b5495c651e3dc1e2629
nonce           : 5
blockHash       : 0xd7d938fcefbe821e1ed20b9a96b91e3e9efae9bbe637a1df9ca41d51a9fd1868
blockNumber     : 60
transactionIndex: 4
from            : 0x4da56f7f58bc14c785cee861d25b2c417fe6853f
to              : 0x167f7969ae2ecf157306f798f63929903a02d771
value           : 0
time            : 1571618764
gasPrice        : 1000000000
gas             : 3000000
input           : 0xf3fef3a300000000000000000000000050fc67693f00fbabc5473c3705ef057b09acf2c700000000000000000000000000000000000000000000000022b1c8c1227a0000
```

Look at the input of this transaction. It seems to contain three distinct pieces of information:
```
var0: f3fef3a3
var1: 00000000000000000000000050fc67693f00fbabc5473c3705ef057b09acf2c7
var2: 00000000000000000000000000000000000000000000000022b1c8c1227a0000
```

The variable `var2` equals the correct amount of eth when converted from hex to decimal:
```
0x22b1c8c1227a0000 = 2500000000000000000 decimal
```

The variable `var1` contains a value that is exactly the same length as an address:
```
6th address: 0x4da56f7f58bc14c785cee861d25b2c417fe6853f
var1:        0x50fc67693f00fbabc5473c3705ef057b09acf2c7
```
The `var1` address must be the 7th address. Check if there are any outgoing transactions from this address: `gtba("0x50fc67693f00fbabc5473c3705ef057b09acf2c7")`. There are none. This must be the final address.

To investigate further, get block number 1. The transaction below has a `to` value set to `null` indicating that this is a contract creation transaction.
```
> eth.getBlock(1, true)
...
blockHash: "0x05ab4b4fedb9b337045bac03f4de35401b236f2693b54d9775b7dae67b68a411",
blockNumber: 1,
from: "0x9701026391e8e0474c9a90f261be9efc3beb531d",
gas: 4700000,
gasPrice: 1000000000,
hash: "0x9127400d214d99183f56398334c02f0877b795e676f411fc3b9b77045970db29",
input: "0x6060604052341561000c57fe5b5b6102658061001c6000396000f30060606040526000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806312065fe014610051578063d0e30db014610077578063f3fef3a314610081575bfe5b341561005957fe5b6100616100c0565b6040518082815260200191505060405180910390f35b61007f610108565b005b341561008957fe5b6100be600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091908035906020019091905050610158565b005b6000600060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205490505b90565b34600060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055505b565b80600060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054101515156101a75760006000fd5b80600060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825403925050819055508173ffffffffffffffffffffffffffffffffffffffff166108fc829081150290604051809050600060405180830381858888f19350505050151561023457fe5b5b50505600a165627a7a72305820b81b4c88732e81c9348003df1a2cda8514646894b71981ae7efd91061bfb2c860029",
nonce: 0,
r: "0xcbfb246d624155e6ff05c7633aaaefdc92deb44fc6f339e4c7c6d5b2570847ff",
s: "0x406c319452dde5faa2ed947d4d08643c64c0a784df1665ced5af29fe21aab256",
to: null,
transactionIndex: 19,
v: "0xac",
value: 0
...
```

Copy the `input` and paste into https://ethervm.io/decompile. At first it will result in an error:

> This might be constructor bytecode - to get at the deployed contract, go back and remove the constructor prefix, usually up to the next 6060 or 6080.

Follow the instruction and remove the constructor prefix up to `6060` or `6080`:
```
Remove this:
0x6060604052341561000c57fe5b5b6102658061001c6000396000f300

Paste this:
60606040526000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806312065fe014610051578063d0e30db014610077578063f3fef3a314610081575bfe5b341561005957fe5b6100616100c0565b6040518082815260200191505060405180910390f35b61007f610108565b005b341561008957fe5b6100be600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091908035906020019091905050610158565b005b6000600060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205490505b90565b34600060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825401925050819055505b565b80600060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054101515156101a75760006000fd5b80600060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825403925050819055508173ffffffffffffffffffffffffffffffffffffffff166108fc829081150290604051809050600060405180830381858888f19350505050151561023457fe5b5b50505600a165627a7a72305820b81b4c88732e81c9348003df1a2cda8514646894b71981ae7efd91061bfb2c860029
```

View the full decompiled contract [here][8]. Look at the last else statement in the main function:
```javascript
else if (var0 == 0xf3fef3a3) {
    // Dispatch table entry for withdraw(address,uint256)
    if (msg.value) { assert(); }

    var1 = 0x00be;
    var var2 = msg.data[0x04:0x24] & 0xffffffffffffffffffffffffffffffffffffffff;
    var var3 = msg.data[0x24:0x44];
    withdraw(var2, var3);
    stop();
}
```
The hex value `0xf3fef3a3` matches `var0` from the contract transaction to the 7th address. This else statement also calls the withdraw function, which will send an amount to the address given via the input. Ethervm further confirms this by listing the following:
```
Public Methods
0x12065fe0 getBalance()
0xd0e30db0 deposit()
0xf3fef3a3 withdraw(address,uint256)
```

To sum up, the ransomed eth hopped between the following addresses:
```
1. 0xb4ba4b90df51d42a7c6093e92e1c7d22874c14f2
2. 0xae5165d3d0c9aa682557fe964c6da645b84e9e1d
3. 0xf387f84b74e05416679ebbdbc79b509f7f2caa47
4. 0x3ec2a3d11e177ea8bff7d6cd9df360ebcc52d584
5. 0x4da56f7f58bc14c785cee861d25b2c417fe6853f
6. 0x167f7969ae2ecf157306f798f63929903a02d771
7. 0x50fc67693f00fbabc5473c3705ef057b09acf2c7
```

## Resources
* [Install Geth][4]
* [What is Ether: Denominations][7]
* [What does every block field mean?][9]
* https://web3js.readthedocs.io/en/v1.2.0/web3-eth.html#getbalance
* https://github.com/ethereum/wiki/wiki/JavaScript-API#web3ethgettransactioncount
* https://ethereum.stackexchange.com/a/3478/60341
* https://ethereum.stackexchange.com/questions/1871/how-to-find-contracts-address
* https://geth.ethereum.org/docs/interface/javascript-console
* https://medium.com/@codetractio/inside-an-ethereum-transaction-fa94ffca912f


[1]:http://challenge.acictf.com:10132/
[2]:chain.tar.gz
[3]:wallet.sol
[4]:https://geth.ethereum.org/docs/install-and-build/installing-geth#install-on-ubuntu-via-ppas
[5]:KidsOnTheBlock.js
[6]:webpage.png
[7]:https://ethdocs.org/en/latest/ether.html
[8]:decompiled.js
[9]:https://ethereum.stackexchange.com/questions/10548/what-does-every-field-in-block-means