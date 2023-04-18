from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404


class IsOwnerPermissions(UserPassesTestMixin):
    def test_func(self):
        """
        Checks whether the user is the owner of the ticket.
        """
        if self.request.user.is_authenticated:
            ticket = self.get_object()
            return ticket.user == self.request.user
        return False
        # raise Http404


class IsOwnerOrAdminPermissions(UserPassesTestMixin):
    def test_func(self):
        """
        Checks whether the user is admin or the owner of the ticket.
        """
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return True
            ticket = self.get_object()
            return ticket.user == self.request.user
        return False
        # raise Http404


class IsAdminPermissions(UserPassesTestMixin):
    def test_func(self):
        """
        Checks whether the user is admin or the owner of the ticket.
        """
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return True
        return False
        # raise Http404