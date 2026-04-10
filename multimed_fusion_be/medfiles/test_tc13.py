from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc13


class Tc13Tests(WorkflowTestCase):
    def test_tc13(self):
        run_tc13(self)
