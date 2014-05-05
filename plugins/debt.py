from util import hook, http, text, web
import json

@hook.command(autohelp=False)
def debt(inp):
    """debt -- returns the us national debt"""
    href = "http://www.nationaldebtclocks.org/debtclock/unitedstates"
    results = http.get_html(href)
    debt = results.xpath("//span[@id='debtDisplayFast']/text()")[0]
    householdshare = results.xpath("//span[@id='SCS']/text()")[0]

    return("Current US Debt: \x02${:,}\x02 - Amount Per Citizen: \x02{}\x02".format(int(debt), householdshare))