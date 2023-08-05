from typing import Any

from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from contact_importer.decorators import get_contacts


@method_decorator(
    [
        # csrf_exempt,
        # login_required,
        # get_contacts,
    ],
    name="dispatch",
)
class ContactsView(TemplateView):
    template_name = "contacts.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if kwargs.get("contact_provider"):
            context["contacts"] = kwargs["contact_provider"].get_contact_list()
        else:
            context["contacts"] = []
        return context
