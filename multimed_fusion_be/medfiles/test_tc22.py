from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc22


class Tc22Tests(WorkflowTestCase):
    def test_tc22(self):
        run_tc22(self)
