"""
Django integration for contact_importer app.
"""
import json
import logging
from typing import Any, Dict

from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect

from .providers.google import GmailContacts

# from .providers.yahoo import YahooContacts
# from .providers.hotmail import HotmailContacts

logger = logging.getLogger(__name__)

providers = {
    "google": GmailContacts,
    # "yahoo": YahooContacts,
    # "hotmail": HotmailContacts,
}

PROVIDER_CREDENTIALS = settings.CONTACT_IMPORT_SETTINGS

if not isinstance(PROVIDER_CREDENTIALS, dict):
    raise AttributeError("CONTACT_IMPORT_SETTINGS is invalid")


def import_contacts(view):
    def wrapped_func(request: HttpRequest, **kwargs):
        service_name = request.GET.get("service") or request.session.get(
            "contact_import_service"
        )
        if not service_name:
            return view(request, contact_provider=None, **kwargs)

        if service_name not in providers:
            raise AttributeError(f"Unknown service name: {service_name}")

        if not isinstance(PROVIDER_CREDENTIALS.get(service_name), dict):
            raise AttributeError(
                f'Settings for "{service_name}" provider is not defined'
            )

        provider_class = providers.get(service_name)

        current_url = request.build_absolute_uri(request.get_full_path())
        provider = provider_class(
            credentials=PROVIDER_CREDENTIALS.get(service_name),
            redirect_url=current_url,
        )

        if "contact_import_service" not in request.session:
            logger.debug(
                "Step 1, gonna redirect user to consent. Service provider: %s",
                service_name,
            )
            # step 1
            request.session["contact_import_service"] = service_name
            # request.session["contact_import_data"] = json.dumps(
            #     provider.get_tokens(current_url)
            # )
            logger.debug("Redirecting to %s", provider.get_auth_url())
            return redirect(provider.get_auth_url())
        else:
            # step 2
            logger.debug("Step 2, getting contacts. Service provider: %s", service_name)
            # params = dict(PROVIDER_CREDENTIALS.get(service_name))
            # params.update(json.loads(request.session.get("contact_import_data", "[]")))
            # params.update(dict([(k, v) for k, v in request.GET.items()]))

            # if request.method == "POST":
            #     params["post_params"] = request.POST
            # provider = provider_class(**params)
            del request.session["contact_import_service"]

            if "contact_import_data" in request.session:
                del request.session["contact_import_data"]

            logger.debug("Getting contacts from %s", service_name)

            return view(request, contact_provider=provider, **kwargs)

    return wrapped_func
