from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc44


class Tc44Tests(WorkflowTestCase):
    def test_tc44(self):
        run_tc44(self)
