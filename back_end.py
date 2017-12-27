'''
/*************************************************************************
/
/           Source code created by:
/           Nicholas Lockhart
/           Algonquin College Student
/           For the Shopify Back-end internship challenege
/           nrlockhart@gmail.com
/
/*************************************************************************
'''
import urllib
import json 
import requests

#intialization
output = {}
page = 1
invalid_Menus = []
valid_Menus = []
roots = []
menus = []

endPoint = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json"

inputa = raw_input("Do you want the Main Challenge output or the Extra Challenge output? Type main or extra.\n")

if(inputa.lower() == "main"):
    endPoint = endPoint + "?id=1"
elif(inputa.lower() == "extra"): 
    endPoint = endPoint + "?id=2"
else:
    print("Sorry, you have got to be better at following instructions.")
    exit(0)


#get the pagination information for iteration and creation of full set of the menus
responseMain = json.loads(requests.get(endPoint).text)
pagination = responseMain["pagination"]

#creating the full set of menus for processing
while((pagination.get("total")/pagination.get("per_page")) >= page):
    urlstring = endPoint + "&page=" + str(page)
    response = json.loads(requests.get(urlstring).text)
    for obj in response["menus"]:
      menus.append(obj)  
    page += 1


#goes through menus list of dictionaries creating a list of root menus and their child ids
#appends submenus to the roots child menus
for obj in menus:
    root_id = obj["id"]
    child_ids = obj["child_ids"]
    if("parent_id" not in obj):
        rootItem = {"root_id": root_id, "children": child_ids}
        roots.append(rootItem.copy())
    else:
        for r in roots:
            if(obj["parent_id"] == r["root_id"]):
                r["children"].extend(obj["child_ids"])
            if(obj["parent_id"] in r["children"]):
                r["children"].extend(obj["child_ids"])


for r in roots:
    r["children"] = [x for x in r["children"] if x != []]
    if(r["root_id"] in r["children"]):
        invalid_Menus.append(r)
        continue
    if(len(r["children"]) > 4):
        invalid_Menus.append(r)
    else:
        valid_Menus.append(r)

output ["valid_menus"] = valid_Menus
output ["invalid_menus"] = invalid_Menus
jsonOutput = json.dumps(output)
print(jsonOutput)



        

            
