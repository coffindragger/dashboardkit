from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group

from hashlib import sha1
import zipfile
import os


ACCESS_READ = 'r'
ACCESS_WRITE = 'w'
ACCESS_CHOICES = (
    (ACCESS_READ, 'Read Only'),
    (ACCESS_READ, 'Read/Write'),
)

STATUS_DRAFT = 'draft'
STATUS_WIP = 'wip'
STATUS_LIVE = 'live'
STATUS_DEFUNCT = 'defunct'
STATUS_CHOICES = (
    (STATUS_DRAFT, 'Draft'),
    (STATUS_WIP, 'Work-in-progress'),
    (STATUS_LIVE, 'Live'),
    (STATUS_DEFUNCT, 'Defunct'),
)


class Dashboard(models.Model):
    owner = models.ForeignKey("auth.User")
    url = models.CharField(max_length=1024, db_index=True)
    title = models.CharField(max_length=1024, blank=False)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default=STATUS_DRAFT, db_index=True)
    template_name = models.CharField(max_length=1024, default='dashboard/base.html')

    def __unicode__(self):
        return self.title


    def gadget_rows(self):
        rows = {}
        for dg in self.dashboardgadget_set.all():
            if dg.row not in rows:
                rows[dg.row] = []
            rows[dg.row].append( (dg.position,(dg.gadget,dg.query_args)) )
        for row_no,gadgets in sorted(rows.items(), lambda x,y: cmp(x[0],y[0])):
            if len(gadgets) >= 3:
                yui_grid = 'yui-gb'
            else:
                yui_grid = 'yui-gc'

            yield(yui_grid, tuple(g for p,g in sorted(gadgets, lambda x,y:cmp(x[0],y[0]))))


class DashboardTeam(models.Model):
    dashboard = models.ForeignKey(Dashboard)
    group = models.ForeignKey("auth.Group", null=True, blank=True)
    access = models.CharField(max_length=64, choices=ACCESS_CHOICES, default=ACCESS_READ)



class Gadget(models.Model):
    owner = models.ForeignKey("auth.User")
    name = models.CharField(max_length=1024)
    uuid = models.CharField(max_length=64, editable=False, db_index=True, unique=True)
    description = models.TextField(blank=True)
    archive = models.FileField(upload_to=lambda instance, filename: '%s/%s' % (instance.owner, instance.magic_cookie))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.magic_cookie
        super(Gadget, self).save(*args, **kwargs)
        self.explode_archive()

    @property
    def magic_cookie(self):
        if not self.uuid:
            self.uuid = sha1(self.name).hexdigest()
        return self.uuid

    @property
    def explode_root(self):
        if not hasattr(settings, 'EXPLODE_ROOT'):
            raise AttributeError("EXPLODE_ROOT must be defined.")
        return os.path.join(settings.EXPLODE_ROOT, 'gadgets', self.magic_cookie)

    def explode_archive(self):
        zf = zipfile.ZipFile(self.archive.path)
        zf.extractall(self.explode_root)
        zf.close()
        return ""

    @property
    def document_root(self):
        if hasattr(self, '_document_root'):
            return self._document_root

        # look for a file called 'index.html', if oyu find one, use its directory as the toplevel directory.

        for dirname,dirs,files in os.walk(self.explode_root):
            if 'index.html' in files:
                self._document_root = dirname.replace(settings.EXPLODE_ROOT,'')
                return self._document_root

        return None




class GadgetTeam(models.Model):
    widget = models.ForeignKey(Gadget)
    group = models.ForeignKey("auth.Group", null=True, blank=True)
    access = models.CharField(max_length=64, choices=ACCESS_CHOICES, default=ACCESS_READ)





class DashboardGadget(models.Model):
    dashboard = models.ForeignKey(Dashboard)
    row = models.PositiveIntegerField(default=0, choices=((c,c) for c in range(0,11)))
    position = models.PositiveIntegerField(default=1, choices=((c,c) for c in range(1,4)))
    gadget = models.ForeignKey(Gadget)
    query_args = models.CharField(max_length=1024,blank=True)


    def __unicode__(self):
        if self.gadget_id:
            return self.gadget.__unicode__() 
        return "DashboardGadget object"
