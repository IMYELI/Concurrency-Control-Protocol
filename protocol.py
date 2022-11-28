import sys

class Protocol:

    """Protocol used for concurrency control"""
    protocol = None    
    
    """List of transactions need to be done"""
    trans = []

    """dictionary to keep track of transaction"""
    trans_dict = {}

    """Transaction that is currently executed"""
    exec_trans = []

    """Transaction turn now"""
    turn = 0

    def __init__(self, chosen_protocol, transaction):
        self.chooseProtocol(chosen_protocol)
        self.getTransaction(transaction)

    def chooseProtocol(self, string):
        if(string == "Simple Locking"):
            self.protocol = None 
            """Simple_Locking()"""
        elif(string == "OCC"):
            self.protocol = None
            """OCC()"""
        elif(string == "MVCC"):
            self.protocol = None
            """MVCC()"""
        elif(string == "prototype"):
            pass
        else:
            print("Error: there's no such protocol. Exiting...")
            sys.exit()
        
    def getTransaction(self,transaction):
        #Reading file
        f = open(transaction,"r")
        self.trans = f.readlines()
        for i in range(len(self.trans)):
            #Remove \n from line
            self.trans[i] = self.trans[i].rstrip("\n").split()
            self.trans_dict[i] = self.trans[i]
    
    def start(self):
        #total transaction that exist
        total_trans = len(self.trans)

        #Repeat while there's transaction left in the array
        while(self.trans != []):
            for i in range(total_trans):
                tlen = len(self.trans)
                if(self.trans_dict[i] != []):
                    # print(f"Transaction about to be done: {self.trans}")
                    self.exec_trans = self.trans_dict[i]
                    print(f"Executing T{i+1}: {self.exec_trans[0]}")
                    """
                    Process
                    """
                    self.onTransactionDone()
                    tlen = len(self.trans)
                    if(tlen == 0):
                        break
                    self.setTurn(tlen)
    
    def setTurn(self, tlen):
        self.turn += 1
        self.turn %= tlen
    
    def onTransactionDone(self):
        self.exec_trans.pop(0)
        # print(f"Turn: {self.turn}")

        if (self.exec_trans == []):
            self.trans.pop(self.turn)

        # print(f"Transaction to be done: {self.trans}\n")
