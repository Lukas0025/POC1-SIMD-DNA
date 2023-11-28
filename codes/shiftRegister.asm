#
# Selected NOT in DNA|SIMD
# @autor Lukáš Plevač <xpleva07@vutbr.cz>
# @date 11.27.2023
#

define:
    #   BIT     NOT selector
    0 [ABC][DE][NSE].<U*>
    1 [ABCD]{E}[NSE].<U*>

data:
    #    Implicit zero
    00110[ABC][DE][NSE]
    #01100[ABC][DE][NSE]
    #11000[ABC][DE][NSE]
    00000[ABC][DE][NSE]
    11111[ABC][DE][NSE]

instructions: # O(34)
    {NSEU}           # remove all notselectors selector
    {D*E*N*}
    {DEN}
    {E*N*S*E*A*}
    {D*E*N*S*E*G*}
    {ENSEA}
    {E*N*S*E*A*B*}
    {ENSEAB}
    {E*N*S*E*I*}     # bind not selector for 11
    {N*S*E*A*B*C*F*}
    {DENSEG}
    {NSEABCF}
    {D*E*N*S*E*A*B*}
    {DENSEAB}
    {E*N*S*E*Y*}
    {B*C*D*}
    {DENSEAB}
    {ENSEI}          # remove temp not selector for 11
    {N*S*E*U*}   # bind not selector for 00
    {ENSEY}
    {A*B*C*}     # write zero back
    {D*E*}       # second zero part
    # selected not subprogram
    {G*D*E*N*}         # mark NOT 0 and NOT 1
    {ABCD}             # remove unwraped 1
    {GDEN}             # remove mark
    {C*D*E*N*}         # mark write 0
    {CDEN}             # remowe mark write 0 (is only posible when is unvraped for second part of zero)
    {A*B*C*D*}         # write 1
    {ABCD}             # remove not writed 1 (is unwraped by mark write 0)
    {N*S*E*G*}         # unwrap write 0 mark
    {CDEN}             # remove write 0 mark
    {NSEG}             # remove unwraper
    {A*B*C*} {D*E*}    # write 0
    {N*S*E*U*}         # lock all NOT selectors

    