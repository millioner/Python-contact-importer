from typing import Any
from django import http
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# from django.contrib.auth.decorators import login_required

from contact_importer.decorators import import_contacts


class ContactsView(TemplateView):
    template_name = "contacts.html"

    @method_decorator(
        [
            csrf_exempt,
            # login_required,
            import_contacts,
        ],
        name="dispatch",
    )
    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: http.HttpRequest, *args, **kwargs) -> http.HttpResponse:
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if kwargs.get("contact_provider"):
            context["contacts"] = kwargs["contact_provider"].get_contact_list()
        else:
            context["contacts"] = []
        return context
