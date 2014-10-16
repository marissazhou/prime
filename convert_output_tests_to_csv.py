import sys

def main():
  '''
  This script converts marissa's test output file to CSV format, printing out
  all items outside a certain tolerance
  '''
  if len(sys.argv)<2:
    print "\n Invalid input, please enter at least 1 parameter"
    sys.exit(0)
  #store command line arguments to local variables
  input_file = sys.argv[1]
  distance_threshold = 0.5
  if len(sys.argv) > 2:
    distance_threshold = float(sys.argv[2])
  raw_reader = open(input_file,'rU')
  output_file = open(input_file.replace('.txt','.csv'), 'w')
  line = ''
  '''
  test			:0
  init death averted	:0E-9
  python death total 	:258843.0
  python death averted 	:-5.82076609135e-11
  distance			:5.82076609135e-11
  passed:True
  '''
  init_death_averted = ''
  python_death_total = ''
  python_death_averted = ''
  distance = 0.1
  passed = ''
  for i in range(320):
    line = raw_reader.readline().split(':')[1][:-1]
    init_death_averted = raw_reader.readline().split(':')[1][:-1]
    python_death_total = raw_reader.readline().split(':')[1][:-1]
    python_death_averted = raw_reader.readline().split(':')[1][:-1]
    distance = float(raw_reader.readline().split(':')[1][:-1])
    passed = raw_reader.readline().split(':')[1][:-1]
    if distance < -distance_threshold or distance > distance_threshold:
      output_file.write(line + ',' + init_death_averted + ',' + python_death_total + ',' + python_death_averted + ',' + str(distance) + ',' + passed +'\n')
  raw_reader.close()
  output_file.close()
    
"""
Standard boilerplate to call the main() function to begin the program.
"""
if __name__ == '__main__': 
    main() #Standard boilerplate to call the main() function to begin the program.
