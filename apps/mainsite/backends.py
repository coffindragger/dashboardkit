from django_auth_ldap.backend import LDAPBackend
from django.conf import settings
from django.contrib.auth.models import Group

class StaffLDAPBackend(LDAPBackend):

    def get_or_create_user(self, username, ldap_user):
        staff_group_name = getattr(settings, 'STAFF_GROUP_NAME', 'Staff')

        user, created = super(StaffLDAPBackend, self).get_or_create_user(username, ldap_user)
        if created:
            try:
                user.groups.add(Group.objects.get(name=staff_group_name))
            except Group.DoesNotExist:
                pass

            user.is_staff = True
            user.save()
        return (user, created)
