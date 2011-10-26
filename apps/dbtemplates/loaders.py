from django.template.loader import BaseLoader
from django.template.base import TemplateDoesNotExist

from dbtemplates.models import DatabaseTemplate

class DatabaseTemplateLoader(BaseLoader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        try:
            dbtemplate = DatabaseTemplate.objects.get(template_name=template_name)
            return (dbtemplate.template_source, dbtemplate)
        except DatabaseTemplate.DoesNotExist as e:
            pass

        raise TemplateDoesNotExist(template_name)

_loader = DatabaseTemplateLoader
