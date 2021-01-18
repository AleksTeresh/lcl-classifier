ITERATED_LOGARITHMIC_TIGHT = [
    #MIS
    ({'BC', 'AA'},
    {'AAB', 'ABB', 'CCC', 'BBB'}),
    #MIS
    ({'AA', 'BC', 'AC'},
    {'CCC','AAB'})
]


ITERATED_LOGARITHMIC_UPPER_BOUND = [

    ({'AA', 'BC', 'CC'},
    {'AAC','BBB','ABB'})
]

LOGARITHMIC_TIGHT = [

    # 3 vertex coloring on latex
    ({'AB', 'AC', 'BC'},
    {'AAA','BBB','CCC'}),

    # 3 edge coloring on latex
    ({'AA', 'BB', 'CC'},{'ABC'}),


    ({'AB','CC'},
    {'AAA','BBB','AAC','BBC'})
]
LOGARITHMIC_UPPER_BOUND = [

# SOO done on latex
    ({'AC', 'BC'},
    {'ABC', 'BCC'}),

# SOO done on latex
    ({'AB','BC'},
    {'AAB','BBC'}),

# EO done on latex 1
    ({'AC','BC'},
    {'ABC','CCC'}),

# EO done on latex 2
    ({'AC','BC'},
    {'AAA','BCC'}),

# EO done on latex 2
    ({'AC','BC'},
    {'ABB','ACC'}),

# EO done on latex 2
    ({'AC','BC'},
    {'ABB','BCC'}),

# color+edgecolor done on latex 2
    ({'AC','BC','AB'},
    {'ABC'}),

# R&C
    ({'AB', 'CC'},
    {'CCB', 'ACC'}),

#    #####
#    ({'AB', 'CC'},
#    {'BCC', 'ABB'}),

# R&C
    ({'AB', 'CC'},
    {'BCC', 'AAC'}),

# R&C
    ({'AB','CC'},
    {'ABC'}),

# R&C
    ({'AB','CC'},
    {'AAB','BBC'}),

# R&C
    ({'AB','CC'},
    {'AAC','BBC'}),

# R&C
    ({'AB','CC'},
    {'AAB','BCC'}),

# R&C
    ({'AB','CC'},
    {'BCC','AAA'}),

# R&C
    ({'AB','CC'},
    {'BBC','AAA'})

]

LOGARITHMIC_LOWER_BOUND = [
# Manually checked fixed points using RE

# fixed point 1
    ({'AC', 'BB', 'CC', 'AA', 'BC'},
    {'AAB','ABC','ABB'}),

# fixed point 1
    ({'AC', 'AB', 'CC', 'BC'},
    {'AAA','BBC','BBB','ABB'}),

# fixed point 2
    ({'BB', 'CC', 'AA'},
    {'BCC','BBC','AAC','AAB'}),

# fixed point 2
    ({'BB', 'CC', 'AA'},
    {'BCC','AAC','ABB'}),

# fixed point 2
    ({'AB', 'CC'},
    {'ABB','AAA','BBB','BCC','ACC'}),
    
# fixed point 2
    ({'AB', 'CC'},
    {'AAB','AAA','BBB','BCC','AAC'}),

# fixed point 2
    ({'CC', 'BC', 'AA'},
    {'BBC','AAB','BBB','AAC','BCC'}),

# fixed point 2.5
    ({'AB', 'CC'},
    {'AAC','BBC','BBB','ABB'}),

# fixed point auto
    ({'AB', 'CC'},
    {'BCC','AAC','ABB'}),

# fixed point auto
    ({'AB', 'CC'},
    {'BCC','AAA','ABC'}),

# fixed point auto
    ({'AB', 'CC'},
    {'BBC','AAA','ABC'}),


# fixed point auto
    ({'AB', 'CC'},
    {'BCC','BBC','AAA'}),


# fixed point auto
    ({'AB', 'CC'},
    {'AAA','BBB','ABC'}),

# fixed point auto
    ({'AB', 'CC'},
    {'BCC','BBC','AAA','ABC'})
]