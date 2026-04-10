from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc3


class Tc3Tests(WorkflowTestCase):
    def test_tc3(self):
        run_tc3(self)
