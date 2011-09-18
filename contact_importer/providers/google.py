###-*- coding: utf-8 -*-#################################
import json

import oauth2 as oauth
from .oauth import OAuthContacts

class GmailContacts(OAuthContacts):
    """
    Class for getting contacts from gmail account
    (api details at http://code.google.com/apis/contacts/docs/3.0/reference.html)
    You can get "OAuth Consumer Key" and "OAuth Consumer Secret Key" for your domain at
    https://www.google.com/accounts/ManageDomains
    """

    request_token_url = 'https://www.google.com/accounts/OAuthGetRequestToken'
    access_token_url = 'https://www.google.com/accounts/OAuthGetAccessToken'
    authorize_url = 'https://www.google.com/accounts/OAuthAuthorizeToken'

    get_contacts_url = 'https://www.google.com/m8/feeds/contacts/default/full' \
                                           '?alt=json&max-results=50&start-index=%s'

    scope_urls = ['https://www.google.com/m8/feeds/']
    # get contacts url:

    def get_contacts(self):
        """
        Implements a generator for iterating in contacts
        """
        super(GmailContacts, self).get_contacts()
        token = oauth.Token(self.access_token, self.access_token_secret)
        client = oauth.Client(self.consumer, token)
        start = 1
        data = None
        while start == 1 or 'entry' in data['feed']:
            resp, content = client.request(self.get_contacts_url % start, "GET")
            if resp.get('status') == '200':
                data = json.loads(content)
                if 'entry' in data['feed'] and len(data['feed']['entry']):
                    for entry in data['feed']['entry']:
                        contact = self.parse_contact(entry)
                        if contact:
                            yield contact
            else:
                raise Exception('Cannot retrieve a contact list')
            start += 50

    def parse_contact(self, contact):
        if u'gd$email' in contact:
            emails = []
            for e in contact[u'gd$email']:
                emails.append(e.get(u'address'))
            return {
                'name': contact.get('title', {}).get('$t', ''),
                'emails': emails
            }
        else:
            return None