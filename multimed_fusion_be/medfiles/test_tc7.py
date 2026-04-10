from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc7


class Tc7Tests(WorkflowTestCase):
    def test_tc7(self):
        run_tc7(self)
