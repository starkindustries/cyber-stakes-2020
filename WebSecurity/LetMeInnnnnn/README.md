# Let me INNNNNN

## Web Security: 40 points

## Solve

Let's see if you can break into our secure vault. **WARNING**: This problem is currently disabled.

## Hints

How is the email determined for the password resending?

## Solution
Go to the Login page and inspect the login form. There is a hidden input with `id="email"` and `value="vault.master@cyberstakes.com"`. Change this email to your email and click **Resend password**. Check your email for the password. Enter the password and get the flag.