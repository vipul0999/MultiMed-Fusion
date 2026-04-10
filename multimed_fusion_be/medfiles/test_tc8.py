from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc8


class Tc8Tests(WorkflowTestCase):
    def test_tc8(self):
        run_tc8(self)
