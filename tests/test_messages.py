from fedora_review_service.helpers import find_srpm_url, review_package_name
from fedora_review_service.messages.copr import Copr
from fedora_review_service.messages.bugzilla import Bugzilla
from tests.base import MessageTestCase


class TestMessages(MessageTestCase):

    def test_review_package_name(self):
        summary = "Review Request: libgbinder - C interfaces for Android binder"
        assert review_package_name(summary) == "libgbinder"

    def test_find_srpm_url(self):
        message = self.get_message("bugzilla-contributor-srpm-update.json")
        packagename = review_package_name(message.body["bug"]["summary"])
        srpm_url = find_srpm_url(packagename, message.body["comment"]["body"])
        assert srpm_url == (
            "https://download.copr.fedorainfracloud.org"
            "/results/aleasto/waydroid/fedora-rawhide-x86_64/05068987-libgbinder"
            "/libgbinder-1.1.29-1.fc38.src.rpm"
        )


class TestCopr(MessageTestCase):

    def test_ignore(self):
        name = "copr-review-build-end.json"

        message = self.get_message(name)
        assert Copr(message).ignore is False

        message = self.get_message(name)
        message.body["chroot"] = "fedora-37-x86_64"
        assert Copr(message).ignore is True

        message = self.get_message(name)
        message.body["owner"] = "jdoe"
        assert Copr(message).ignore is True

        message = self.get_message(name)
        message.body["copr"] = "coprname-not-related-to-review"
        assert Copr(message).ignore is True


class TestBugzilla(MessageTestCase):

    def test_ignore(self):
        message = self.get_message("bugzilla-contributor-srpm-update.json")
        assert Bugzilla(message).ignore is False

        message = self.get_message("bugzilla-reviewer-comment.json")
        assert Bugzilla(message).ignore is True

        message = self.get_message("bugzilla-reviewer-metadata-update.json")
        assert Bugzilla(message).ignore is True
