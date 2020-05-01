import leveldb
import binascii

dbPath = "geth_data_dir/geth/chaindata"
db = leveldb.LevelDB(dbPath)

# Python script to dump the content of a leveldb on standard output
# https://gist.github.com/msegura/7a676b76eb7ba1ac6ee1f312445ac64a
for k, v in list(db.RangeIter(key_from=None, key_to=None)):
    print(f"key: {binascii.hexlify(k)}")
    print(f"val: {binascii.hexlify(k)}\n")