#!/bin/bash
docker build -t gns3documentation . && docker run -i -t -v `pwd`:/code gns3documentation $*
