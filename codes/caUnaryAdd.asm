#
# Shift left register in DNA|SIMD
# @autor Lukáš Plevač <xpleva07@vutbr.cz>
# @date 12.06.2023
#

define:
    0 [AB][CD][EF]
    1 [ABC][DEF]
    2 {A}[BCDE]{F}

data:
    00022120

instructions: 
    {F*A*G*}       # mark 02 and 22
    {F*A*B*G*}     # mark 20 nothing to do here and open binding for 21
    {F*A*B*C*G*}   # mark 21
    {B*C*D*E*}     # replace old zero with 2
    {FAG} 
    {A*B*C*D*G*}   # unvrap 2 when 02
    {ABCDG} 

    {A*B*C*} {D*E*F*} # set 1

    

    #{DEF}
    
    #{FABG}  # unmark 20
    
    #{B*C*D*E*} # write 2

    #{FABCG}