from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc41


class Tc41Tests(WorkflowTestCase):
    def test_tc41(self):
        run_tc41(self)
