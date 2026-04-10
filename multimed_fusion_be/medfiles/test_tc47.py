from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc47


class Tc47Tests(WorkflowTestCase):
    def test_tc47(self):
        run_tc47(self)
