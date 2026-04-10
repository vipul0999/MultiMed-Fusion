from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc9


class Tc9Tests(WorkflowTestCase):
    def test_tc9(self):
        run_tc9(self)
