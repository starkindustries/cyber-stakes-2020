# Proxy List

## Miscellaneous: 100 points

## Solve

We need you to perform geolocation analysis on this list of IPs. We have attributed it to a malicious proxy network. Report back with the prevalent country of origin: [ips.txt](./ips.txt)

## Hints

* The flag is the name of the origin country (case-sensitive) found most frequently in the list
* Offline geolocation IP analysis can be scripted with a python package or two
* These IPs were collected in late 2019, if necessary you may need to use 'historical' geolocation data

## Solution
Install the **geoip2** python library:
```
$ pip3 install geoip2
```
Download the GeoLite2-Country.mmdb database file from maxmind:
https://www.maxmind.com/en/accounts/290137/geoip/downloads

Take a look at the [database example code][1] for geoip2:

```
>>> import geoip2.database
>>>
>>> # This creates a Reader object. You should use the same object
>>> # across multiple requests as creation of it is expensive.
>>> reader = geoip2.database.Reader('/path/to/GeoLite2-City.mmdb')
>>>
>>> # Replace "city" with the method corresponding to the database
>>> # that you are using, e.g., "country".
>>> response = reader.city('128.101.101.101')
>>>
>>> response.country.iso_code
'US'
>>> response.country.name
'United States'
>>> response.country.names['zh-CN']
u'美国'
>>>
>>> response.subdivisions.most_specific.name
'Minnesota'
>>> response.subdivisions.most_specific.iso_code
'MN'
>>>
>>> response.city.name
'Minneapolis'
>>>
>>> response.postal.code
'55455'
>>>
>>> response.location.latitude
44.9733
>>> response.location.longitude
-93.2323
>>>
>>> response.traits.network
IPv4Network('128.101.101.0/24')
>>>
>>> reader.close()
```
This sample code provides everything needed to create a python script that will tally up IP locations. 

The script [ProxyList.py](./ProxyList.py) loops through each IP in the text file, finds the IP's country in the database, and increments that country's counter. The [output](./output.txt) of the script reveals the most frequent country.

```
Most frequent country: ('Brazil', 2400)
Flag: ACI{Brazil}
```

[1]:https://geoip2.readthedocs.io/en/latest/