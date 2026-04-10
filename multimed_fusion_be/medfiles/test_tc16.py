from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc16


class Tc16Tests(WorkflowTestCase):
    def test_tc16(self):
        run_tc16(self)
