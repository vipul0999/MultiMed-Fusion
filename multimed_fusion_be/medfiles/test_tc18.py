from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc18


class Tc18Tests(WorkflowTestCase):
    def test_tc18(self):
        run_tc18(self)
