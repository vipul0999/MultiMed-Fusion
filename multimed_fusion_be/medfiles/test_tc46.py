from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc46


class Tc46Tests(WorkflowTestCase):
    def test_tc46(self):
        run_tc46(self)
