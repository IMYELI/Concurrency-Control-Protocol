import random
def simpleLocking(Transaction_Manager):
    #total transaction that exist
    total_trans = len(Transaction_Manager.trans)

    #Repeat while there's transaction left in the array using round robin
    br = 0
    failed = False
    while(Transaction_Manager.trans != []):
        # if(failed):
        #     break
        for i in range(total_trans):
            
            # print("AWAL :")
            # print(Transaction_Manager.trans)
            tlen = len(Transaction_Manager.trans)
            if(Transaction_Manager.trans_dict[i] != []):
                abort = False
                # print(f"Transaction about to be done: {Transaction_Manager.trans}")
                Transaction_Manager.exec_trans = Transaction_Manager.trans_dict[i]

                print(f"Executing T{i+1}: {Transaction_Manager.exec_trans[0]}")
                
                """
                Process
                """
                check_grant = Transaction_Manager.grantLock("x", Transaction_Manager.exec_trans[0].split("-")[1],i)

                # if(br == 4):
                #     failed = True
                #     break  
                # br += 
                
                if(check_grant>0):
                    Transaction_Manager.onTransactionDone()
                    br = 0
                if(len(Transaction_Manager.wg.adj_list) != 0 and Transaction_Manager.wg.hasCycle()):
                    print(f"DEADLOCK DETECTED: {Transaction_Manager.wg.adj_list}")
                    Transaction_Manager.onAbort(i)
                    abort = True

                oldTlen = tlen
                tlen = len(Transaction_Manager.trans)
                if(oldTlen != tlen and not abort):
                    Transaction_Manager.onCommit(i)
                if(tlen == 0):
                    break
                Transaction_Manager.setTurn(tlen)
                # print(Transaction_Manager.trans)
                # print(Transaction_Manager.trans_dict)
                print()
    
    print()
    for aborted in Transaction_Manager.abort_list:
        for action in Transaction_Manager.perm_trans[aborted]:
            print(f"Executing T{aborted+1}: {action}")
            Transaction_Manager.grantLock("x", action.split("-")[1],aborted)
        Transaction_Manager.onCommit(aborted)
        print()