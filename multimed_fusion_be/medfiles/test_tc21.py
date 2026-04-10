from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc21


class Tc21Tests(WorkflowTestCase):
    def test_tc21(self):
        run_tc21(self)
