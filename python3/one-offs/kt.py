# Keyboard Transform code take-home quiz

# Write a keyboard that maintains a 10x4 subset of the keyboard:
# 1 - 0
# q - p
# a - ;
# z - /

# Apply the following transforms:
# H - horizontal flip
# V - vertical flip
# N - shift keys to the right -N or +N

# Take in any amount or order of options (HVN)

# Produce transformed string

##

# import modules
import sys

# Set up variables
Subset = (('0','1','2','3','4','5','6','7','8','9','0'), \
        ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'), \
        ('a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'), \
        ('z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'))

# class to perform the different transforms on single items
class transform:

    def __init__(self, Option, Value):
        
        self.option = Option
        self.value = Value

        for Row in Subset:
            if self.value in Row:
                self.row = Subset.index(Row)
                self.index = Row.index(self.value)

    def h_flip(self):
    
        return Subset[self.row][::-1][self.index]

    def v_flip(self):

        return Subset[::-1][self.row][self.index]

    def n_shift(self):
        if (self.index + self.option) > 9:
            return Subset[self.row][(self.index - 1) + (self.option % 10)]
        elif (self.index + self.option) < 0:
            return Subset[self.row][(self.index - 1) + (self.option % -10)]
        return Subset[self.row][self.index + self.option]

# function to process string input
def process_string(Input, Args):
    '''
    To run from python shell as module:
      import kt
      kt.process_string(<string>, [<options>])
      
      Options must be entered as a list
    '''
    Output = []
    for Value in Input:
        if any(Value in X for X in Subset):
            new_value = Value
            for Arg in Args:
                try:
                    run_transform = transform(Arg, new_value)
                except:
                    return '[transform error]' + str(sys.exc_info()[1])

                if Arg == 'h' or Arg == 'H':
                    try:
                        new_value = run_transform.h_flip()
                    except:
                        return '[Option H Transform Error]: ' + str(sys.exc_info()[1])
                elif Arg == 'v' or Arg == 'V':
                    try:
                        new_value = run_transform.v_flip()
                    except:
                        return '[Option V Transform Error]: ' + str(sys.exc_info()[1])
                elif any(X in list(Arg) for X in ['+', '-']):
                    try:
                        new_value = transform(int(Arg), new_value).n_shift()
                    except:
                        return '[Option +/-N Transform Error]: ' + new_value + str(sys.exc_info()[1])
                else:
                    return f'[Bad Option]: {Arg}'
            Output.append(new_value)
        else:
            Output.append(Value)
    return ''.join(Output)

# Run from terminal
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Keyboard Transformer', prog='kt')
    parser.add_argument('-s', action='store', required=True, help='The string to transform')
    parser.add_argument('-o', action='store', required=True, help='Comma seperated options to transform the string: H (flip horizontally), V (flip vertically), +/-N (move up or down N spots)') 
    parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Get current version of kt, the keyboard transformer.')

    args = parser.parse_args()

    try:
        Output = process_string(str(args.s), args.o.split(','))
    except:
        print(f'[ArgParse Error]: {sys.exc_info()[1]}')
    print(Output)
