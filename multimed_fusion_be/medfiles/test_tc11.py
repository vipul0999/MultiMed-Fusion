from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc11


class Tc11Tests(WorkflowTestCase):
    def test_tc11(self):
        run_tc11(self)
