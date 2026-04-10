from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc20


class Tc20Tests(WorkflowTestCase):
    def test_tc20(self):
        run_tc20(self)
