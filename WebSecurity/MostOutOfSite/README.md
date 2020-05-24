# Most Out of Site

## Web Security: 20 points

## Solve

Alright, one more try. We had to think long and hard about how to keep you from viewing the flag. After a quick snack break, we had an epiphany. Your tricks won't work this time. http://challenge.acictf.com:35515/

## Hints

* What on earth could [snack food](https://en.wikipedia.org/wiki/HTTP_cookie) have to do with this problem?
* The browser must be storing these cookies somewhere...
* If you're getting tired of using a browser, the Python [Requests](https://requests.readthedocs.io/en/master/) library is pretty useful for interacting with web servers.


## Solution

In Chrome, right click and inspect the `input` element. 

```
<input type="text" id="flag" name="flag" placeholder="ACI{...}" oninput="check_flag()" required="">
```

Like the previous challenge (MoreOutOfSite), the `onInput` attribute calls the `check_flag()` function. In Chrome dev tools, click **Sources** then click on **flag_checker.js**. The `check_flag()` function contains a line to get the flag:

```
var secret_flag = get_cookie("most_out_of_site_flag");
```

Examine the `get_cookie(name)` function. It contains a call to `document.cookie`, which likely contains the flag.

Click the **Application** tab. Under the **Storage** section, click **Cookies**. Look for the cookie named `most_out_of_site_flag`. The flag is stored here.