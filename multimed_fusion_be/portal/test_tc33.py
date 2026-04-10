from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc33


class Tc33Tests(WorkflowTestCase):
    def test_tc33(self):
        run_tc33(self)
