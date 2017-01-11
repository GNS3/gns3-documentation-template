import httplib2
import datetime
import argparse
import string
import shutil
import json
import lxml
import os

from retrying import retry
from apiclient import discovery
from apiclient.http import BatchHttpRequest

import oauth2client
import oauth2client.contrib.dictionary_storage
from oauth2client import client
from oauth2client import tools

import jinja2.exceptions

from .appliances import get_appliances
from .document import DriveDocument
from .utils import process_link
from .theme import Theme

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Docxel'


class Drive:
    @retry(wait_exponential_multiplier=1000, stop_max_attempt_number=10)
    def _callback_document_exported(self, request_id, data, exception):
        if exception:
            raise exception

        item = self._document_items[request_id]
        try:
            editable_by_anyone = self._permissions_for_anyone(item)
        except KeyError:
            editable_by_anyone = False
        template = 'document'
        if 'description' in item and item['description'].startswith('theme:'):
            template = item['description'].split(':')[1].strip()

        modifiedTime = datetime.datetime.strptime(item['modifiedTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
        self._documents[item['id']] = DriveDocument(item['id'], item['name'], data, self._export_dir,
                                 template=template,
                                 modifiedTime=modifiedTime,
                                 theme=self._theme,
                                 editable_by_anyone=editable_by_anyone,
                                 config=self._config,
                                 appliances=self._appliances)

    @retry(wait_exponential_multiplier=1000, stop_max_attempt_number=10)
    def _callback_document_authors(self, request_id, results, exception):
        if exception:
            raise exception

        file_id = self._document_items[request_id]
        authors = set()
        items = results.get('revisions', [])
        if items:
            for item in items:
                authors.add(string.capwords(item['lastModifyingUser']['displayName']))
        authors = list(authors)
        authors.sort()
        self._documents[file_id].authors = authors

    def process(self, config, export_dir, only_document_ids=[]):
        """
        :params only_document_id: Process only this document (For speedup tests)
        """
        # if os.path.exists(export_dir):
        #     shutil.rmtree(export_dir)
        #self._copy_ressources(export_dir)
        self._theme = Theme(export_dir)
        self._export_dir = export_dir
        self._config = config

        self._appliances = get_appliances()

        credentials = self._get_credentials(config)
        http = credentials.authorize(httplib2.Http(cache=".cache"))
        self._service = discovery.build('drive', 'v3', http=http)

        documents_id = set()
        documents_id.add((".", config['folder_id'], ))
        processed_ids = set()
        documents = []
        files_api = self._service.files()
        self._revision_api = self._service.revisions()
        self._permissions_api = self._service.permissions()

        self._document_items = {} # Google Drive document
        self._documents = {} # Final document object

        batch = self._service.new_batch_http_request(callback=self._callback_document_exported)
        request_id = 0
        last_modified_time = None # Last update of a document
        while len(documents_id) > 0:
            parent, document_id = documents_id.pop()
            processed_ids.add(document_id)
            search = "'{}' in parents".format(document_id)
            request = files_api.list(fields="nextPageToken, files(id, name, mimeType, permissions, modifiedTime, trashed, description)", q=search, pageSize=1000)
            while request is not None:
                results = request.execute()
                items = results.get('files', [])
                if items:
                    for item in items:
                        if only_document_ids != [] \
                           and item['id'] not in only_document_ids \
                           and item['mimeType'] != 'application/vnd.google-apps.folder':
                            continue
                        if  item['trashed']:
                            continue
                        if item['mimeType'] == 'application/vnd.google-apps.document':
                            modifiedTime = datetime.datetime.strptime(item['modifiedTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
                            if last_modified_time is None or modifiedTime > last_modified_time:
                                last_modified_time = modifiedTime
                            batch.add(files_api.export(fileId=item['id'], mimeType="text/html"), request_id=str(request_id))
                            self._document_items[str(request_id)] = item
                            request_id += 1
                        elif item['mimeType'] == 'application/vnd.google-apps.folder':
                            if not item['name'].startswith('.'):
                                documents_id.add((os.path.join(parent, item['name']), item['id'], ))
                        # else:
                        #     # Export other file directly to the disk
                        #     data = files_api.get_media(fileId=item['id']).execute()
                        #     os.makedirs(os.path.join(export_dir, parent), exist_ok=True)
                        #     with open(os.path.join(export_dir, parent, item['name']), 'wb+') as f:
                        #         f.write(data)

                request = files_api.list_next(request, results)

        batch.execute(http=http)

        # Batch requests for getting document authors
        batch = self._service.new_batch_http_request(callback=self._callback_document_authors)
        for document in self._documents.values():
            batch.add(self._revision_api.list(fields="nextPageToken, revisions(lastModifyingUser(displayName))", fileId=document.id, pageSize=1000), request_id=str(request_id))
            self._document_items[str(request_id)] = document.id
            request_id += 1
        batch.execute(http=http)

        for document in self._documents.values():
            document.export()

        for appliance_id, appliance in self._appliances.items():
            content = self._theme.render('appliance.html', appliance=appliance, appliance_id=appliance_id, root="..")
            os.makedirs(os.path.join(export_dir, 'appliances'), exist_ok=True)
            with open(os.path.join(export_dir, 'appliances', appliance_id + '.html'), 'wb+') as f:
                f.write(content.encode('utf-8'))

        for file in os.listdir('theme'):
            if (file.endswith('.html') or file.endswith('.txt')) and file not in ['document.html', 'base.html']:
                try:
                    content = self._theme.render(file, lastModifiedTime=last_modified_time, appliances=self._appliances)
                    with open(os.path.join(export_dir, file), 'wb+') as f:
                        f.write(content.encode('utf-8'))
                except jinja2.exceptions.TemplateRuntimeError:
                    pass # Not a template for global rendering

        print('Export finish file are inside', export_dir)


    @retry(wait_exponential_multiplier=1000, stop_max_attempt_number=10)
    def _permissions_for_anyone(self, item):
        """
        :returns: Boolean True if acessible by anyone
        """

        for perm in item['permissions']:
            if perm['type'] == 'anyone':
                if perm['role'] in ['commenter', 'writer']:
                    return True
                else:
                    self._permissions_api.update(fileId=item['id'], permissionId=perm['id'], body={
                        'role': 'commenter',
                    }).execute()
                    return True
        return False

    def _copy_ressources(self, export_dir):
        """
        Copy CSS, JS &  CO to the export directory
        """
        if os.path.exists(os.path.join(export_dir, 'ressources')):
            shutil.rmtree(os.path.join(export_dir, 'ressources'))
        ressources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ressources')
        shutil.copytree(ressources_dir, os.path.join(export_dir, 'ressources'))

    def _get_credentials(self, config):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """

        store = oauth2client.contrib.dictionary_storage.DictionaryStorage(config, 'oauth2')
        credentials = store.get()
        if not credentials or credentials.invalid:
            print("Ask credentials for " + config['user_id'])
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME

            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument('--logging_level', default='ERROR')
            parser.add_argument('--noauth_local_webserver', action='store_true',
                default=True, help='Do not run a local web server.')
            args = parser.parse_args([])
            credentials = tools.run_flow(flow, store, args)
            config.save()
        return credentials



