from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc48


class Tc48Tests(WorkflowTestCase):
    def test_tc48(self):
        run_tc48(self)
