from jinja2 import Environment, FileSystemLoader

import http.server
import socketserver
import datetime

PORT = 8000

# Filters
def strftime(value, format):
    return value.strftime(format)



class FakeDocument:
    """
    A fake documentation article
    """
    def __init__(self):
        self.title = "ASA"
        self.editable_by_anyone = True
        self.id = "1JZLzpB2gWVtdlgjBkKAMrKckpee9YjqAyt5zliBXGkM"
        self.authors = ["John Doe", "Jane Doe"]
        self.content = """
<div>
<p class="title" id="h.n9rpnjlpmr0w">Cisco ASA</p>
<h1 id="h.1zcxdkbdbmy1">ASA 8</h1>
<p class="warning"><strong>WARNING</strong><span>ASA 8&nbsp;IS NOT SUPPORTED</span></p>
<p><strong></strong></p>
<p>You may find a lot of tutorials on the Internet explaining how to extract ASA 8 images from physical hardware devices and use them with GNS3. This method was the only way to get an ASA image in the past, but the results are random; and getting worse with modern computers and operating systems. For example Windows 10 has multiple issues running ASA 8.</p>
<p><strong></strong></p>
<p>The problem with this way of doing things is that you are using an image made for a bespoke hardware device from Cisco. Qemu can emulate part of the hardware, but some components specific to a physical ASA are missing. For example, the hardware clock on the hardware ASA appliance is missing. The ASA kernel can sometimes replace it depending of the speed of your computer, but results may vary.</p>
<p></p>
<p>You will also encounter issues when running multiple ASAs simultaneously.</p>
<h1 id="h.ctygta8hamgc"></h1>
<h1 id="h.46g02c8z74m8">ASAv</h1>
<p>ASAv is a version of ASA made by Cisco for using ASA in virtualized environments. This the solution supported by Cisco and the GNS3 team.</p>
<p></p>
<p></p>
<h2 id="h.lla7xvwpp5jv">ASAv with Qemu (RECOMMENDED)</h2>
<p class="important"><strong>IMPORTANT</strong>Only images validated by VIRL team are known to work correctly with GNS3. &nbsp;</p>
<p>Images <strong>asav952-204.qcow2</strong>&nbsp;or later are recommend (previous releases may not work). It is very important to use the correct ASA image because only this image (or a later image validated by VIRL) will work with GNS3. </p>
<p></p>
<p class="note"><strong>NOTE</strong><span>Even though Cisco releases images via the download portal, only use images approved by the VIRL team with GNS3. Images on the main Cisco site may be missing required features such as console output.</span></p>
<p></p>
<p>To install the ASAv on GNS3, download the ASAv template from here:</p>
<p><span><a href="https://gns3.com/marketplace/appliance/cisco-asav">https://gns3.com/marketplace/appliance/cisco-asav</a></span></p>
<p><span><a href="https://gns3.com/marketplace/appliance/cisco-asav"></a></span></p>
<p>And follow these instructions to import an appliance:</p>
<p><span><a href="../1MAdxz0BSEAfGM7tA-w-o3TMmf8XOx7nBf0z6d9nRz_c/index.html">Install an appliance from the GNS3 Marketplace</a></span></p>
<p></p>
<h2 id="h.edn8761cbbra">ASAv with VMware</h2>
<p>You can run the ASAv OVA as a VMware VM. This will work, but is not recommended because it is harder to share the VM between projects or other GNS3 users.</p>
<p></p>
<h1 id="h.uftuzeconr0d">Using ASA</h1>
<p>Once the ASA appliance is imported into GNS3, you can create topologies such as the following:</p>
<p><span class="image"><a alt="image04.png" title="" class="image" href="5164d3b3afa2d162f660fd69e29628cf.jpg" target="_blank"><img src="5164d3b3afa2d162f660fd69e29628cf.jpg"></a></span></p>
<p>The cloud is linked to an eth2 interface of the GNS3 VM. In order to have an eth2 interface in the VM in the GNS3 VM settings in VMware (not in GNS3, the parameters of the VM in VMware) add a third network adapter with host only.</p>
<p></p>
<p>We use a generic switch between the cloud and the ASAv vm because a qemu limitation of the current version of GNS3 prevent a direct link between qemu and a cloud.</p>
<p></p>
<p>Our cloud configuration:</p>
<p><span class="image"><a alt="image05.png" title="" class="image" href="7da7206df1ad69400de81b2947669776.jpg" target="_blank"><img src="7da7206df1ad69400de81b2947669776.jpg"></a></span></p>
<p>The ASA is connected to the switch via is Management 0/0 interface.</p>
<p>After that boot the ASAv it will take a long time with a reboot the first time. Open the console and will see a prompt:</p>
<p class="code">ciscoasa&gt;</p>
<p></p>
<p>Switch to the configure mode (by default password is empty):</p>
<p class="code">ciscoasa&gt; enable<br>Password: <br>ciscoasa# configure terminal<br>ciscoasa(config)# <br><br>***************************** NOTICE *****************************<br><br>Help to improve the ASA platform by enabling anonymous reporting,<br>which allows Cisco to securely receive minimal error and health<br>information from the device. To learn more about this feature,<br>please visit: http://www.cisco.com/go/smartcall<br><br>Would you like to enable anonymous error reporting to help improve<br>the product? [Y]es, [N]o, [A]sk later: n<br>In the future, if you would like to enable this feature,<br>issue the command "call-home reporting anonymous".</p>
<p></p>
<p></p>
<p>We can now change the hostname and write the config</p>
<p class="code">ciscoasa(config)# hostname gns3asav<br>gns3asav(config)# write<br>Building configuration...<br>Cryptochecksum: 5c5f8e54 7203401c 38a17bec c74e13c6 <br><br>7413 bytes copied in 0.240 secs<br>[OK]<br></p>
<p><strong>Remember GNS3 will not save this for you. </strong>When you save in GNS3 you save the design of topology not the memory of the devices. Like in the real life you need to ask the OS to save before turning it off.</p>
<p></p>
<h2 id="h.no54mwxqb94">Configure ASDM</h2>
<p>In order to manage ASA with asdm we need to setup an ip on the Management 0/0 interface. Because the cloud is a VMware host only adapter we can use DHCP to do that.</p>
<p class="code">ciscoasa(config)# interface Management 0/0<br>ciscoasa(config-if)# ip address dhcp<br>ciscoasa(config-if)# no shutdown &nbsp;<br>ciscoasa(config-if)# nameif mgmt<br>INFO: Security level for "mgmt" set to 0 by default.<br>ciscoasa(config-if)# exit<br>ciscoasa(config)# show ip &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <br>System IP Addresses:<br>Interface &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Name &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; IP address &nbsp; &nbsp; &nbsp;Subnet mask &nbsp; &nbsp; Method <br>Management0/0 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;mgmt &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 172.16.16.156 &nbsp; 255.255.255.0 &nbsp; DHCP &nbsp;<br>Current IP Addresses:<br>Interface &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Name &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; IP address &nbsp; &nbsp; &nbsp;Subnet mask &nbsp; &nbsp; Method <br>Management0/0 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;mgmt &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 172.16.16.156 &nbsp; 255.255.255.0<br>We can see that our ASA as the IP 172.16.16.156</p>
<p></p>
<p>Now we need to enable the HTTP server</p>
<p class="code">ciscoasa(config)# http server enable<br>ciscoasa(config)# http 0.0.0.0 0.0.0.0 mgmt<br></p>
<p>Now open <span><a href="https://172.16.16.156/">https://172.16.16.156</a></span>&nbsp;and ignore the HTTPS certificate error.</p>
<p></p>
<p>You will see this page</p>
<p><span class="image"><a alt="image02.png" title="" class="image" href="e778a8e5bd51a94a32a17eb4d3ad2597.jpg" target="_blank"><img src="e778a8e5bd51a94a32a17eb4d3ad2597.jpg"></a></span></p>
<p>Click on install ASDM launcher. And when you have ASDM on your computer opened it. Enter the IP of the ASA and OK</p>
<p><span class="image"><a alt="image03.png" title="" class="image" href="f423b69b1947df18f7bdfb29b6d04b1d.jpg" target="_blank"><img src="f423b69b1947df18f7bdfb29b6d04b1d.jpg"></a></span></p>
<p>You will see the ASDM interface</p>
<p><span class="image"><a alt="image01.png" title="" class="image" href="a742fab65b5f3787d6940446a271588f.jpg" target="_blank"><img src="a742fab65b5f3787d6940446a271588f.jpg"></a></span></p>
<p>The warning about the licence is normal. The appliance provided by Cisco is dedicated to learning not a production usage where you need to pay.</p>
<p><span class="image"><a alt="image00.png" title="" class="image" href="21f220aa98028bdc08c1d8f652674bda.jpg" target="_blank"><img src="21f220aa98028bdc08c1d8f652674bda.jpg"></a></span></p>
<p></p>
<h1 id="h.z3tym6w95glf">Troubleshooting</h1>
<h2 id="h.rdlhal6wt4c9">No console is showing with ASAv</h2>
<p>Depending of the image, the serial console could be not activated. You need to use one of the recommended images.</p>
<p></p>
<h2 id="h.drkgoov0yp0y">Configuration is not saving when running ASAv on Windows</h2>
<p>ASAv is not supported by the version of Qemu provided for Windows you need to run it using the GNS3 VM.</p>
<p></p>
</div>
"""


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args):
        self._env = Environment(loader=FileSystemLoader('.'))
        self._env.filters['strftime'] = strftime
        super().__init__(*args)

    def render(self, template, root='.', **kwargs):
        template = self._env.get_template(template)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(template.render(root=root, config={"title": "GNS3"}, **kwargs).encode("utf-8"))

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            return self.render("index.html")
        elif self.path.startswith("/1") and self.path.endswith("/index.html"):
            return self.render("document.html", document=FakeDocument())
        return super().do_GET()

httpd = socketserver.TCPServer(("", PORT), Handler)
print("Serving at port", PORT)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    httpd.socket.close()
