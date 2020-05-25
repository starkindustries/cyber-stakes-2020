# Not So Meta

## Forensics: 50 points

## Solve

Look, it's the flag! Oh wait...it looks like we need to take a closer look... [not\_so\_meta.jpg](./not\_so\_meta.jpg)

## Hints

* How do images keep contextual information when they're created? (e.g., GPS data, creation timestamp, etc.)
* How do you [encode](https://en.wikipedia.org/wiki/Base64) binary data into common ASCII characters?

## Solution

Starting off with hexdump, we can see that there is some exif data stored in the jpg file.
```
hexdump -C not_so_meta.jpg > not_so_meta_hex.txt
```
Use the `strings` command to view just the ascii bytes:
```
$ strings -n 64 not_so_meta.jpg > not_so_meta.txt
<x:xmpmeta xmlns:x='adobe:ns:meta/' x:xmptk='Image::ExifTool 10.80'>
<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  xmlns:mwg-rs='http://www.metadataworkinggroup.com/schemas/regions/'
  <xmp:ItsTheFlag>QUNJezhhM2E0OWJjZWUxM2MzZGNlYzE4MGQzNDgxZX0=</xmp:ItsTheFlag>
```

One line is particularly interesting:
```
<xmp:ItsTheFlag>QUNJezhhM2E0OWJjZWUxM2MzZGNlYzE4MGQzNDgxZX0=</xmp:ItsTheFlag>
```

The flag is shown as a base64 string. Convert it to ascii to get the real flag.