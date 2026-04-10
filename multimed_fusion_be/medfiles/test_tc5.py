from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc5


class Tc5Tests(WorkflowTestCase):
    def test_tc5(self):
        run_tc5(self)
