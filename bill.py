#!/usr/bin/env python2
from billsplit import billsplit

all = ["MR", "JS", "MH", "PT", "JR"]

bills = [
    {
        'name':    "Geschenk Micha",
        'lender':  "MR",
        'debtors': all,
        'amount':  38.99+1.37,
        'comment': "Ardberg + Chinaplastik"
    },
    {
        'name':    "Tanken Berlin",
        'lender':  "MR",
        'debtors': ["MR", "JS", "PT", "JR"],
        'amount':  68.63,
        'comment': ""
    },
    {
        'name':    "Tanken Weinsberg 1",
        'lender':  "MR",
        'debtors': all,
        'amount':  87.17,
        'comment': ""
    },
    {
        'name':    "Tanken Weinsberg 2",
        'lender':  "MR",
        'debtors': all,
        'amount':  30.03,
        'comment': "Weinsberg - KA - Weinsberg"
    },
    {
        'name':    "Kaufland Weinsberg",
        'lender':  "MR",
        'debtors': all,
        'amount':  0.55+1.25+2.49+1.05+0.45,
        'comment': "Baguette, Salat, ..."
    },
    {
        'name':    "Kaufland Weinsberg",
        'lender':  "MR",
        'debtors': ["PT"],
        'amount':  14.8/10.0+2.4+0.57+3.77/4.0,
        'comment': "Bier, Milch, Bananen, Steak"
    },
    {
        'name':    "Kaufland Weinsberg",
        'lender':  "MR",
        'debtors': ["MH"],
        'amount':  14.8/20.0+3.77/2.0,
        'comment': "Bier, Steaks"
    },
    {
        'name':    "Kaufland Weinsberg",
        'lender':  "MR",
        'debtors': ["MR", "JS"],
        'amount':  14.8*17.0/20.0+3.10,
        'comment': "Bier, Pfand"
    },
    {
        'name':    "KVV Ticket",
        'lender':  "JS",
        'debtors': ["MR", "JS", "JR"],
        'amount':  25.00,
        'comment': ""
    },
]

billsplit(all, bills)