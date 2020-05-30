function logTransaction(e, block) {
    console.log(
        "\n  tx hash          : " + e.hash + "\n"
        + "   nonce           : " + e.nonce + "\n"
        + "   blockHash       : " + e.blockHash + "\n"
        + "   blockNumber     : " + e.blockNumber + "\n"
        + "   transactionIndex: " + e.transactionIndex + "\n"
        + "   from            : " + e.from + "\n"
        + "   to              : " + e.to + "\n"
        + "   value           : " + (e.value) + "\n"
        + "   time            : " + block.timestamp + "\n"
        + "   gasPrice        : " + e.gasPrice + "\n"
        + "   gas             : " + e.gas + "\n"
        + "   input           : " + e.input
    );
}

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
            logTransaction(e, block);
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
                    logTransaction(e, block);
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

// Dump all transactions to a text file
// $ geth attach ./geth_data_dir/geth.ipc --exec 'loadScript("KidsOnTheBlock.js")' > transactions.txt
getAllTransactions();