import urllib
import datetime
import os
from xml.dom import minidom
from datetime import date, timedelta

#TODO parse all rates and put into buffer array
class RateConverter:

    def __init__(self):
        self.rates_filename = "rates-last90d.xml"
        self.xml_rates = minidom.parse(self.rates_filename)

    # expects billDate as String in format "Year-Month-Day" Example: "2013-09-03"
    # expects billCurrency as String containing an ISO 4217 Currency Code
    # return rate or 1 if currency Code is EUR
    def getRateInEUR(self, billDate, billCurrency):
        #return 1 if currency is EUR
        if billCurrency == "EUR":
            return 1.0

        # interface for module
        #billDate = "2013-10-03"
        rateDate = "1900-01-01"
        #billCurrency = "USD"

        # reference values
        date_currency = "EUR"
        rate = 0.0

        billDateDate = datetime.datetime.strptime(billDate, "%Y-%M-%d")
        #print billDateDate.strftime("%d.%M.%Y")
        dd = timedelta(days=1)

        #print "hello"

        # find all Cubes in XML
        daily_rates_list = self.xml_rates.getElementsByTagName('Cube')

        while (rate == 0.0):
            #print rate
            # find right Cube with time attribute
            for node in self.xml_rates.getElementsByTagName('Cube'):
                try:
                    rateDate = node.attributes['time'].value
                except KeyError:
                    i = 0

                if rateDate == billDate:
                    try:
                        date_currency = node.attributes['currency'].value
                    except KeyError:
                        i = 0

                    if billCurrency == date_currency:
                        rate = node.attributes['rate'].value

            if rate == 0.0:
                billDateDate = billDateDate - dd
                billDate = billDateDate.strftime("%Y-%M-%d")
                # determine last rate before current date by rerunning process

        return float(rate)

    #print getRateInEUR("2013-10-03","USD")

    def cleanUpRates(self):
        try:
            with open(self.rates_filename):
                remove(self.rates_filename)

        except IOError:
            pass
            #do nothing

    def receiveECBRates(self):
        ecbURL = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"
        # download rates from ECB
        try:
            urllib.urlretrieve(ecbURL, self.rates_filename)
            return 0
        except IOError:
            # download didn't work, try to use old file
            print("ECB reference conversion rates could not be retrieved from %s" % (ecbURL))
            try:
                with open(self.rates_filename):
                    print("But found old file, I'm going to use it")
                    return 0
            except IOError:
                return 4