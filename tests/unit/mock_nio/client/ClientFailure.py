from __future__ import annotations

import abc

from ansible_collections.famedly.matrix.tests.unit.mock_nio.client import failure


class ClientFailure(failure.ClientLogin, failure.ClientLogout, abc.ABC):
    pass
