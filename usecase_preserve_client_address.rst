----------------------------
Preserve HTTP Client Address
----------------------------

.. index:: single: protocol;HTTP

Use case
========

Most common usage of a proxy firewall (or reverse proxy) for server protection is to control and inspect *HTTP* traffic. This is a simple example that shows how the traffic can be manipulated using *Zorp* and at the same time gives a solution to a relevant technical problem.
In case you cannot keep the client’s IP address for network topology reasons, debugging the web application will become almost impossible, as the web server will log all requests as tough it was coming from the firewall. It might not be possible to keep the IP address for various reasons, such as:

- you are using a load-balancer to divide the traffic between several firewalls, so the server does not know to which firewall it should send reply packets if you are keeping the original client address

- the servers targeted by the user traffic have a default gateway other than the firewall

Solution
========

The application level solution of the problem is to instruct the firewall to take the original client address, insert it as a custom *HTTP* header into the request forwarded to the server and instruct the web server to log this header’s value as the client’s address. If you are using apache2, you can find help on how to achieve this here.

For implementing the above, you will need to define a new proxy class in your *Zorp* policy:


.. literalinclude:: sources/http_preserve_client_address.py
  :language: python

1. Creates a new Proxy class with ``HttpProxy`` as its parent, so that it inherits all the attributes, methods and functionality from the original proxy.
2. Overrides the ``config`` method of the original HttpProxy. This method is called on proxy startup, before any data exchange is performed and is used to set configuration parameters and other attributes of the proxy that influence its behavior.
3. Calls the ``config`` method of the parent proxy, to make sure that all the necessary initialization task are performed and all the config attributes are set properly.
4. This instructs *Zorp* to take a header called X-Original-Ip, insert it into the *HTTP* request (``HTTP_HDR_INSERT``), with the value of the original client’s IP address (``self.session.client_address.ip_s``)

Use the resulting proxy (by setting the proxy_class attribute) in the Service that handles the traffic in question, as described in the :ref:`usecase-access-control` section.

Result
======

The result is very simple. The traffic goes through the firewall, connects to the target server with its own IP address and the *HTTP* request includes the client’s original IP address in the ``X-Original-IP`` ``HTTP`` header.
