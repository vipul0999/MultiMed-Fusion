from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc45


class Tc45Tests(WorkflowTestCase):
    def test_tc45(self):
        run_tc45(self)
