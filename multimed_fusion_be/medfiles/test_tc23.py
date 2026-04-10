from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc23


class Tc23Tests(WorkflowTestCase):
    def test_tc23(self):
        run_tc23(self)
