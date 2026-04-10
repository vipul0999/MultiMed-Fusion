from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc26


class Tc26Tests(WorkflowTestCase):
    def test_tc26(self):
        run_tc26(self)
