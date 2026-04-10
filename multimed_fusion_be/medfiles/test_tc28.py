from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc28


class Tc28Tests(WorkflowTestCase):
    def test_tc28(self):
        run_tc28(self)
