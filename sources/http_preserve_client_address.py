class ClientIPHttpProxy(HttpProxy): # <1>
    def config(self): # <2>
        HttpProxy.config(self) # <3>
        self.request_header["X-Original-Ip"] = (HTTP_HDR_INSERT, self.session.client_address.ip_s) # <4>
