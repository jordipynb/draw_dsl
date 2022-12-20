
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AXIOM BASE CALL_RULE CALL_SHAPE COMMA C_KEY C_PAR DRAW ID INT ITER JUMP LEFT LINE NILL O_KEY O_PAR PENCIL POP PUSH RIGHT RULE SHAPE TWO_POINTscene : draws_instructiondraws_instruction : draws_instruction shape\n\t                     | draws_instruction draw\n\t\t\t\t\t\t | shape\n\t\t\t\t\t\t | drawdraw : DRAW ID INT COMMA INT\n\t        | DRAW ID\n\t\t\t| DRAW NILLshape : SHAPE ID O_KEY pencil rules_locals axiom C_KEYpencil : PENCIL ID\n\t\t\t  | rules_locals : rules\n\t                | rules  : rule rules\n\t          | rulerule  : RULE ID O_KEY base instructions loop C_KEYbase : BASE TWO_POINT instruction_base\n\t        | BASE O_KEY instructions_base C_KEYinstructions_base : instruction_base instructions_base\n\t\t\t\t    \t | instruction_base instruction_base  : LEFT  INT   \n\t\t\t\t\t\t | RIGHT INT     \n\t\t\t\t\t\t | LINE  INT   \n\t\t\t\t\t\t | JUMP  INT COMMA INT      \n\t\t\t\t\t\t | NILL  \n\t\t\t\t\t\t | PUSH  INT COMMA INT \t\t\n\t\t\t\t\t\t | POP \n\t\t\t\t\t\t | CALL_SHAPE IDinstructions : instruction instructions\n\t\t\t\t    | instruction instruction  : instruction_base\n\t                | CALL_RULE IDloop : ITER INT\n\t\t\t| axiom  : AXIOM O_KEY instructions_axiom C_KEYinstructions_axiom : instruction_axiom instructions_axiom\n\t                      | instruction_axiominstruction_axiom  : instruction_base\n\t                      | CALL_RULE ID O_PAR INT C_PAR'
    
_lr_action_items = {'SHAPE':([0,2,3,4,7,8,10,11,22,27,],[5,5,-4,-5,-2,-3,-7,-8,-6,-9,]),'DRAW':([0,2,3,4,7,8,10,11,22,27,],[6,6,-4,-5,-2,-3,-7,-8,-6,-9,]),'$end':([1,2,3,4,7,8,10,11,22,27,],[0,-1,-4,-5,-2,-3,-7,-8,-6,-9,]),'ID':([5,6,15,20,33,41,56,],[9,10,21,26,46,52,65,]),'NILL':([6,28,31,32,38,40,42,47,48,49,52,54,55,57,58,65,66,68,70,71,74,76,],[11,38,38,-38,-25,-27,38,-21,-22,-23,-28,38,-31,38,38,-32,-17,38,-24,-26,-18,-39,]),'O_KEY':([9,24,26,43,],[12,28,29,58,]),'INT':([10,16,34,35,36,37,39,59,60,61,63,],[13,22,47,48,49,50,51,69,70,71,73,]),'PENCIL':([12,],[15,]),'RULE':([12,14,19,21,72,],[-11,20,20,-10,-16,]),'AXIOM':([12,14,17,18,19,21,25,72,],[-11,-13,24,-12,-15,-10,-14,-16,]),'COMMA':([13,50,51,],[16,60,61,]),'C_KEY':([23,30,31,32,38,40,44,45,47,48,49,52,53,54,55,62,64,65,67,68,70,71,73,75,76,],[27,44,-37,-38,-25,-27,-35,-36,-21,-22,-23,-28,-34,-30,-31,72,-29,-32,74,-20,-24,-26,-33,-19,-39,]),'CALL_RULE':([28,31,32,38,40,42,47,48,49,52,54,55,65,66,70,71,74,76,],[33,33,-38,-25,-27,56,-21,-22,-23,-28,56,-31,-32,-17,-24,-26,-18,-39,]),'LEFT':([28,31,32,38,40,42,47,48,49,52,54,55,57,58,65,66,68,70,71,74,76,],[34,34,-38,-25,-27,34,-21,-22,-23,-28,34,-31,34,34,-32,-17,34,-24,-26,-18,-39,]),'RIGHT':([28,31,32,38,40,42,47,48,49,52,54,55,57,58,65,66,68,70,71,74,76,],[35,35,-38,-25,-27,35,-21,-22,-23,-28,35,-31,35,35,-32,-17,35,-24,-26,-18,-39,]),'LINE':([28,31,32,38,40,42,47,48,49,52,54,55,57,58,65,66,68,70,71,74,76,],[36,36,-38,-25,-27,36,-21,-22,-23,-28,36,-31,36,36,-32,-17,36,-24,-26,-18,-39,]),'JUMP':([28,31,32,38,40,42,47,48,49,52,54,55,57,58,65,66,68,70,71,74,76,],[37,37,-38,-25,-27,37,-21,-22,-23,-28,37,-31,37,37,-32,-17,37,-24,-26,-18,-39,]),'PUSH':([28,31,32,38,40,42,47,48,49,52,54,55,57,58,65,66,68,70,71,74,76,],[39,39,-38,-25,-27,39,-21,-22,-23,-28,39,-31,39,39,-32,-17,39,-24,-26,-18,-39,]),'POP':([28,31,32,38,40,42,47,48,49,52,54,55,57,58,65,66,68,70,71,74,76,],[40,40,-38,-25,-27,40,-21,-22,-23,-28,40,-31,40,40,-32,-17,40,-24,-26,-18,-39,]),'CALL_SHAPE':([28,31,32,38,40,42,47,48,49,52,54,55,57,58,65,66,68,70,71,74,76,],[41,41,-38,-25,-27,41,-21,-22,-23,-28,41,-31,41,41,-32,-17,41,-24,-26,-18,-39,]),'BASE':([29,],[43,]),'ITER':([38,40,47,48,49,52,53,54,55,64,65,70,71,],[-25,-27,-21,-22,-23,-28,63,-30,-31,-29,-32,-24,-26,]),'TWO_POINT':([43,],[57,]),'O_PAR':([46,],[59,]),'C_PAR':([69,],[76,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'scene':([0,],[1,]),'draws_instruction':([0,],[2,]),'shape':([0,2,],[3,7,]),'draw':([0,2,],[4,8,]),'pencil':([12,],[14,]),'rules_locals':([14,],[17,]),'rules':([14,19,],[18,25,]),'rule':([14,19,],[19,19,]),'axiom':([17,],[23,]),'instructions_axiom':([28,31,],[30,45,]),'instruction_axiom':([28,31,],[31,31,]),'instruction_base':([28,31,42,54,57,58,68,],[32,32,55,55,66,68,68,]),'base':([29,],[42,]),'instructions':([42,54,],[53,64,]),'instruction':([42,54,],[54,54,]),'loop':([53,],[62,]),'instructions_base':([58,68,],[67,75,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> scene","S'",1,None,None,None),
  ('scene -> draws_instruction','scene',1,'p_scene','grammar.py',13),
  ('draws_instruction -> draws_instruction shape','draws_instruction',2,'p_draws_instruction','grammar.py',19),
  ('draws_instruction -> draws_instruction draw','draws_instruction',2,'p_draws_instruction','grammar.py',20),
  ('draws_instruction -> shape','draws_instruction',1,'p_draws_instruction','grammar.py',21),
  ('draws_instruction -> draw','draws_instruction',1,'p_draws_instruction','grammar.py',22),
  ('draw -> DRAW ID INT COMMA INT','draw',5,'p_draw','grammar.py',35),
  ('draw -> DRAW ID','draw',2,'p_draw','grammar.py',36),
  ('draw -> DRAW NILL','draw',2,'p_draw','grammar.py',37),
  ('shape -> SHAPE ID O_KEY pencil rules_locals axiom C_KEY','shape',7,'p_shape','grammar.py',49),
  ('pencil -> PENCIL ID','pencil',2,'p_pencil','grammar.py',64),
  ('pencil -> <empty>','pencil',0,'p_pencil','grammar.py',65),
  ('rules_locals -> rules','rules_locals',1,'p_rules_locals','grammar.py',72),
  ('rules_locals -> <empty>','rules_locals',0,'p_rules_locals','grammar.py',73),
  ('rules -> rule rules','rules',2,'p_rules','grammar.py',80),
  ('rules -> rule','rules',1,'p_rules','grammar.py',81),
  ('rule -> RULE ID O_KEY base instructions loop C_KEY','rule',7,'p_rule','grammar.py',88),
  ('base -> BASE TWO_POINT instruction_base','base',3,'p_base','grammar.py',98),
  ('base -> BASE O_KEY instructions_base C_KEY','base',4,'p_base','grammar.py',99),
  ('instructions_base -> instruction_base instructions_base','instructions_base',2,'p_instructions_base','grammar.py',103),
  ('instructions_base -> instruction_base','instructions_base',1,'p_instructions_base','grammar.py',104),
  ('instruction_base -> LEFT INT','instruction_base',2,'p_instruction_base','grammar.py',111),
  ('instruction_base -> RIGHT INT','instruction_base',2,'p_instruction_base','grammar.py',112),
  ('instruction_base -> LINE INT','instruction_base',2,'p_instruction_base','grammar.py',113),
  ('instruction_base -> JUMP INT COMMA INT','instruction_base',4,'p_instruction_base','grammar.py',114),
  ('instruction_base -> NILL','instruction_base',1,'p_instruction_base','grammar.py',115),
  ('instruction_base -> PUSH INT COMMA INT','instruction_base',4,'p_instruction_base','grammar.py',116),
  ('instruction_base -> POP','instruction_base',1,'p_instruction_base','grammar.py',117),
  ('instruction_base -> CALL_SHAPE ID','instruction_base',2,'p_instruction_base','grammar.py',118),
  ('instructions -> instruction instructions','instructions',2,'p_instructions','grammar.py',148),
  ('instructions -> instruction','instructions',1,'p_instructions','grammar.py',149),
  ('instruction -> instruction_base','instruction',1,'p_instruction','grammar.py',156),
  ('instruction -> CALL_RULE ID','instruction',2,'p_instruction','grammar.py',157),
  ('loop -> ITER INT','loop',2,'p_loop','grammar.py',168),
  ('loop -> <empty>','loop',0,'p_loop','grammar.py',169),
  ('axiom -> AXIOM O_KEY instructions_axiom C_KEY','axiom',4,'p_axiom','grammar.py',178),
  ('instructions_axiom -> instruction_axiom instructions_axiom','instructions_axiom',2,'p_instructions_axiom','grammar.py',182),
  ('instructions_axiom -> instruction_axiom','instructions_axiom',1,'p_instructions_axiom','grammar.py',183),
  ('instruction_axiom -> instruction_base','instruction_axiom',1,'p_instruction_axiom','grammar.py',190),
  ('instruction_axiom -> CALL_RULE ID O_PAR INT C_PAR','instruction_axiom',5,'p_instruction_axiom','grammar.py',191),
]
