---
description: Intercepting basic web traffic
---

# 🅾 Red

### First Steps

We get a hint from the site telling us that the request to our web server could be modified to give interesting results. We can now view our requests in burp suite and craft our own requests to the server.

The solution then was pretty straight forward, we just needed to change our HTTP method to `HEAD` instead of `GET` or `POST.`As we see this gave us the following result

<figure><img src=".gitbook/assets/image (1).png" alt=""><figcaption><p>Flag in the HTTP response </p></figcaption></figure>
