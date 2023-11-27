#
# RULE 110 cellular automaton implementation in DNA|SIMD
# @autor Lukáš Plevač <xpleva07@vutbr.cz>
# @date 11.21.2023
#

define:
    0 {A}[BCD][EF]
    1 {A}{BCD}[EF]

data:
    01

instructions:
    # need mark for 10 and 01
    {G*E*F*A*}     # mark 01
    #{GEFA}         # remove mark 01
    #{B*C*D*E*}     # write 1