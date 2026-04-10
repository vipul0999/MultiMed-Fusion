from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc38


class Tc38Tests(WorkflowTestCase):
    def test_tc38(self):
        run_tc38(self)
