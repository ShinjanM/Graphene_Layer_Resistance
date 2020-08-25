operator_list = set('PSD')

def resistance(circuit):
  temp = circuit.split(" ")
  stack = []
  for char in temp:
      if char in operator_list:
          a = new_resistance(stack.pop(), stack.pop(), char)
          print(a)
          stack.append(a)
      else:
          print(char)
          stack.append(char)
  return stack[-1]

def new_resistance(a,b,c):
  if c == 'P':
      if float(a) == 0 or float(b) == 0:
          return 0
      else:
          return 1/(1/float(a) + 1/float(b))
  else:
      return float(a) + float(b)

circuit = input('Enter the circuit : ')
resistance(circuit)
