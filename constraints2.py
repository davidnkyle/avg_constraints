def m2i(m1, m2= None):
    if m2 == None:
        return [(m1 - 9)%12]
    return range((m1 - 9)%12, (m2 - 9)%12 + 1)

##
# initial balance fixed
#
ibfd = {'emilys checking and savings account': 10000,
        'davids checking and savings account': 5000,
        'mom and dad last semester fund':      4500
        }
init_bal = sum(ibfd.values())

# initial balance variable (YAGNI)

# savings fixed (YAGNI)

##
# savings variable
#
svd = {'two months rent': [4000, m2i(9,8)],
       'extra months rent': [2000, m2i(8)]
       }

##
# income fixed
#
ifd = {'northrop fall': [640, m2i(9,11)],
       'northrop spring': [800, m2i(1,8)]
       }

# income variable (YAGNI)

##
# expenses fixed
#

##
# expenses variable
#
