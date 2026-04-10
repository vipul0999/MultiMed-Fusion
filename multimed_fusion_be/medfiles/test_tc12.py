from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc12


class Tc12Tests(WorkflowTestCase):
    def test_tc12(self):
        run_tc12(self)
