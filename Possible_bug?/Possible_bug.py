import pickle,cvxpy,numpy

pickle_in = open("Matrix_of_Constraints","rb")

CONSTRAINTS = pickle.load(pickle_in)
x= cvxpy.Variable(26)
list_of_constraints=[x>=0]

obj = cvxpy.Minimize(cvxpy.pnorm(x,1))

for i in range(len(CONSTRAINTS)):
    list_of_constraints.append(1 <= numpy.transpose(CONSTRAINTS[i])*x)

prob = cvxpy.Problem(obj, list_of_constraints)   
y=prob.solve()
print(x.value)