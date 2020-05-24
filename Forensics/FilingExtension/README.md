# Filing Extension

## Forensics: 10 points

## Description

We went to apply for a tax-filing extension with the IRS, and they replied with this image saying it contained the code we needed. Unfortunately, our computer refuses to display it and just says that it isn't a PNG... [flag.png](./flag.png)

## Hints

* Is the extension the only way to tell a file's type?
* Wouldn't it be awesome if there was a [list](https://en.wikipedia.org/wiki/List_of_file_signatures) of way to identify files.


## Solution

Find the file type:

```
$ file flag.png
flag.png: Zip archive data, at least v2.0 to extract
```

It is a zip file. Unzip:

```
$ unzip flag.png
Archive:  flag.png
  inflating: flag.txt
```

Print flag contents:
```
$ cat flag.txt
ACI{Something_witty_92adc6d7}
```