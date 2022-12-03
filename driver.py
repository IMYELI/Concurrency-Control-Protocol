from datatype.transaction_manager import Transaction_Manager
from simple_locking import simpleLocking
import sys

print("1. Simple Lock(Exclusive Lock Only)")
print("2. OCC")
print("3. MVCC")
protocol = int(input("Choose the protocol(1-3): ").strip())

trans = Transaction_Manager( "test5.txt")

if(protocol == 1):
    simpleLocking(trans)
elif(protocol == 2):
    """OCC()"""
elif(protocol == 3):
    """MVCC()"""
else:
    print("Error: there's no such protocol. Exiting...")
    sys.exit()
