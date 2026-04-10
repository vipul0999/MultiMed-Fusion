from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc17


class Tc17Tests(WorkflowTestCase):
    def test_tc17(self):
        run_tc17(self)
