from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc29


class Tc29Tests(WorkflowTestCase):
    def test_tc29(self):
        run_tc29(self)
