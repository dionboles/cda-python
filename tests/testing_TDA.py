from cdapython import Q

q1 = Q('subject_associated_project = "TCGA-OV"')
r = q1.run(host="http://localhost:8080")
print(r)
