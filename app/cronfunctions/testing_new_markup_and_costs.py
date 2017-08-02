from dbfeeder import updatedb

prices = [1000,1500,3062.15,141.73]

def getCostsAndMarkup(table_obj):
    costs_table = 'costs_costs'
    markup_table = 'costs_markup'
    
    unit_costs = table_obj.getValues("value",costs_table)
    unit_costs_type = table_obj.getValues("valuetype",costs_table)

    fixed_markup = table_obj.getValues("value",markup_table)

    costs_dictionary = {}
    costs_dictionary["%"] = []
    costs_dictionary["HK$"] = []
    for unit_cost,unit_cost_type in zip(unit_costs,unit_costs_type):
        if unit_cost_type == "%":
            costs_dictionary["%"].append(unit_cost)
        elif unit_cost_type == "HK$":
            costs_dictionary["HK$"].append(unit_cost)
    return costs_dictionary,fixed_markup[0]


table_obj = updatedb()
costs_dictionary,fixed_markup = getCostsAndMarkup(table_obj)

for price in prices:
    print price
    for unit_cost in costs_dictionary["HK$"]:
        price = float(price) + float(unit_cost.replace("HK$",""))
    price_after_markup = float(price) * (1 + float(fixed_markup.replace("%",""))/100.0)
    print price_after_markup
    percent = 0
    for unit_cost in costs_dictionary["%"]:
        percent += float(unit_cost.replace("%",""))/100.0
    price_after_markup = float(price_after_markup) / (1.0 - percent)
    print percent
    print price_after_markup
    print
