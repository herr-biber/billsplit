#!/usr/bin/env python

from collections import defaultdict
from bill import * # import the bill file

accounts = dict()
for person in all:
    accounts[person] = 0.0
    
personalBills = defaultdict(dict)

for b in bills:
    # split bill evenly among deptors
    amountPerPerson = b["amount"] / len(b["deptors"])

    # put amount on accounts
    for deptor in b["deptors"]:
        accounts[deptor] -= amountPerPerson
        personalBill = personalBills[deptor]
        
        # accumulate amounts of same-named bills
        if b["name"] in personalBill.keys():
            personalBill[b["name"]] += round(amountPerPerson, 2)
        else:
            personalBill[b["name"]] = round(amountPerPerson, 2)
        # CAVE: this overwrites name, if used more than once
#        personalBills[deptor].update({b["name"]: round(amountPerPerson, 2)})
        
    # lender paid money, so fill his/her account
    accounts[b["lender"]] += b["amount"]
    
# make sure we are not printing or burning money
sum = 0.0
for a in accounts.values():
    sum += a
assert(round(sum, 2) == 0.00)

# use the one who paid most as accountant
max = 0.0
accountant = accounts.iterkeys().next()
for person, amount in accounts.items():
    if amount > max:
        accountant = person
        max = amount


#print "Accountant:"
#print "   ", accountant
#print
#print

# show personal bills
for person, bills in personalBills.items():
    print "Personal bill for %s:" % (person)
    
    sum = 0.0
    for name, amount in bills.items():
        print "%9.2f %s" % (amount, name)
        sum += amount
    print "    -----"
    print "%9.2f total" % (sum)
    print
print
    
# show, who has to transfer money to whom
print "Transactions:"
for person, amount in accounts.items():

    # skip accountant
    if person == accountant:
        continue
    
    if amount <= 0.0:
        print "    %s -> %s: %.2f" % (person, accountant, round(-amount, 2))
    else:
        print "    %s -> %s: %.2f" % (accountant, person, round(amount, 2))
print
