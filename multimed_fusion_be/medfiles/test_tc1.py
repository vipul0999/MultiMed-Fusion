from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc1


class Tc1Tests(WorkflowTestCase):
    def test_tc1(self):
        run_tc1(self)
