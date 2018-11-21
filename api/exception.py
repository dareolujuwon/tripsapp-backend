# for d in range(0, len(data)):
#     if content['primaryid'] == data[d]['primaryid']:
#         updated_entry = {
#                         "datetime" : content['datetime'],
#                         "description" : content['description'],
#                         "elevation" : content['elevation'],
#                         "id" : content['id'],
#                         "latitude" : content['latitude'],
#                         "longitude" : content['longitude'],
#                         "primaryid" : data[d]['primaryid']
#                     }
#         data.pop(d)
#         data.append(updated_entry)
#         break