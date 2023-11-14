import json
import logging

import google.oauth2.credentials
import google_auth_oauthlib.flow

from .oauth import OAuthContacts

logger = logging.getLogger(__name__)

# Create your Google project - https://console.developers.google.com/project
# Enable the People API - https://console.cloud.google.com/apis/dashboard
# Create credentials - https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred
# Getting OAuth 2.0 access tokens - https://developers.google.com/identity/protocols/oauth2/web-server#python_1
# Getting contacts API docs - https://developers.google.com/people/v1/contacts#python
# Code sample - https://developers.google.com/people/quickstart/python


class GmailContacts(OAuthContacts):
    """
    Class for getting contacts from gmail account
    (api details at http://code.google.com/apis/contacts/docs/3.0/reference.html)
    You can get "OAuth Consumer Key" and "OAuth Consumer Secret Key" for your domain at
    https://www.google.com/accounts/ManageDomains
    """

    # request_token_url = "https://www.google.com/accounts/OAuthGetRequestToken"
    # access_token_url = "https://www.google.com/accounts/OAuthGetAccessToken"
    # authorize_url = "https://www.google.com/accounts/OAuthAuthorizeToken"

    # get_contacts_url = (
    #     "https://www.google.com/m8/feeds/contacts/default/full"
    #     "?alt=json&max-results=50&start-index=%s"
    # )

    # https://www.googleapis.com/auth/contacts.readonly
    scope_urls = ["https://www.googleapis.com/auth/contacts.readonly"]

    def get_auth_url(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.credentials["client_secret_file"],  # TODO: is it in place?
            scopes=["https://www.googleapis.com/auth/contacts.readonly"],
        )
        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required. The value must exactly
        # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
        # configured in the API Console. If this value doesn't match an authorized URI,
        # you will get a 'redirect_uri_mismatch' error.
        # TODO: parametrize!
        flow.redirect_uri = "http://localhost:8000/contact-import/"

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        #
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type="online",
            # state=sample_passthrough_value,
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes="true",
        )
        return authorization_url
        # might later redirect to https://oauth2.example.com/auth?error=error_code
        # or https://oauth2.example.com/auth?code=auth_code

    # get contacts url:
    def get_contacts(self):
        """
        Implements a generator for iterating contacts
        """
        logger.debug("Getting contacts from Google - creating flow...")
        # state = some random state we sent to google in the auth url
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.credentials["client_secret_file"],  # TODO: is it in place?
            scopes=["https://www.googleapis.com/auth/contacts.readonly"],
            # state=state
        )
        # TODO: parametrize!
        flow.redirect_uri = "http://localhost:8000/contact-import/"

        logger.debug("Our redirect url: %s", self.redirect_url)
        flow.fetch_token(
            authorization_response=self.redirect_url.replace(
                "http", "https"
            )  # TODO: remove replace
        )

        # Store the credentials in the session.
        # ACTION ITEM for developers:
        #     Store user's access and refresh tokens in your data store if
        #     incorporating this code into your real app.
        credentials = {
            "token": flow.credentials.token,
            "refresh_token": flow.credentials.refresh_token,
            "token_uri": flow.credentials.token_uri,
            "client_id": flow.credentials.client_id,
            "client_secret": flow.credentials.client_secret,
            "scopes": flow.credentials.scopes,
        }
        logger.info("credentials: %s", credentials)
        # TODO: import contacts finally!!!
        # service = build("people", "v1", credentials=creds)
        # people = people_service.people().connections()
        #     .list('people/me', personFields='names,emailAddresses')

        # or

        # results = (
        #     service.people()
        #     .connections()
        #     .list(
        #         resourceName="people/me",
        #         pageSize=10,
        #         personFields="names,emailAddresses",
        #     )
        #     .execute()
        # )
        # connections = results.get("connections", [])

        return []

    def parse_contact(self, contact):
        if "gd$email" in contact:
            emails = []
            for e in contact["gd$email"]:
                emails.append(e.get("address"))
            return {"name": contact.get("title", {}).get("$t", ""), "emails": emails}
        else:
            return None
