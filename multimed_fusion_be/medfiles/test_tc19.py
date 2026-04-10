from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc19


class Tc19Tests(WorkflowTestCase):
    def test_tc19(self):
        run_tc19(self)
