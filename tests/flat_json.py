from cdapython import Q

q = Q('id = "TCGA-E2-A10A"')

q1 = q.run(verbose=True , host='http://localhost:8080')
print(q1)
# print(q1.filter("id"))
# df = q1.to_DataFrame()

# print(q1)
