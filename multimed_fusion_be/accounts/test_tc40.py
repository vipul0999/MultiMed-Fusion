from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc40


class Tc40Tests(WorkflowTestCase):
    def test_tc40(self):
        run_tc40(self)
