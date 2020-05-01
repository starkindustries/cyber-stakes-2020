function getAllTransactions() {
    var count = 0;
    for (var i = 0; i <= 62; i++) {
        var block = eth.getBlock(i, true);
        // Check for empty block or empty transactions
        if (block == null || block.transactions == null) {
            continue;
        }
        block.transactions.forEach(function (e) {
            count += 1;
            console.log("\n  tx hash          : " + e.hash + "\n"
                + "   nonce           : " + e.nonce + "\n"
                + "   blockHash       : " + e.blockHash + "\n"
                + "   blockNumber     : " + e.blockNumber + "\n"
                + "   transactionIndex: " + e.transactionIndex + "\n"
                + "   from            : " + e.from + "\n"
                + "   to              : " + e.to + "\n"
                + "   value           : " + (e.value / 1000000000000000000) + "\n"
                + "   time            : " + block.timestamp + "\n"
                + "   gasPrice        : " + e.gasPrice + "\n"
                + "   gas             : " + e.gas + "\n"
                + "   input           : " + e.input);
        });
    }
    console.log("Tx count: " + count);
}

// getTransactionsByAccount = gtba
function gtba(myaccount) {
    startBlockNumber = 0
    endBlockNumber = 62
    console.log("Searching for transactions to/from account \"" + myaccount + "\" within blocks " + startBlockNumber + " and " + endBlockNumber);

    for (var i = startBlockNumber; i <= endBlockNumber; i++) {
        var block = eth.getBlock(i, true);
        if (block != null && block.transactions != null) {
            block.transactions.forEach(function (e) {
                if (myaccount == "*" || myaccount == e.from || myaccount == e.to) {
                    console.log("\n  tx hash          : " + e.hash + "\n"
                        + "   nonce           : " + e.nonce + "\n"
                        + "   blockHash       : " + e.blockHash + "\n"
                        + "   blockNumber     : " + e.blockNumber + "\n"
                        + "   transactionIndex: " + e.transactionIndex + "\n"
                        + "   from            : " + e.from + "\n"
                        + "   to              : " + e.to + "\n"
                        + "   value           : " + (e.value / 1000000000000000000) + "\n"
                        + "   time            : " + block.timestamp + "\n"
                        + "   gasPrice        : " + e.gasPrice + "\n"
                        + "   gas             : " + e.gas + "\n"
                        + "   input           : " + e.input);
                }
            })
        }
    }
}

function findContract() {
    startBlockNumber = 0
    endBlockNumber = 62
    for (var i = startBlockNumber; i <= endBlockNumber; i++) {
        var block = eth.getBlock(i, true);
        // Check for empty block or empty transactions
        if (block == null || block.transactions == null) {
            continue;
        }
        block.transactions.forEach(function (e) {
            r = eth.getTransactionReceipt(e.hash);
            if (r.contractAddress != null) {
                console.log("Found contract " + r.contractAddress + " for transaction " + e.hash);
            }
        });
    }
}

// https://ethereum.stackexchange.com/questions/10548/what-does-every-field-in-block-means

// geth console --datadir ./geth_data_dir --nodiscover --preload KidsOnTheBlock.js
// > eth.getBalance("0xb4ba4b90df51d42a7c6093e92e1c7d22874c14f2")
// > eth.blockNumber

// https://web3js.readthedocs.io/en/v1.2.0/web3-eth.html#getbalance
// web3.eth.getBalance(address [, defaultBlock] [, callback])

// https://github.com/ethereum/wiki/wiki/JavaScript-API#web3ethgettransactioncount
// web3.eth.getTransactionCount(addressHexString [, defaultBlock] [, callback])

// https://ethereum.stackexchange.com/questions/2531/common-useful-javascript-snippets-for-geth/3478#3478

// gtba("0xb4ba4b90df51d42a7c6093e92e1c7d22874c14f2") 2.5
// gtba("0xae5165d3d0c9aa682557fe964c6da645b84e9e1d") 2.5
// gtba("0xf387f84b74e05416679ebbdbc79b509f7f2caa47") 2.5
// gtba("0x3ec2a3d11e177ea8bff7d6cd9df360ebcc52d584") 1.25 1.25 to same address
// gtba("0x4da56f7f58bc14c785cee861d25b2c417fe6853f") 2.5 1571618645
// gtba("0x167f7969ae2ecf157306f798f63929903a02d771") 2.5

// https://ethereum.stackexchange.com/questions/1871/how-to-find-contracts-address
// ====================
// tx hash         : 0x8fbf818cf1ebf1c319aa970c2a2f7e9718169a724b79504d4f0051a48118c42f
// nonce           : 0
// blockHash       : 0xe117fa8d2405ca3fbf7682bc0be8db74472aa3c8ab4f72d8f5218b83349a0344
// blockNumber     : 2
// transactionIndex: 1
// from            : 0xb4ba4b90df51d42a7c6093e92e1c7d22874c14f2
// to              : 0xae5165d3d0c9aa682557fe964c6da645b84e9e1d
// value           : 2.5
// time            : 1571618183
// gasPrice        : 1000000000
// gas             : 21000
// input           : 0x
// ====================
// tx hash         : 0x836dfec2f9e6ea6b7a98ce3e2775f8125b56389461602b5fbc087a8dd300eee0
// nonce           : 1
// blockHash       : 0x538f41f36b25efe8337d0ebe84a9a64e8e3a42c36f13c5970f3b0ba118bf2972
// blockNumber     : 17
// transactionIndex: 2
// from            : 0xae5165d3d0c9aa682557fe964c6da645b84e9e1d
// to              : 0xf387f84b74e05416679ebbdbc79b509f7f2caa47
// value           : 2.5
// time            : 1571618300
// gasPrice        : 1000000000
// gas             : 21000
// input           : 0x
// ====================
// tx hash         : 0x4f05a8f1f86c982f254d7f483fb2bd8593f81c6e275375e17744380c98822e73
// nonce           : 1
// blockHash       : 0x7b919de4e05b3af17a66f5e3ff65b7a12a70bd647b4f093c9c127b0f3a5fcfc6
// blockNumber     : 23
// transactionIndex: 3
// from            : 0xf387f84b74e05416679ebbdbc79b509f7f2caa47
// to              : 0x3ec2a3d11e177ea8bff7d6cd9df360ebcc52d584
// value           : 2.5
// time            : 1571618371
// gasPrice        : 1000000000
// gas             : 21000
// input           : 0x
// ====================
// tx hash         : 0x7c75c823b8f7d05866d934a9f0c6f50132f8c8406dd906ad0ef32f4bf79e7427
// nonce           : 0
// blockHash       : 0x7f3bc5444ef2817dfffa47054fd7a80f0a022c5240c2f5e6b4ef1b62c3f4cd7d
// blockNumber     : 35
// transactionIndex: 0
// from            : 0x3ec2a3d11e177ea8bff7d6cd9df360ebcc52d584
// to              : 0x4da56f7f58bc14c785cee861d25b2c417fe6853f
// value           : 1.25
// time            : 1571618521
// gasPrice        : 1000000000
// gas             : 21000
// input           : 0x

// tx hash         : 0xfd6b0019cfcb7dff8bd39826b61b3a356f7e78f3937db0e6e08f8303a5873450
// nonce           : 1
// blockHash       : 0x4186c468e404e342cfc581cc5b3c5335e31aa81dedcdb7a877fb5142ba6d28e0
// blockNumber     : 40
// transactionIndex: 3
// from            : 0x3ec2a3d11e177ea8bff7d6cd9df360ebcc52d584
// to              : 0x4da56f7f58bc14c785cee861d25b2c417fe6853f
// value           : 1.25
// time            : 1571618562
// gasPrice        : 1000000000
// gas             : 21000
// input           : 0x
// ====================
// tx hash         : 0x09c0dd28b28cf223ac4ad093808dc4ffc0461f7a512b4a0c5a566d98205084b5
// nonce           : 4
// blockHash       : 0x4fa6e84b34e4362eec6596112c46801e521fbaeee1f334d08e1ec1c92e19fd6a
// blockNumber     : 48
// transactionIndex: 2
// from            : 0x4da56f7f58bc14c785cee861d25b2c417fe6853f
// to              : 0x167f7969ae2ecf157306f798f63929903a02d771
// value           : 2.5
// time            : 1571618645
// gasPrice        : 1000000000
// gas             : 3000000
// input           : 0xd0e30db0
// ====================

// eth.getTransactionReceipt("0x8fbf818cf1ebf1c319aa970c2a2f7e9718169a724b79504d4f0051a48118c42f")
// eth.getTransactionReceipt("0x836dfec2f9e6ea6b7a98ce3e2775f8125b56389461602b5fbc087a8dd300eee0")
// eth.getTransactionReceipt("0x4f05a8f1f86c982f254d7f483fb2bd8593f81c6e275375e17744380c98822e73")
// eth.getTransactionReceipt("0x7c75c823b8f7d05866d934a9f0c6f50132f8c8406dd906ad0ef32f4bf79e7427")
// eth.getTransactionReceipt("0xfd6b0019cfcb7dff8bd39826b61b3a356f7e78f3937db0e6e08f8303a5873450")
// eth.getTransactionReceipt("0x09c0dd28b28cf223ac4ad093808dc4ffc0461f7a512b4a0c5a566d98205084b5")

// Found contract 0x90acc1c268c67079b508a16271691c68285bd7e4 for transaction 0xfad6ae04e831ad9fff6a28577d24886aa76367269328bfe97887015361148ed3
// Found contract 0x2bd44a623242f81e748764f5ac9a78102e930aaf for transaction 0x6edcdd601dc87a19993d57c62a85d882d740e34c25efb64999268a1dd36b0f8f
// Found contract 0xfd28f51aa384748150da2700727cb11b42319372 for transaction 0x618ceb50141139a3c0b59eb0eed706b0d435bb5ff880bc5439fbe87603100941
// Found contract 0xb452f4d85e9bfe1efd825f7f6b40e2bbb3f4bf48 for transaction 0x7dd12c078903525e1a2d18a822fb9d0f84f96c88006522dec90158f11f352a16
// Found contract 0xb329341fb7dae66c7810bf550736eff6f29c35fd for transaction 0x8ebd8586e185a1d5da3468e234a9ea6306fb8cdf6c44beef6382ddc52987bb70
// Found contract 0xa52604352fbc6e42ee8aa0333ee43aef01823730 for transaction 0x8244775cd43cf99383f059a97b60eb501269aefe3332e4fd5a3549c91909e18e
// Found contract 0xaf0d9e9fadc102794d44a1d2d92e4f58089dadf0 for transaction 0x425e397e8efe4bad83fb0f91ebb8b5d5af973e7409d09a3ba57cb23f938bc5d9
// Found contract 0x622fb0a31c9699f0f81a36d67655f6ea3180efd3 for transaction 0x951aa13e7a33dabdc0278ac01e3b65f0cfd209e750b302255dd8fd6a333aa8ee
// Found contract 0x98851731b98595d3f93b8d908d4498968392dfe8 for transaction 0xb6e5ad0f4b186d4e31fcbb3b3bf7705ff2fa723c17fbe8b6edb316c5e9b236d7
// Found contract 0xbcd4c7db5491e0abd265ece94d1320b69fd4fd6f for transaction 0xf69586f27fc89f9d804b74738d09c8ee1c69b909fbabf99f17f490181dbba09f
// Found contract 0xfc1d12d9537ca4655515587dc9176a3e0cf5cadc for transaction 0xa4fe8857d88d3a0603e1d30ccca7b96ef077e5b9f3c57a5d0d6c95ccc941d656
// Found contract 0x49a1c6ae4330eddad4fc37d1f53e93d943a82e5d for transaction 0xdb9ad4ef1608fc7d91e71f649e61703826e3526c42b213ddcef7b0224b967c38
// Found contract 0xa4dde280610342d8d82a280c08a252fc93cdd99b for transaction 0x4915fc8708c26d384d06045494ae49fbdd68222a8ffbba4c0e54983236663398
// Found contract 0xd999cf2418dc2610415055eabf7f3fde8dc78e7a for transaction 0xc2a2f5a05e2cfe631afea80c59c53c0c197714a42457bbf4eecabb1c3d1258a2
// Found contract 0x2063a29a3bb5c056586d07736737591d25a5e3d1 for transaction 0x6dca8169946010c542fa2f894c7fd9191b08bc859370b10378c6b69654d0bb2b
// Found contract 0xf7445ad8a0cef1f1b1f01ebc6c2b2de6f95fc096 for transaction 0xbf41ad3cf0cb45c24c4475f139015d6516f4515e6631bc31a1ad7650edbf6922
// Found contract 0xe5f222c3e1594e3f3bcef7de3755a4c7acd55d29 for transaction 0x6ec7e516fbf5c1dd267c2490ff1ce0e57a751cbfb2594314a334cf0576faf849
// Found contract 0x167f7969ae2ecf157306f798f63929903a02d771 for transaction 0x5c5188b3978690f57af65426ea79c96ad47bc5e1cc974b53ab273f02d9ea5137
// Found contract 0xb060bf9ca6216c64d297b5bba04fa920b5154644 for transaction 0x6e9fc5cb9f0dd6256603d7a9d778ce7e49ce3c8b60a0626565726a4acbc0a177
// Found contract 0xd2458d392bb28b8af8f1299c330979b1da951baa for transaction 0x9127400d214d99183f56398334c02f0877b795e676f411fc3b9b77045970db29

// gtba("0xd999cf2418dc2610415055eabf7f3fde8dc78e7a")

// https://geth.ethereum.org/docs/interface/javascript-console
// It’s also possible to execute files to the JavaScript interpreter. The console and attach subcommand accept the --exec argument which is a javascript statement.
// geth attach /path/to/geth.ipc --exec "eth.blockNumber"

// geth console --datadir ./geth_data_dir/ --preload KidsOnTheBlock.js 

// Problem
// This command:
// geth attach ./geth_data_dir/geth.ipc --exec "getAllTransactions()"
// Produces this error: ReferenceError: getAllTransactions is not defined 
// Even though the instance of geth that is running is loaded with the js code: --preload ./KidsOnTheBlock.js

// Solution
// geth attach ./geth_data_dir/geth.ipc --exec 'loadScript("KidsOnTheBlock.js")' > transactions.txt
getAllTransactions();