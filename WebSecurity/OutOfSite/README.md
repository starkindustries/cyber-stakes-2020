# Out of Site

## Web Security: 5 points

## Solve

The flag submission system lets us see the strings you submitted even when they're wrong. Since some of you may consider that a privacy issue, we decided to demo a flag validation system that checks it client-side before sending the flag to us for checking. Why don't you give it a try: http://challenge.acictf.com:63225

## Hints

* How does your browser know what the right key is to do the check?
* If only there were a way to `control+U` the view of what the server sent you.


## Solution
Inspect page, find the `form` element. The flag is written in the `pattern` attribute of the `input` element.

```
<form action="check" method="post">
    <label for="flag"><b>Flag:</b></label>
    <input type="text" id="flag" name="flag" placeholder="ACI{...}" pattern="ACI{hidden_in_plain_site_ade8a282}" required="">
    <input type="submit">
</form>
```