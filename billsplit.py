from __future__ import print_function
from collections import defaultdict

def billsplit(persons, bills):

    accounts = dict()
    for person in persons:
        accounts[person] = 0.0

    personalBills = defaultdict(dict)

    for b in bills:
        amount = b["amount"]

        # use conversion rate
        if "conversion" in b:
            amount *= b["conversion"]

        # split bill evenly among debtors
        amountPerPerson = amount / len(b["debtors"])

        # put amount on accounts
        for debtor in b["debtors"]:
            accounts[debtor] -= amountPerPerson
            personalBill = personalBills[debtor]

            # accumulate amounts of same-named bills
            if b["name"] in personalBill.keys():
                personalBill[b["name"]] += round(amountPerPerson, 2)
            else:
                personalBill[b["name"]] = round(amountPerPerson, 2)
            # CAVE: this overwrites name, if used more than once
    #        personalBills[debtor].update({b["name"]: round(amountPerPerson, 2)})

        # lender paid money, so fill his/her account
        accounts[b["lender"]] += amount

    # make sure we are not printing or burning money
    sum = 0.0
    for a in accounts.values():
        sum += a
    assert(round(sum, 2) == 0.00)

    # use the one who paid most as accountant
    max = 0.0
    accountant = None
    for person, amount in accounts.items():
        if amount > max:
            accountant = person
            max = amount


    #print("Accountant:")
    #print("   ", accountant)
    #print()
    #print()

    # show bills sorted by lender
    lastlender = None
    sum = 0.0
    for b in sorted(bills, key=lambda k: k['lender']):
        lender = b['lender']

        conversion_rate = 1.0
        if 'conversion' in b:
            conversion_rate = b['conversion']

            # new lender
        if lastlender != lender:
            # do not print sum header for lastlender == None
            if lastlender:
                print("    -----")
                print("%9.2f total" % sum)
                print()

            lastlender = lender
            sum = 0
            print("Bills paid by %s:" % lender)

        sum += b['amount'] * conversion_rate
        print("%9.2f %s for (%s)" % (b['amount'] * conversion_rate, b['name'], ", ".join(b['debtors'])))

    if lastlender:
        print("    -----")
        print("%9.2f total" % sum)
        print()

    print("=" * 78)
    print()

    # show personal bills
    for person, bills in personalBills.items():
        print("Personal bill for %s:" % (person))

        sum = 0.0
        for name, amount in bills.items():
            print("%9.2f %s" % (amount, name))
            sum += amount
        print("    -----")
        print("%9.2f total" % sum)
        print()
    print("=" * 78)
    print()

    # show, who has to transfer money to whom
    print("Transactions:")
    for person, amount in accounts.items():

        # skip accountant
        if person == accountant:
            continue

        if amount <= 0.0:
            print("    %s -> %s: %.2f" % (person, accountant, round(-amount, 2)))
        else:
            print("    %s -> %s: %.2f" % (accountant, person, round(amount, 2)))
    print
