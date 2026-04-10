from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc32


class Tc32Tests(WorkflowTestCase):
    def test_tc32(self):
        run_tc32(self)
