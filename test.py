from sys import stdout
from time import sleep

for count in range(0, 10):
  print(count + 1)
  stdout.flush()
  sleep(0.5)