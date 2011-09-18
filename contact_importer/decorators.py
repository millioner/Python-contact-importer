###-*- coding: utf-8 -*-#################################
"""
Django integration module
"""
import json

from django.conf import settings
from django.shortcuts import redirect

from .providers.google import GmailContacts
from .providers.yahoo import YahooContacts
from .providers.hotmail import HotmailContacts

providers = {
    'google': GmailContacts,
    'yahoo': YahooContacts,
    'hotmail': HotmailContacts
}

PROVIDER_CREDENTIALS = settings.CONTACT_IMPORT_SETTINGS

if type(PROVIDER_CREDENTIALS) != dict:
    raise AttributeError('CONTACT_IMPORT_SETTINGS is not dictionary')

def get_contacts(view):

    def wrapped_func(request, **kwargs):
        service_name = request.GET.get('service') or request.session.get('contact_import_service')
        if not service_name:
            raise AttributeError('Service name is not defined')

        if service_name not in providers:
            raise AttributeError('Unknown service name: %s' % service_name)

        if type(PROVIDER_CREDENTIALS.get(service_name)) != dict:
            raise AttributeError('Settings for "%s" provider is not defined' % service_name)

        provider_class = providers.get(service_name)

        if 'contact_import_service' not in request.session:
            # step 1
            provider = provider_class(**PROVIDER_CREDENTIALS.get(service_name))
            request.session['contact_import_service'] = service_name
            current_url = request.build_absolute_uri(request.path)
            request.session['contact_import_data'] = json.dumps(provider.get_tokens(current_url))
            return redirect(provider.get_auth_url())
        else:
            # step 2
            params = dict(PROVIDER_CREDENTIALS.get(service_name))
            params.update(json.loads(request.session.get('contact_import_data', '[]')))
            params.update(dict([(k, v) for k, v in request.GET.items()]))

            if request.method == 'POST':
                params['post_params'] = request.POST
            provider = provider_class(**params)
            del request.session['contact_import_service']
            if 'contact_import_data' in request.session:
                del request.session['contact_import_data']
            return view(request, contact_provider=provider, **kwargs)

    return wrapped_func