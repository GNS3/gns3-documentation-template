#!/usr/bin/env python
#
# Copyright (C) 2016 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import io
import os
import json
import zipfile
import urllib.request

def get_appliances():
    """
    This will download an archive of all GNS3 appliances and load them to a dictionnary
    """
    appliances = {}

    url = 'https://github.com/GNS3/gns3-registry/archive/master.zip'
    response = urllib.request.urlopen(url)
    z = zipfile.ZipFile(io.BytesIO(response.read()))
    for path in z.namelist():
        if path.endswith('.gns3a'):
            with z.open(path, 'r') as f:
                id = os.path.basename(path).split('.')[0]
                appliances[id] = json.loads(f.read().decode())
    return appliances

if __name__ == '__main__':
    print(get_appliances())

