from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc43


class Tc43Tests(WorkflowTestCase):
    def test_tc43(self):
        run_tc43(self)
