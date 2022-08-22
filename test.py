import sys

res = []
for line in sys.stdin:
    res.append(line.rstrip('\n'))

sys.stdin.close()
sys.stdin = open('/dev/tty')

b = input()
print(res[0] + b)

#   for line in sys.stdin:
#       a = line
#       break

#   sys.stdin.close()
#   b = input()
#   print(a + b)
