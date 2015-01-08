'''
Created on Jun 8, 2013

@author: emma_ping
'''
import sys
import getopt
import diff
def usage():
    print "AutoEtl.py -c <counter> -o <outputfile> <inputfile1> <inputfile2> "

def AutoEtl(argv=None):
    try:
        opts, args = getopt.getopt(argv,"hc:o:", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
        
    etl1,etl2 = args  
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-c", "--counter"):
            counter = arg
        elif opt in ("-o", "--ofile"):
            output = arg
    
    diff.main(etl1, etl2 ,counter, output)
if __name__ == '__main__':
    AutoEtl(sys.argv[1:])