from __future__ import annotations

import abc

from ansible_collections.famedly.matrix.tests.unit.mock_nio.client import success


class ClientSuccess(success.ClientLogin, success.ClientLogout, abc.ABC):
    pass
