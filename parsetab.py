
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AXIOM BASE CALL_RULE CALL_SHAPE COMMA C_KEY DEPTH DRAW FILL FLOAT ID INT ITER JUMP LEFT LINE NILL O_KEY PENCIL POP PUSH RIGHT RULE SHAPE TWO_POINTscene    : draws_instruction scene\n\t            | draws_instruction\n\t\t\t\t| shapesdraws_instruction : shapes drawsshapes : shape shapes \n\t          | shapedraws  : draw draws\n\t\t\t  | drawdraw : DRAW ID INT COMMA INTshape : SHAPE ID pencilpencil : PENCIL ID fill\n\t\t\t  | fillfill   : FILL ID axiom\n\t\t\t  | axiomaxiom  : AXIOM O_KEY instructions C_KEY rulesrules  : rule rules\n\t\t\t  | depthrule  : RULE ID O_KEY base instructions loopsbase : BASE TWO_POINT instruction_base \n\t\t\t| BASE O_KEY instructions_base C_KEYinstructions : instruction instructions\n\t\t\t\t    | instruction instruction  : LEFT  INT \n\t\t\t\t    | LEFT FLOAT    \n\t\t\t\t\t| RIGHT INT \n\t\t\t\t\t| RIGHT FLOAT     \n\t\t\t\t\t| LINE  INT   \n\t\t\t\t\t| JUMP  INT COMMA INT      \n\t\t\t\t\t| NILL  \n\t\t\t\t\t| PUSH  INT COMMA INT \t\t\n\t\t\t\t\t| POP \n\t\t\t\t\t| CALL_RULE ID\n\t\t\t\t\t| CALL_SHAPE IDinstruction_base  : LEFT  INT \n\t\t\t\t\t\t | LEFT FLOAT    \n\t\t\t\t\t\t | RIGHT INT \n\t\t\t\t\t\t | RIGHT FLOAT     \n\t\t\t\t\t\t | LINE  INT   \n\t\t\t\t\t\t | JUMP  INT COMMA INT      \n\t\t\t\t\t\t | NILL  \n\t\t\t\t\t\t | PUSH  INT COMMA INT \t\t\n\t\t\t\t\t\t | POP instructions_base : instruction_base instructions_base\n\t\t\t\t    \t | instruction_base depth  : DEPTH INTloops  : ITER INT C_KEY\n\t\t\t  | C_KEY'
    
_lr_action_items = {'SHAPE':([0,2,4,7,8,12,14,16,18,25,26,38,50,52,57,59,],[5,5,5,-4,-8,-7,-10,-12,-14,-11,-13,-9,-15,-17,-16,-45,]),'$end':([1,2,3,4,6,7,8,10,12,14,16,18,25,26,38,50,52,57,59,],[0,-2,-3,-6,-1,-4,-8,-5,-7,-10,-12,-14,-11,-13,-9,-15,-17,-16,-45,]),'DRAW':([3,4,8,10,14,16,18,25,26,38,50,52,57,59,],[9,-6,9,-5,-10,-12,-14,-11,-13,-9,-15,-17,-16,-45,]),'ID':([5,9,15,17,36,37,53,],[11,13,21,22,48,49,58,]),'PENCIL':([11,],[15,]),'FILL':([11,21,],[17,17,]),'AXIOM':([11,21,22,],[19,19,19,]),'INT':([13,24,29,30,31,32,34,54,55,56,69,72,73,74,75,77,92,93,],[20,38,41,43,45,46,47,59,60,61,81,82,84,86,87,88,94,95,]),'O_KEY':([19,58,64,],[23,62,67,]),'COMMA':([20,46,47,87,88,],[24,55,56,92,93,]),'LEFT':([23,28,33,35,41,42,43,44,45,48,49,60,61,63,66,67,71,76,78,80,82,83,84,85,86,89,94,95,],[29,29,-29,-31,-23,-24,-25,-26,-27,-32,-33,-28,-30,29,72,72,-19,-40,-42,72,-34,-35,-36,-37,-38,-20,-39,-41,]),'RIGHT':([23,28,33,35,41,42,43,44,45,48,49,60,61,63,66,67,71,76,78,80,82,83,84,85,86,89,94,95,],[30,30,-29,-31,-23,-24,-25,-26,-27,-32,-33,-28,-30,30,73,73,-19,-40,-42,73,-34,-35,-36,-37,-38,-20,-39,-41,]),'LINE':([23,28,33,35,41,42,43,44,45,48,49,60,61,63,66,67,71,76,78,80,82,83,84,85,86,89,94,95,],[31,31,-29,-31,-23,-24,-25,-26,-27,-32,-33,-28,-30,31,74,74,-19,-40,-42,74,-34,-35,-36,-37,-38,-20,-39,-41,]),'JUMP':([23,28,33,35,41,42,43,44,45,48,49,60,61,63,66,67,71,76,78,80,82,83,84,85,86,89,94,95,],[32,32,-29,-31,-23,-24,-25,-26,-27,-32,-33,-28,-30,32,75,75,-19,-40,-42,75,-34,-35,-36,-37,-38,-20,-39,-41,]),'NILL':([23,28,33,35,41,42,43,44,45,48,49,60,61,63,66,67,71,76,78,80,82,83,84,85,86,89,94,95,],[33,33,-29,-31,-23,-24,-25,-26,-27,-32,-33,-28,-30,33,76,76,-19,-40,-42,76,-34,-35,-36,-37,-38,-20,-39,-41,]),'PUSH':([23,28,33,35,41,42,43,44,45,48,49,60,61,63,66,67,71,76,78,80,82,83,84,85,86,89,94,95,],[34,34,-29,-31,-23,-24,-25,-26,-27,-32,-33,-28,-30,34,77,77,-19,-40,-42,77,-34,-35,-36,-37,-38,-20,-39,-41,]),'POP':([23,28,33,35,41,42,43,44,45,48,49,60,61,63,66,67,71,76,78,80,82,83,84,85,86,89,94,95,],[35,35,-29,-31,-23,-24,-25,-26,-27,-32,-33,-28,-30,35,78,78,-19,-40,-42,78,-34,-35,-36,-37,-38,-20,-39,-41,]),'CALL_RULE':([23,28,33,35,41,42,43,44,45,48,49,60,61,63,71,76,78,82,83,84,85,86,89,94,95,],[36,36,-29,-31,-23,-24,-25,-26,-27,-32,-33,-28,-30,36,-19,-40,-42,-34,-35,-36,-37,-38,-20,-39,-41,]),'CALL_SHAPE':([23,28,33,35,41,42,43,44,45,48,49,60,61,63,71,76,78,82,83,84,85,86,89,94,95,],[37,37,-29,-31,-23,-24,-25,-26,-27,-32,-33,-28,-30,37,-19,-40,-42,-34,-35,-36,-37,-38,-20,-39,-41,]),'C_KEY':([27,28,33,35,40,41,42,43,44,45,48,49,60,61,65,76,78,79,80,81,82,83,84,85,86,90,94,95,],[39,-22,-29,-31,-21,-23,-24,-25,-26,-27,-32,-33,-28,-30,70,-40,-42,89,-44,91,-34,-35,-36,-37,-38,-43,-39,-41,]),'ITER':([28,33,35,40,41,42,43,44,45,48,49,60,61,65,],[-22,-29,-31,-21,-23,-24,-25,-26,-27,-32,-33,-28,-30,69,]),'FLOAT':([29,30,72,73,],[42,44,83,85,]),'RULE':([39,51,68,70,91,],[53,53,-18,-47,-46,]),'DEPTH':([39,51,68,70,91,],[54,54,-18,-47,-46,]),'BASE':([62,],[64,]),'TWO_POINT':([64,],[66,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'scene':([0,2,],[1,6,]),'draws_instruction':([0,2,],[2,2,]),'shapes':([0,2,4,],[3,3,10,]),'shape':([0,2,4,],[4,4,4,]),'draws':([3,8,],[7,12,]),'draw':([3,8,],[8,8,]),'pencil':([11,],[14,]),'fill':([11,21,],[16,25,]),'axiom':([11,21,22,],[18,18,26,]),'instructions':([23,28,63,],[27,40,65,]),'instruction':([23,28,63,],[28,28,28,]),'rules':([39,51,],[50,57,]),'rule':([39,51,],[51,51,]),'depth':([39,51,],[52,52,]),'base':([62,],[63,]),'loops':([65,],[68,]),'instruction_base':([66,67,80,],[71,80,80,]),'instructions_base':([67,80,],[79,90,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> scene","S'",1,None,None,None),
  ('scene -> draws_instruction scene','scene',2,'p_scene','grammar.py',6),
  ('scene -> draws_instruction','scene',1,'p_scene','grammar.py',7),
  ('scene -> shapes','scene',1,'p_scene','grammar.py',8),
  ('draws_instruction -> shapes draws','draws_instruction',2,'p_draws_instruction','grammar.py',21),
  ('shapes -> shape shapes','shapes',2,'p_shapes','grammar.py',24),
  ('shapes -> shape','shapes',1,'p_shapes','grammar.py',25),
  ('draws -> draw draws','draws',2,'p_draws','grammar.py',28),
  ('draws -> draw','draws',1,'p_draws','grammar.py',29),
  ('draw -> DRAW ID INT COMMA INT','draw',5,'p_draw','grammar.py',32),
  ('shape -> SHAPE ID pencil','shape',3,'p_shape','grammar.py',35),
  ('pencil -> PENCIL ID fill','pencil',3,'p_pencil','grammar.py',39),
  ('pencil -> fill','pencil',1,'p_pencil','grammar.py',40),
  ('fill -> FILL ID axiom','fill',3,'p_fill','grammar.py',43),
  ('fill -> axiom','fill',1,'p_fill','grammar.py',44),
  ('axiom -> AXIOM O_KEY instructions C_KEY rules','axiom',5,'p_axiom','grammar.py',47),
  ('rules -> rule rules','rules',2,'p_rules','grammar.py',50),
  ('rules -> depth','rules',1,'p_rules','grammar.py',51),
  ('rule -> RULE ID O_KEY base instructions loops','rule',6,'p_rule','grammar.py',54),
  ('base -> BASE TWO_POINT instruction_base','base',3,'p_base','grammar.py',57),
  ('base -> BASE O_KEY instructions_base C_KEY','base',4,'p_base','grammar.py',58),
  ('instructions -> instruction instructions','instructions',2,'p_instructions','grammar.py',61),
  ('instructions -> instruction','instructions',1,'p_instructions','grammar.py',62),
  ('instruction -> LEFT INT','instruction',2,'p_instruction','grammar.py',65),
  ('instruction -> LEFT FLOAT','instruction',2,'p_instruction','grammar.py',66),
  ('instruction -> RIGHT INT','instruction',2,'p_instruction','grammar.py',67),
  ('instruction -> RIGHT FLOAT','instruction',2,'p_instruction','grammar.py',68),
  ('instruction -> LINE INT','instruction',2,'p_instruction','grammar.py',69),
  ('instruction -> JUMP INT COMMA INT','instruction',4,'p_instruction','grammar.py',70),
  ('instruction -> NILL','instruction',1,'p_instruction','grammar.py',71),
  ('instruction -> PUSH INT COMMA INT','instruction',4,'p_instruction','grammar.py',72),
  ('instruction -> POP','instruction',1,'p_instruction','grammar.py',73),
  ('instruction -> CALL_RULE ID','instruction',2,'p_instruction','grammar.py',74),
  ('instruction -> CALL_SHAPE ID','instruction',2,'p_instruction','grammar.py',75),
  ('instruction_base -> LEFT INT','instruction_base',2,'p_instruction_base','grammar.py',78),
  ('instruction_base -> LEFT FLOAT','instruction_base',2,'p_instruction_base','grammar.py',79),
  ('instruction_base -> RIGHT INT','instruction_base',2,'p_instruction_base','grammar.py',80),
  ('instruction_base -> RIGHT FLOAT','instruction_base',2,'p_instruction_base','grammar.py',81),
  ('instruction_base -> LINE INT','instruction_base',2,'p_instruction_base','grammar.py',82),
  ('instruction_base -> JUMP INT COMMA INT','instruction_base',4,'p_instruction_base','grammar.py',83),
  ('instruction_base -> NILL','instruction_base',1,'p_instruction_base','grammar.py',84),
  ('instruction_base -> PUSH INT COMMA INT','instruction_base',4,'p_instruction_base','grammar.py',85),
  ('instruction_base -> POP','instruction_base',1,'p_instruction_base','grammar.py',86),
  ('instructions_base -> instruction_base instructions_base','instructions_base',2,'p_instructions_base','grammar.py',89),
  ('instructions_base -> instruction_base','instructions_base',1,'p_instructions_base','grammar.py',90),
  ('depth -> DEPTH INT','depth',2,'p_depth','grammar.py',93),
  ('loops -> ITER INT C_KEY','loops',3,'p_loops','grammar.py',96),
  ('loops -> C_KEY','loops',1,'p_loops','grammar.py',97),
]
