from nlpcalculator.BackendCode import *

def showResult(entryQuery):
  userQuery = entryQuery.lower()
  try:
    finalResult = solveQuery(userQuery)
  except Exception as e:
    result = "Invalid query. Resolve and try again."
  else:
    result = finalResult[1] + " = " + str(finalResult[0])
  return result