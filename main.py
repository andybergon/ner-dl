import time
import read_training as rt
import distribution_calculator as dc

start = time.clock()
# print(start)

# substitute_midnames()
# substitute_midnames_partial()
# substitute_midnames_in_memory()
# print get_id_by_token('{m.03cd5dk:45037:45040}')
# print rt.get_all_entity_properties_by_id('m.0c3dqq3')
# print search_midname('m.01000036')
print dc.count_types()

end = time.clock()
# print(end)

print(str(end - start) + ' seconds')