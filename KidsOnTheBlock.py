import leveldb
import binascii

dbPath = "geth_data_dir/geth/chaindata"
db = leveldb.LevelDB(dbPath)

# Python script to dump the content of a leveldb on standard output
# https://gist.github.com/msegura/7a676b76eb7ba1ac6ee1f312445ac64a
for k, v in list(db.RangeIter(key_from=None, key_to=None)):
    print(f"key: {binascii.hexlify(k)}")
    print(f"val: {binascii.hexlify(k)}\n")

# https://ethereum.stackexchange.com/questions/10548/what-does-every-field-in-block-means

# geth console --datadir . --nodiscover
# eth.getBalance("0xb4ba4b90df51d42a7c6093e92e1c7d22874c14f2")
# eth.blockNumber

# https://web3js.readthedocs.io/en/v1.2.0/web3-eth.html#getbalance
# web3.eth.getBalance(address [, defaultBlock] [, callback])

# https://github.com/ethereum/wiki/wiki/JavaScript-API#web3ethgettransactioncount
# web3.eth.getTransactionCount(addressHexString [, defaultBlock] [, callback])

# https://ethereum.stackexchange.com/questions/2531/common-useful-javascript-snippets-for-geth/3478#3478

====================
function gtba(myaccount) {  
  startBlockNumber = 0
  endBlockNumber = 62
  console.log("Searching for transactions to/from account \"" + myaccount + "\" within blocks "  + startBlockNumber + " and " + endBlockNumber);

  for (var i = startBlockNumber; i <= endBlockNumber; i++) {
    console.log("Searching block " + i);
    var block = eth.getBlock(i, true);
    if (block != null && block.transactions != null) {
      block.transactions.forEach( function(e) {
        if (myaccount == "*" || myaccount == e.from) {
          console.log("\n  tx hash          : " + e.hash + "\n"
            + "   nonce           : " + e.nonce + "\n"
            + "   blockHash       : " + e.blockHash + "\n"
            + "   blockNumber     : " + e.blockNumber + "\n"
            + "   transactionIndex: " + e.transactionIndex + "\n"
            + "   from            : " + e.from + "\n" 
            + "   to              : " + e.to + "\n"
            + "   value           : " + (e.value/1000000000000000000) + "\n"
            + "   time            : " + block.timestamp + "\n"
            + "   gasPrice        : " + e.gasPrice + "\n"
            + "   gas             : " + e.gas + "\n"
            + "   input           : " + e.input);
        }
      })
    }
  }
}

tx: 0x8fbf818cf1ebf1c319aa970c2a2f7e9718169a724b79504d4f0051a48118c42f
gtba("0xb4ba4b90df51d42a7c6093e92e1c7d22874c14f2") 2.5

gtba("0xae5165d3d0c9aa682557fe964c6da645b84e9e1d") 2.5
gtba("0xf387f84b74e05416679ebbdbc79b509f7f2caa47") 2.5
gtba("0x3ec2a3d11e177ea8bff7d6cd9df360ebcc52d584") 1.25 1.25 to same address
gtba("0x4da56f7f58bc14c785cee861d25b2c417fe6853f") 2.5 1571618645
gtba("0x167f7969ae2ecf157306f798f63929903a02d771") 2.5

# https://ethereum.stackexchange.com/questions/1871/how-to-find-contracts-address
web3.eth.getTransactionReceipt('0x8fbf818cf1ebf1c319aa970c2a2f7e9718169a724b79504d4f0051a48118c42f')