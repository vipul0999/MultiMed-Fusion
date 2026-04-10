from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc27


class Tc27Tests(WorkflowTestCase):
    def test_tc27(self):
        run_tc27(self)
