from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc31


class Tc31Tests(WorkflowTestCase):
    def test_tc31(self):
        run_tc31(self)
