import clips
import traceback
from clips import CLIPSError

class RulesEngine:
    def __init__(self, rules_path):
        self.env = clips.Environment()
        self.env.load(path=rules_path)

    def assert_fact(self, fact_string):
        """Asserts a new fact in the environment."""
        print(f"asserting fact: {fact_string}")
        try:
            self.env.eval(fact_string)
        except CLIPSError as e:
            # print error from clips
            print(e)
            traceback.print_exc()
        print(f"facts: {self.env.facts()}")

    def define_functions(self, functions):
        for f in functions:
            self.env.define_function(f)

    def undefine_functions(self, names):
        for name in names:
            self.env.find_function(name).undefine()

    def reset(self):
        """Resets the environment, removing all facts. Rules are retained."""
        print("resetting rules engine")
        self.env.reset()
        print("rules engine reset")

    def run(self):
        """Executes the rules in the environment."""
        print("running rules engine")
        self.env.run()
        print("rules engine finished")

    def get_fact_strings(self):
        return [str(f) for f in self.env.facts()]
