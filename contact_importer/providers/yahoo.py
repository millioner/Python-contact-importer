###-*- coding: utf-8 -*-#################################
import json

import oauth2 as oauth
import urllib
from .oauth import OAuthContacts

class YahooContacts(OAuthContacts):
    """
    Class for getting contacts from Yahoo! account
    (api details at http://developer.yahoo.com/oauth/guide/oauth-guide.html and http://developer.yahoo.com/yql/guide/index.html)
    You can get "OAuth Consumer Key" and "OAuth Consumer Secret Key" for your domain at
    https://developer.apps.yahoo.com/dashboard/createKey.html
    """
    service_name = 'yahoo'

    request_token_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
    access_token_url = 'https://api.login.yahoo.com/oauth/v2/get_token'
    authorize_url = 'https://api.login.yahoo.com/oauth/v2/request_auth'

    get_contacts_url = 'http://social.yahooapis.com/v1/user/%s/contacts?format=json'
    get_guid_url = 'http://social.yahooapis.com/v1/me/guid?format=json'

    contact_query = { 'q': 'select * from social.contacts where guid=me;', 'format': 'json' }

    def get_contacts(self):
        """
        Implements a generator for iterating in contacts
        """
        super(YahooContacts, self).get_contacts()
        token = oauth.Token(self.access_token, self.access_token_secret)
        client = oauth.Client(self.consumer, token)

        resp, content = client.request(self.get_contacts_url % self.get_guid(client), "GET")

        if resp.get('status') == '200':
            data = json.loads(content).get('contacts')
            if data['total']:
                for contact in data.get('contact'):
                    c = self.parse_contact(contact)
                    if c.get('emails'):
                        yield c
        else:
            raise Exception('Cannot retrieve a contact list')

    def get_guid(self, client):
        resp, content = client.request(self.get_guid_url, "GET")
        if resp.get('status') == '200':
            data = json.loads(content)
        else:
            return None
        
        return data.get('guid', {}).get('value')

    def parse_contact(self, contact):
        emails = []
        name = ''
        nickname = ''
        for field in contact.get('fields'):
            type = field.get('type')
            value = field.get('value')
            if type == 'nickname':
                nickname = value
            elif type == 'email':
                emails.append(value)
            elif type == 'name':
                name = "%s %s %s" % (value['givenName'], value['middleName'], value['familyName'])

        return { 'name': name or nickname, 'emails': emails }

    def get_contact_list(self):
        """
        Returns a contact list
        """
        return [c for c in self.get_contacts()]