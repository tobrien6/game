import clips
import psutil
import time

DEFTEMPLATE_STRING = """
(deftemplate person
  (slot name (type STRING))
  (slot surname (type STRING))
  (slot birthdate (type SYMBOL)))
"""

DEFRULE_STRING = """
(defrule hello-world
  "Greet a new person."
  (person (name ?name) (surname ?surname))
  =>
  (assert (tst blah))
  (println "Hello " (py-test ?name) " " ?surname))
  
"""

[clips.Environment() for _ in range(10000)]
t = time.time()
environment = clips.Environment()

def py_test(*der):
  s = ["a", "b", "c"]
  return "a b c"

environment.define_function(py_test, name="py-test")
#environment.find_function("py-test").undefine()

# define constructs
environment.build(DEFTEMPLATE_STRING)

environment.build(DEFRULE_STRING)

# retrieve the fact template
template = environment.find_template('person')

# assert a new fact through its template
fact = template.assert_fact(name='John',
                            surname='Doe',
                            birthdate=clips.Symbol('01/01/1970'))

# fact slots can be accessed as dictionary elements
assert fact['name'] == 'John'

# execute the activations in the agenda
environment.run()

final_facts = []
for f in environment.facts():
  final_facts.append(str(f))

print(f"took: {time.time() - t}")

print(final_facts)

print(psutil.cpu_percent())
print(psutil.virtual_memory())  # physical memory usage
print('memory % used:', psutil.virtual_memory()[2])