import clips

class CLIPS:
    def __init__(self, rules_path):
        self.env = clips.Environment()
        self.env.load(path=rules_path)

    def assert_fact(self, fact_string):
        """Asserts a new fact in the environment."""
        self.env.build(fact_string)

    def define_functions(self, functions):
        for f in functions:
            self.env.define_function(f)

    def undefine_functions(self, names):
        for name in names:
            self.env.find_function(name).undefine()

    def reset(self):
        """Resets the environment, removing all facts. Rules are retained."""
        self.env.reset()

    def run(self):
        """Executes the rules in the environment."""
        self.env.run()

    def get_fact_strings(self):
        return [str(f) for f in environment.facts()]
