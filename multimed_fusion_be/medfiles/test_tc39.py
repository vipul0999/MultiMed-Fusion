from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc39


class Tc39Tests(WorkflowTestCase):
    def test_tc39(self):
        run_tc39(self)
