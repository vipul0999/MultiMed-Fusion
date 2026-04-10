from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc36


class Tc36Tests(WorkflowTestCase):
    def test_tc36(self):
        run_tc36(self)
