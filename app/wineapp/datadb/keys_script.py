HOST = "localhost"
NAME = "winedb"
USER = "root"
PASSWORD = "wineappjosephpass"

wines_dictionary = {}
wines_dictionary['1/2 bt.'] = "37,5cl"
wines_dictionary['half'] = "37,5cl"
wines_dictionary['bt.'] = "75cl"
wines_dictionary['d.mag.'] = "3,0L"
wines_dictionary['dmag.'] = "3,0L"
wines_dictionary['imp\xc3\xa9.'] = "6,0L"
wines_dictionary['imp.'] = "6,0L"
wines_dictionary['j\xc3\xa9ro.'] = "5,0L"
wines_dictionary['jero.'] = "5,0L"
wines_dictionary['mag.'] = "1,5L"
wines_dictionary['balt.'] = "12,0L"
wines_dictionary['75'] = '75cl'
wines_dictionary['600'] = "6,0L"
wines_dictionary['150'] = "1,5L"
wines_dictionary['300'] = "3,0L"
wines_dictionary['500'] = "5,0L"
wines_dictionary['37.5'] = "37,5cl"
wines_dictionary['1200'] = "12,0L"
wines_dictionary['1500'] = "15,0L"
wines_dictionary['bt'] = "75cl"
wines_dictionary['dm'] = "3,0L"

negoces_dictionary = {}
negoces_dictionary["ballande"] = {}
negoces_dictionary["twins"] = {}
negoces_dictionary["diva"] = {}
negoces_dictionary["dubos"] = {}
negoces_dictionary["joanne"] = {}
negoces_dictionary["rca"] = {}

negoces_dictionary["ballande"]["column"] = ["appellation","produit","classement","millesime","PV_mini",
                                           "dispo","centil","parker","w"]
negoces_dictionary["ballande"]["wine"] = "produit"
negoces_dictionary["ballande"]["price"] = "PV_mini"
negoces_dictionary["ballande"]["year"] = "millesime"
negoces_dictionary["ballande"]["region"] = "appellation"
negoces_dictionary["ballande"]["format"] = "centil"
negoces_dictionary["ballande"]["currency"] = "euro"

negoces_dictionary["twins"]["column"] = ["Commune","ranking","Year","wine","Size","parker","price","Notes",
                                         "Year 2","wine (second / white)","Bottle","price 2","empty",
                                         "parker 2"]
negoces_dictionary["twins"]["wine"] = "wine"
negoces_dictionary["twins"]["price"] = "price"
negoces_dictionary["twins"]["year"] = "Year"
negoces_dictionary["twins"]["region"] = "Commune"
negoces_dictionary["twins"]["format"] = "Size"
negoces_dictionary["twins"]["currency"] = "euro"

negoces_dictionary["diva"]["column"] = ["Num","Vintage","Wine","Appelation","Color","Classement",
                                        "Quantity","Volume","Packaging","Price","Parker"]
negoces_dictionary["diva"]["wine"] = "Wine"
negoces_dictionary["diva"]["price"] = "Price"
negoces_dictionary["diva"]["year"] = "Vintage"
negoces_dictionary["diva"]["region"] = "Appelation"
negoces_dictionary["diva"]["format"] = "Volume"
negoces_dictionary["diva"]["currency"] = "euro"

negoces_dictionary["dubos"]["column"] = ["Num","Vint.","Chateau","Format","Comment","Appellation","Qty",
                                         "N1","N2","Price","Parker","Decanter","WS","JS"]
negoces_dictionary["dubos"]["wine"] = "Chateau"
negoces_dictionary["dubos"]["price"] = "Price"
negoces_dictionary["dubos"]["year"] = "Vint."
negoces_dictionary["dubos"]["region"] = "Appellation"
negoces_dictionary["dubos"]["format"] = "Format"
negoces_dictionary["dubos"]["currency"] = "euro"

#negoces_dictionary["joanne"]["column"] = ["Num","Color","Wine","Appelation","Price","N1","Neal Martin","N2",
#                                          "Wine Spectator","N3","Vinous","N4","J. Suckling","N5",
#                                          "Wine Enthousiast","N6","R. Gabriel","N7","Decanter"]
#negoces_dictionary["joanne"]["wine"] = "Wine"
#negoces_dictionary["joanne"]["price"] = "Price"
#negoces_dictionary["joanne"]["year"] = "Price"

negoces_dictionary["rca"]["column"] = ["Appellation","Classificat","Wine","Vint","cl","Qty",
                                       "Euros","RP","N1"]
negoces_dictionary["rca"]["wine"] = "Wine"
negoces_dictionary["rca"]["price"] = "Euros"
negoces_dictionary["rca"]["year"] = "Vint"
negoces_dictionary["rca"]["region"] = "Appellation"
negoces_dictionary["rca"]["format"] = "cl"
negoces_dictionary["rca"]["currency"] = "euro"

