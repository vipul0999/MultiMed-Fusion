from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc34


class Tc34Tests(WorkflowTestCase):
    def test_tc34(self):
        run_tc34(self)
