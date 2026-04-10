from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc4


class Tc4Tests(WorkflowTestCase):
    def test_tc4(self):
        run_tc4(self)
