from django.db import models



class DatabaseTemplate(models.Model):
    template_name = models.CharField(max_length=1024, unique=True, db_index=True)
    template_source = models.TextField(blank=True)

    class Meta:
        ordering = ('template_name',)

    def __unicode__(self):
        return self.template_name
