from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc15


class Tc15Tests(WorkflowTestCase):
    def test_tc15(self):
        run_tc15(self)
