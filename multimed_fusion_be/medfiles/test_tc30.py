from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc30


class Tc30Tests(WorkflowTestCase):
    def test_tc30(self):
        run_tc30(self)
