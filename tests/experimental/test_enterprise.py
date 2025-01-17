#!/usr/bin/env python

"""Tests admin-related functionality"""

import os

import python_pachyderm
from python_pachyderm.experimental.service import enterprise_proto
from tests import util


@util.skip_if_no_enterprise()
def test_enterprise():
    client = python_pachyderm.experimental.Client()
    client.delete_all_license()
    client.activate_license(os.environ["PACH_PYTHON_ENTERPRISE_CODE"])
    client.add_cluster("localhost", "localhost:1650", secret="secret")
    client.activate_enterprise("localhost:1650", "localhost", "secret")
    assert client.get_enterprise_state().state == enterprise_proto.State.ACTIVE
    client.deactivate_enterprise()
    client.delete_all_license()
