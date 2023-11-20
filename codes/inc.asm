#
# 1 2 3 4 5 6 7 8
# A B C D E F G H
#

define:
    0 [ABC][DE]
    1 [AB][CDE]

data:
    1011{FT} # {FT} is TUE BINDING hold

instructions:
    # mark last if is 1 if exist and replace this and open base C
    #
    #                                               /
    # - > - - > - - > - > - > - - > - >   - - - - /  
    # | | | | | | | | | | | | | | | | |   | | | | |  
    # - - - - - - - - - - - - - - - - - - - - - - -  
    # A B C D E A B C D E A B C D E A B C D E A B C  
    #
    # if next bit is 1 it again replace this and open base C this is chain reaction
    #
    {D*E*F*T*G*}   {D*E*A*B*C*H*}

    # remove all markers
    {DEFTG}        {DEABCH}

    # set 1 end this unvrap last 0
    {C*D*E*}

    # shift 1 end to center of register cell if possible to by eble of unvrap by 0
    {B*C*D*}

    # set 0
    {ABC} {DE}

    # remove last 0
    {ABC}

    # set last 0 to 1
    {A*B*}