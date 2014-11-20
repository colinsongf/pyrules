from pyrules.engine import RuleContext, RuleEngine
from pyrules.rules import Rule, TableRuleset


class CalculateBasicFare(Rule):
    def should_trigger(self, context):
        return True
    def perform(self, context):
        context.fare = context.distance * 20
        return context.fare
        
class CalculateWeekendFare(Rule):
    def should_trigger(self, context):
        return context.weekend 
    def perform(self, context):
        context.fare = context.fare * 1.2
        return context.fare 
    
translations=[
  ('das Wetter', 'context.weather'),
  ('ist', '=='),
  ('schoen', '"nice"'),
  ('Fahrpreis', 'context.fare'),
  ('Wochenende', 'context.weekend'),  
  ('nicht', 'not'),
  ('am Sonntag', 'context.sunday'),
]
    
manyrules = TableRuleset([
  { 'if': ['nicht Wochenende', 'das Wetter ist schoen'],
    'then' : ['Fahrpreis * 1'],
    'target' : ['Fahrpreis'],
  },
  { 'if': ['am Sonntag', 'das Wetter ist schoen'],
    'then' : ['Fahrpreis * 1.5'],
    'target' : ['Fahrpreis'],
  }
], translations=translations)

ruleset = (CalculateBasicFare(),
           CalculateWeekendFare(),
           manyrules,
           #SequencedRuleset([CalculateBasicFare(), CalculateWeekendFare()]),
)

context = RuleContext()
context.distance = 10
context.weekend = 0
context.weather = 'nice'
context.sunday = 1

engine = RuleEngine()
#%timeit engine.execute(ruleset, context)
context = engine.execute(ruleset, context)

print "fare", context.fare
print "executed", context._executed