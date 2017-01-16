import json
import sys


from drive import Drive
from config import Config


import logging
log = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


def main():
    if len(sys.argv) < 3:
        print("You need to pass a config file as parameter and the export directory")
    config = Config(sys.argv[1])
    d = Drive(config)
    d.create_appliance_documents()
    d.process(sys.argv[2], only_document_ids=sys.argv[3:])


if __name__ == '__main__':
    main()
