import sys
import copy
from datatype.wait_graph import wait_graph

class Transaction_Manager:

    """Protocol used for concurrency control"""
    protocol = None    
    
    """List of transactions need to be done"""
    trans = []

    """List of transactions that will not be deleted to do rollback"""
    perm_trans = []

    """dictionary to keep track of transaction"""
    trans_dict = {}

    """List of transaction that's being aborted"""
    abort_list = []

    """Transaction that is currently executed"""
    exec_trans = []

    """dictionary to keep track of X_Lock"""
    x_locks = {}        #USE +! FOR TRANSACTION NUMBER

    """dictionary to keep track of S_Lock"""
    s_locks = {}        #USE +! FOR TRANSACTION NUMBER

    """dictionary to see if a transaction has x-lock"""
    trans_x_locks = {}

    """dictionary to see if a transaction has s-lock"""
    trans_s_locks = {}

    """Transaction turn now"""
    turn = 0

    """Wait_graph"""
    wg = wait_graph()

    def __init__(self, transaction):
        self.getTransaction(transaction)
        
    def getTransaction(self,transaction):
        #Reading file
        f = open(transaction,"r")
        file_read = f.readlines()
        db = file_read[0].rstrip("\n").split()
        for i in db:
            #Set db lock as no(N)
            self.x_locks[i] = 0
            self.s_locks[i] = [0]

        for i in range(1,len(file_read)):
            #Remove \n from line
            self.trans.append(file_read[i].rstrip("\n").split())
            self.trans_dict[i-1] = self.trans[i-1]

            #Set up all locks owned by transaction as None
            self.trans_x_locks[i-1] = ["None"]
            self.trans_s_locks[i-1] = ["None"]
            
        self.perm_trans = copy.deepcopy(self.trans)
    
    def grantLock(self, lock, db, t_num):
        #If the transaction has an s lock and requested x lock
        if(t_num+1 in self.s_locks[db] and lock == "x"):
            self.s_locks[db].remove(db)
            self.x_locks[db] = t_num+1
            print(f"Upgrading s_lock from {db} to x_lock for T{t_num+1}")

        #If the transaction already has lock then do nothing
        if(self.x_locks[db] == t_num+1 or (t_num+1 in self.s_locks[db] and lock=="s")):
            return 1
        else:
            #If the db's x-lock is not used then grant lock
            
            # print(f"TEST: {lock}, {db}, {t_num}")
            # print(self.trans_x_locks)
            # print(self.x_locks)

            if(self.x_locks[db] == 0 and lock == "x"  and self.s_locks[db][0] == 0):
                print(f"Granting {lock}-lock to T{t_num+1} for db {db}")
                #Add locks to the transaction dictionary
                if(self.trans_x_locks[t_num][0] == "None"):
                    self.trans_x_locks[t_num][0] = db
                else:
                    self.trans_x_locks[t_num].append(db)
                #Write transaction that use the lock to dict
                self.x_locks[db] = t_num+1
                return 1
            #If the db's s-lock 
            elif(self.x_locks[db] == 0 and lock == "s"):
                print(f"Granting {lock}-lock to T{t_num+1} for db {db}")
                #Add locks to the transaction dictionary
                if(self.trans_s_locks[t_num][0] == "None"):
                    self.trans_s_locks[t_num][0] = db
                else:
                    self.trans_s_locks[t_num].append(db)
                if(self.s_locks[db][0] == 0):
                    self.s_locks[db][0] = t_num+1
                else:
                    self.s_locks[db].append(t_num+1)
                return 2
            else:
                # print(f"ONFAIL: {self.wg.adj_list}")
                if(t_num +1 not in self.wg.adj_list):
                    self.wg.addNode(t_num+1)
                
                if((lock == "s" or lock == "x") and self.x_locks[db] != 0):
                    print(f"Failed to grant {lock}-lock to T{t_num+1} for db {db} waiting for T{self.x_locks[db]}")
                    if(self.x_locks[db] not in self.wg.adj_list[t_num+1]):
                        if(self.x_locks[db] not in self.wg.adj_list):
                            self.wg.addNode(self.x_locks[db])
                        self.wg.addEdge(t_num+1,self.x_locks[db])
                elif(lock == "x" and self.s_locks[db][0] != 0):
                    print(f"Failed to grant {lock}-lock to T{t_num+1} for db {db} waiting for ", end="")
                    for i in self.s_locks[db]:
                        if(self.s_locks[db] not in self.wg.adj_list[t_num+1]):
                            if(self.s_locks[db] not in self.wg.adj_list):
                                self.wg.addNode(self.s_locks[db])
                            self.wg.addEdge(t_num+1,i)
                        print(f"T{i}", end=" ")
                    print()
                # print(f"ONFAILEND: {self.wg.adj_list}")
                return 0

    def setTurn(self, tlen):
        self.turn += 1
        self.turn %= tlen
    
    def onTransactionDone(self):
        self.exec_trans.pop(0)
        # print(f"Turn: {self.turn}")

        if (self.exec_trans == []):
            self.trans.pop(self.turn)

        # print(f"Transaction to be done: {self.trans}\n")

    #UNLOCKING ALL LOCKS UPON COMMIT
    def onCommit(self, trans):
        print(f"Committing T{trans+1}...")
        self.unlockAll(trans)
            
    def onAbort(self, trans):
        print(f"Aborting T{trans+1}...")
        self.abort_list.append(trans)
        self.unlockAll(trans)
        del self.trans[self.turn]
        self.trans_dict[trans] = []
        self.trans_x_locks[trans] = ["None"]
        self.trans_s_locks[trans] = ["None"]

    def unlockAll(self, trans):
        if(self.trans_s_locks[trans][0] != "None"):
            #Remove lock from s_lock dictionary
            for db in self.trans_s_locks[trans]:
                self.s_locks[db].remove(trans+1)
                if(len(self.s_locks[db]) == 0):
                    self.s_locks[db].append(0)
                print(f"Unlocking s_lock from {db} by T{trans+1}")

        if(self.trans_x_locks[trans][0] != "None"):
            #Remove lock from x_lock dictionary
            print(f"Unlocking x_lock from ", end="")
            for db in self.trans_x_locks[trans]:
                self.x_locks[db] = 0
                print(f"{db} ", end="")
            print(f"by T{trans+1}")
        if(trans+1 in self.wg.adj_list):
            self.wg.removeNode(trans+1)