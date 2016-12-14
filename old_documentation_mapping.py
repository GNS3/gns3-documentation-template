"""
This script create an old directory. This directory will
contains redirection link for the old documentation page to
their new location.
"""

import os
import shutil

mappings = [
    ('quick-start-guide-for-windows-us', '11YYG4NQlPSl31YwvVvBS9RAsOLSYv0Ocy-uG2K8ytIY'),
    ('quick-start-guide-for-mac-users', '1MlG-VjkfQVEDVwGMxE3sJ15eU2KTDsktnZZH8HSR-IQ'),
    ('linux-installation', '1QXVIihk7dsOL7Xr7Bmz4zRzTsJ02wklfImGuHwTlaA4'),
    ('adding-ios-or-iou-qemu-virtual-2', None),
    ('creating-the-simplest-topology-2', '1wr2j2jEfX6ihyzpXzC23wQ8ymHzID4K3Hn99-qqshfg'),
    ('download-the-gns3-vm', '1Bn-s1Izkjp13HxcPF4b8QSGfkWJYG_dpMt9U1DQjvZ4'),
    ('-what-is-the-gns3-vm', '1Bn-s1Izkjp13HxcPF4b8QSGfkWJYG_dpMt9U1DQjvZ4'),
    ('the-new-setup-wizard-for-gns3--4', None),
    ('symbols-2', '1BcjCN6dQkS3YKHHJjnx7n8WMSBh0IDRS_qRE15-yyF8'),
    ('glossary-of-terms', None),
    ('docker-2', '1KGkv1Vm5EgeDusk1qS1svacpuQ1ZUQSVK3XqJ01WKGc'),
    ('install-on-a-remote-server', '1c2Iyiczy6efnv-TS_4Hc7p11gn03-ytz9ukgwFfckDk'),
    ('gns3-configuration-file-for-adva', '1f6uXq05vukccKdMCHhdki5MXFhV8vcwuGwiRvXMQvM0'),
    ('move-from-iouvm-to-gns3-vm-2a', '1xfaVQMdmmomXDb7ssxReZlrwDxYhPiaOTaiFLITTPy8'),
    ('switching-simulation-in-gns3-ver', '1aQSkL4KyIh-3j-UCeuukj4Wg1VJ7uI-vwcewaUHbjbU'),
    ('installing-gns3-1-4-on-ubuntu-li', '1QXVIihk7dsOL7Xr7Bmz4zRzTsJ02wklfImGuHwTlaA4'),
    ('gns3-appliance-files-gns3a', '1MAdxz0BSEAfGM7tA-w-o3TMmf8XOx7nBf0z6d9nRz_c'),
    ('how-to-use-vmware-player-in-gns3', '1u_D9XSSA5PVFrOrTWSw1Vn8Utvimd6ksv76F7731N84'),
    ('how-to-use-vmware-fusion-in-gns3', '1u_D9XSSA5PVFrOrTWSw1Vn8Utvimd6ksv76F7731N84'),
    ('gns3-vm-configuration-with-vir-2', '1wdfvS-OlFfOf7HWZoSXMbG58C4pMSy7vKJFiKKVResc'),
    ('gns3-vm-configuration-with-vmw-3', '1wdfvS-OlFfOf7HWZoSXMbG58C4pMSy7vKJFiKKVResc'),
    ('how-to-use-vmware-workstation-in', '1u_D9XSSA5PVFrOrTWSw1Vn8Utvimd6ksv76F7731N84'),
    ('test-31', '1ESckH2e9owC5skfV09Aba1u2pji8bE1ZFDkXqMLVt3Y'),
    ('run-as-daemon', '1r-SWM3ro8ArPjMHgQslphaLLTjxx0fgOnOCq_1eGajA'),
    ('asa-2', '1JZLzpB2gWVtdlgjBkKAMrKckpee9YjqAyt5zliBXGkM'),
    ('import-virl-images', None),
    ('virtual-machines-supported-2', '1-kBrTplBltp9P3P-AigoMzlDO-ISyL1h3bYpOl5Q8mQ'),
    ('how-to-configure-non-native-io-3', '1PKfYwR78QP_Z3jqxBQ1pdy6SsqM27qhvdCvSmIizRh4'),
]

path = os.path.join('theme', 'old')
if os.path.exists(path):
    shutil.rmtree(path)
os.makedirs(path)

with open(os.path.join(path, 'index.html'), "w+") as f:
    f.write("""<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0;url=https://docs.gns3.com/">
        <title>Page Redirection</title>
    </head>
    <body>
        If you are not redirected automatically, follow the <a href='https://docs.gns3.com/'>link</a>
    </body>
</html>""")

for page_id, redirect_to in mappings:
    if redirect_to is None:
        redirect_to = ""
    os.makedirs(os.path.join(path, page_id))
    with open(os.path.join(path, page_id, 'index.html'), 'w+') as f:
        f.write("""
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0;url=https://docs.gns3.com/{redirect_to}">
        <title>Page Redirection</title>
    </head>
    <body>
        If you are not redirected automatically, follow the <a href='https://docs.gns3.com/{redirect_to}'>link</a>
    </body>
</html>
        """.format(redirect_to=redirect_to))
