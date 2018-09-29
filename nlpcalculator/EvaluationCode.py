from nlpcalculator.KeywordsList import *

class Stack:
  def __init__(self):
    self.items = []

  def isEmpty(self):
    return self.items == []

  def push(self, item):
    self.items.append(item)

  def pop(self):
    return self.items.pop()

  def peek(self):
    return self.items[len(self.items)-1]

  def size(self):
    return len(self.items)

  def clear(self):
    while not self.isEmpty():
      self.pop()
         

latestOperator = Stack()
latestOperand = Stack()

def applyOperator(list):
  LB = 0
  currentState = 1
  finalList = []
  topOperator = []
  for i, token in enumerate(list):
    if token[1] == 'SYM':
      latestOperator.push(token)
      if (list[i+1][1] != 'SYM') and (list[i+1][0] != 'by') and (list[i+1][1] != 'CD'):
        token = [token[0], '$']
    elif token[1] == 'IN':
      token = [token[0], '$']
    elif token[1] == '-LRB-':
      LB = LB + 1
      if LB > 0:
        currentState = 1
    elif token[1] == '-RRB-':
      LB = LB - 1
      if LB <= 0:
        currentState = 2
    elif token[1] == 'CC':
      if not latestOperator.isEmpty():
        topOperator = latestOperator.pop()
        token = topOperator
      else:
        if currentState == 1:
            token = topOperator#previously token = ['+', 'SYM'] if topOperator wasn't ['/', 'SYM'], else: token = topOperator		  
        elif currentState == 2:
          token = ['+', 'SYM']
    if token[1] != '$':
      finalList.append(token[0])
    	
  return finalList    

def createExpression(list):
  countOperator = 0
  countOperand = 0
  finalList = []
  type = 0
  for token in list:
    if token[1] == 'IN':
      type = 1
      break	
  for token in list:
    if token[1] == 'SYM':
      countOperator = countOperator + 1
    elif token[1] == 'CD':
      countOperand = countOperand + 1		
  if type == 1:
    list = applyBracket(list)
    print("\n")
    print("----------------------------------------INITIAL LIST--------------------------------------------")
    initialList = []
    for token in list:		
      initialList.append(token[0])
    print(initialList)
    print("------------------------------------------------------------------------------------------------")    
	
    if countOperand - countOperator < 1:
      raise ValueError("Too few operands.")    
	
    finalList = applyOperator(list)	
    print("\n")
    print("-------------------------------------------FINAL LIST-------------------------------------------")
    print(finalList)
    print("------------------------------------------------------------------------------------------------")
  
  else:
    LB = 0
    RB = 0
    for token in list:
      if token[1] == '-LRB-':
        LB = LB + 1	
      if token[1] == '-RRB-':
        LB = LB - 1			
    while LB > 0:
      list.append([')', '-RRB'])
      LB = LB - 1

    i = 0
    RB = 0
    for i in range(len(list)-1, -1, -1):
      if list[i][1] == '-RRB-':
        RB = RB + 1
      elif list[i][1] == '-LRB-':
        RB = RB - 1
        print(i, "--RB",RB)
      i = i + 2
    while RB > 0:
      list.insert(0, ['(', '-LRB-'])
      RB = RB - 1
	  
    print("\n")
    print("------------------------------------------INITIAL LIST------------------------------------------")
    initialList = []
    for token in list:
      initialList.append(token[0])
    for i, token in enumerate(initialList):
      if initialList[i] == 'and':
        initialList[i] = '+'
    print(initialList)
    print("------------------------------------------------------------------------------------------------") 
	
    if countOperand - countOperator < 1:
      raise ValueError("Too few operands.")    
	  
    finalList = initialList
    print("\n")
    print("-------------------------------------------FINAL LIST-------------------------------------------")
    print(finalList)
    print("------------------------------------------------------------------------------------------------") 

  return finalList

  
def applyBracket(list):
  ctr = 0
  LB = 0
  RB = 0
  currentState = 1
  i = 0
  lastSeenOperator = '('
  lenList = len(list)
  while i < lenList:
    if list[i][1] == 'IN':
      if currentState == 1:
        list.insert(i+1,['(', '-LRB-'])
        lenList = lenList + 1
      elif currentState != 1:
        currentState = 1
        list.insert(i+1,['(', '-LRB-'])
        lenList = lenList + 1
      LB = LB + 1
      i = i + 2
	  
    elif list[i][1] == 'CD':
      if currentState == 1:
        currentState = 2
      elif currentState == 2:
        currentState = 3
        list.insert(i+1,[')', '-RRB-'])
        lenList = lenList + 1
        LB = LB - 1
      elif currentState == 3:
        currentState = 3
        list.insert(i+1,[')', '-RRB-'])
        lenList = lenList + 1
        LB = LB - 1
      i = i + 2
	  
    else:
      i = i + 1

  while LB > 0:
    list.append([')', '-RRB'])
    LB = LB - 1
 
  i = 0	
  for i in range(len(list)-1,-1, -1):
    if list[i][1] == '-RRB-':
      RB = RB + 1
    elif list[i][1] == '-LRB-':
      RB = RB - 1
    i = i + 2
  while RB > 0:
    list.insert(0, ['(', '-LRB-'])
    RB = RB - 1
  return list

def convertInfixToPostfix(list):
  postfixList = []
  operatorStack = Stack()
  for token in list:
    if token == '(':
      operatorStack.push(token)
    elif token in ['*', '/', '+', '-', '--']:
      while (not operatorStack.isEmpty()) and (precedence[operatorStack.peek()] >= precedence[token]):
        postfixList.append(operatorStack.pop())
      operatorStack.push(token)
    elif token == ')':
      topToken = operatorStack.pop()
      while topToken != '(':
        postfixList.append(topToken)
        topToken = operatorStack.pop()
    else:
      postfixList.append(token)
	  
  while not operatorStack.isEmpty():
    postfixList.append(operatorStack.pop())
		
  print("\n")
  print("------------------------------------------POSTFIX LIST------------------------------------------")
  print(postfixList)
  print("------------------------------------------------------------------------------------------------") 

  return postfixList
  
def evaluatePostfix(list):
  operandStack = Stack()
  operand1 = 0
  operand2 = 0
  expression = str()
  result = 0
  for token in list:
    if not token in ['*', '/', '+', '-', '--']:
      operandStack.push([token, str(token)])
    else:
      operand2 = operandStack.pop()
      operand1 = operandStack.pop()
		
      if token == '*':
        expression = "( " + operand1[1] + " * " + operand2[1] + " ) "
        result = operand1[0] * operand2[0]
      elif token == '/':
        expression = "( " + operand1[1] + " / " + operand2[1] + " ) "
        result = operand1[0] / operand2[0]
      elif token == '+':
        expression = "( " + operand1[1] + " + " + operand2[1] + " ) "
        result = operand1[0] + operand2[0]
      elif token == '-':
        expression = "( " + operand1[1] + " - " + operand2[1] + " ) "
        result = operand1[0] - operand2[0]
      elif token == '--':
        expression = "( " + operand2[1] + " - " + operand1[1] + " ) "
        result = operand2[0] - operand1[0]
      operandStack.push([result, expression])
  
  result = operandStack.pop()
  
  
  print("\n")
  print("-------------------------------------------RESULT-----------------------------------------------")
  print(result)
  print("------------------------------------------------------------------------------------------------") 
  return result  
  
def evaluateQuery(list):
  latestOperand.clear()
  latestOperator.clear()
  reqExpression = str()
  infixExpression = createExpression(list)
  postfixExpression = convertInfixToPostfix(infixExpression)
  result = evaluatePostfix(postfixExpression)
  return result

