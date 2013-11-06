import urllib
import datetime
from xml.dom import minidom
from datetime import date, timedelta
from collections import defaultdict

#TODO parse all rates and put into buffer array
class RateConverter:

    def __init__(self):
        self.rates_filename = "rates-last90d.xml"
        self.xml_rates = minidom.parse(self.rates_filename)

        # Get first cube node
        # Skip gesmes nodes
        parentCubeNode = self.xml_rates.firstChild.childNodes[2]

        self.currencies = defaultdict(lambda: dict())

        for dateNode in parentCubeNode.childNodes:
            if dateNode.nodeType == minidom.Node.ELEMENT_NODE:
                date = str(dateNode.attributes['time'].value)
                for currencyNode in dateNode.childNodes:
                    if currencyNode.nodeType == minidom.Node.ELEMENT_NODE:
                        currency = str(currencyNode.attributes['currency'].value)
                        rate = float(currencyNode.attributes['rate'].value)
                        self.currencies[date][currency] = rate

    # expects billDate as String in format "Year-Month-Day" Example: "2013-09-03"
    # expects billCurrency as String containing an ISO 4217 Currency Code
    # return rate or 1 if currency Code is EUR
    def getRateInEUR(self, billDate, billCurrency):

        #return 1 if currency is EUR
        if billCurrency == "EUR":
            return 1.0

        print billDate
        billDateDate = datetime.datetime.strptime(billDate, "%Y-%M-%d")
        dd = timedelta(days=1)

        # Look for conversion rate on day itself or at most 7 days in advance
        tries = 0
        while (not billDate in self.currencies) and tries < 7:
            billDateDate = billDateDate - dd
            billDate = billDateDate.strftime("%Y-%M-%d")
            tries += 1

        if tries == 7:
            raise IOError("Could not find conversion in week before date")

        rate = self.currencies[billDate][billCurrency]

        return rate

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