from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc35


class Tc35Tests(WorkflowTestCase):
    def test_tc35(self):
        run_tc35(self)
