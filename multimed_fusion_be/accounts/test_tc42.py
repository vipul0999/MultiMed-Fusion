from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc42


class Tc42Tests(WorkflowTestCase):
    def test_tc42(self):
        run_tc42(self)
