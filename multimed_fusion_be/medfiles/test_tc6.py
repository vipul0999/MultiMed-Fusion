from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc6


class Tc6Tests(WorkflowTestCase):
    def test_tc6(self):
        run_tc6(self)
