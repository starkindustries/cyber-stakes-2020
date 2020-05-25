# Proxy List - Points: 100

#!/usr/bin/python3
import geoip2.database
import pprint

ip = '128.101.101.101'
# This creates a Reader object. You should use the same object
# across multiple requests as creation of it is expensive.
reader = geoip2.database.Reader('GeoLite2-Country_20200421/GeoLite2-Country.mmdb')

# Replace "city" with the method corresponding to the database
# that you are using, e.g., "country".
response = reader.country(ip)

print(f"IP: {ip}")
print(f"ISO Code: {response.country.iso_code}")
print(f"Country: {response.country.name}")

countryCount = {}
with open('ips.txt') as file:
    for line in file:
        ip = line.strip()
        
        try: 
            response = reader.country(ip)
            country = response.country.name
        except Exception as e:
            print(f"Error {e}")
        
        if not country in countryCount:
            countryCount[country] = 1
        else:
            countryCount[country] += 1
reader.close()

print("\nCountries:")
sortedCountries = sorted(countryCount.items(), key=lambda item: item[1], reverse=True)
print(sortedCountries)
print(f"\nMost frequent country: {sortedCountries[0]}")
print(f"Flag: ACI{{{sortedCountries[0][0]}}}")