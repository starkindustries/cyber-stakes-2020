File npp.exe has a Start at offset 001F 6400

$ vbindiff file1 file2
$ cmp -l npp.6.8.7.bin.minimalist/npp.exe official.npp.6.8.7.bin.minimalist/notepad++.exe 
$ dd if=npp.6.8.7.bin.minimalist/npp.exe skip=2057216 bs=1 count=455 of=npp-chunk
$ xxd npp-chunk 
$ file npp-chunk 
