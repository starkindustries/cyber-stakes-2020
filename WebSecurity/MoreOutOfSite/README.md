# More Out of Site

## Web Security: 10 points

## Solve

Well that was embarrassing... Who knew there was more to a web site then what the browser showed? Not to worry, we're back with a new and improved Javascript version! http://challenge.acictf.com:63225

## Hints

* The Javascript code in an `onInput` gets called anytime you interact with a text field.
* Is there anyway to view the Javascript definition of this function? It should just be text and your browser has it somewhere (it is running it after all).

## Solution

Inspect the page and examine the `input` element. Notice that the `onInput` attribute calls a function `check_flag()`.

```
<input type="text" id="flag" name="flag" placeholder="ACI{...}" onInput="check_flag()" required>
```

There is also a JavaScript file included, which likely contains the `check_flag()` function.
```
<script src="flag_checker.js"></script>
```

In Chrome dev tools, click **Sources**. Find and click **flag_checker.js** to examine the file. The `if` statement checks the input against the actual flag.

```
if (flag == "ACI{client_side_fail_845ce5f8}") {
    submit_button.disabled=false;
    status_field.innerHTML = "";
} else {
    submit_button.disabled=true;
    status_field.innerHTML = "error: does not match flag";
}
```