from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc24


class Tc24Tests(WorkflowTestCase):
    def test_tc24(self):
        run_tc24(self)
