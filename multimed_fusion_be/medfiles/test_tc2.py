from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc2


class Tc2Tests(WorkflowTestCase):
    def test_tc2(self):
        run_tc2(self)
