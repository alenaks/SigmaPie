"""
   SigmaPie: a toolkit for subregular grammars and languages.
   Copyright (C) 2019  Alena Aksenova

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
"""

from sigmapie.sl_class import *
from sigmapie.tsl_class  import *
from sigmapie.mtsl_class import *
from sigmapie.sp_class import *
from sigmapie.ostia import *

print(
    "\nYou successfully loaded SigmaPie. \n\n"
    "Formal language classes and grammars available:\n"
    "\t* strictly piecewise: SP(alphabet, grammar, k, data, polar);\n"
    "\t* strictly local: SL(alphabet, grammar, k, data, edges, polar);\n"
    "\t* tier-based strictly local: TSL(alphabet, grammar, k, data, edges,"
    " polar, tier);\n"
    "\t* multiple tier-based strictly local: MTSL(alphabet, grammar, k, "
    "data, edges, polar).\n\n"
    "Alternatively, you can initialize a transducer: "
    "FST(states, sigma, gamma, initial, transitions, stout).\n"
    "Learning algorithm:\n"
    "\tOSTIA: ostia(sample, sigma, gamma)."
)
