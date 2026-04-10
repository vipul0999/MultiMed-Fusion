from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc37


class Tc37Tests(WorkflowTestCase):
    def test_tc37(self):
        run_tc37(self)
