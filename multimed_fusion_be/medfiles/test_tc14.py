from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc14


class Tc14Tests(WorkflowTestCase):
    def test_tc14(self):
        run_tc14(self)
