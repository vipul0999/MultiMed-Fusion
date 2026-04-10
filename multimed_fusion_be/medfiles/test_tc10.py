from testsupport.base import WorkflowTestCase
from testsupport.sheet_scenarios import run_tc10


class Tc10Tests(WorkflowTestCase):
    def test_tc10(self):
        run_tc10(self)
