from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc25


class Tc25Tests(WorkflowTestCase):
    def test_tc25(self):
        run_tc25(self)
