MINING_REWARD = 10 #placed this in all caps because it is a global variable

#Initializing our (empty) blockchain list
genesis_block = {
    'genesis_hash': '',
    'index': 0,
    'transactions': []
}

#1) Initialising blockchain list (array)
blockchain = [genesis_block]
open_transactions = []
owner = 'ZK' #unique identifier for sender
participants = {'ZK'}  #initialising set. Note set is an unordered list without duplicates

def hash_block(block):
    # inside the string function is a
    return '_'.join([str(block[key]) for key in block])
    #list comprehension

def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
        #the code that you are executing in a listed comprehension is really saying:
        # new_list.append(item_in_for_loop) so you are creating a new list of the items being thrown out of the for loop
        #in this case it would be tx_sender.append[tx['amount]] to give you e.g. [4, 12.1, 3.7]
    open_tx_sender = [ tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent


            #2) Function to access last data structure from array
def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None  #don't have to use else because return None will exit function
                    #after it returns none
    return blockchain[-1]  # -1 in list is python built in functionality for
                            #last element in the list
#python convention - two lines between functions
            #3) Function to add data structure to list, this takes two arguments
                #argument 1 the new data structure
                #argument 2 the previous data structure (this is to create the chain)

def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount'] #the comparison operator will return a boolean
    

def add_transaction(recipient, sender = owner, amount = 1.0): #first variables without defaults

    """ Append a new value

    Arguments: 
        :sender: The sender of the amount.
        :recipient: the recipient of the amount.
        :amount: The amount of coins sent. (default = 1.0)
        """
    transaction = {
        'sender': sender, 
        'recipient':recipient, 
        'amount':amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction) #list of transactions. Transactions take on sender, recipient and amount
        participants.add(sender)
        participants.add(recipient)
        return True
    return False

def mine_block():
    if len(blockchain) > 0:
        last_block = blockchain[-1]  #block is composed of a dictionary of 'previous hash', 'index', 'transactions'
    else:
        last_block = genesis_block
    hashed_block = hash_block(last_block)

    reward_transaction = {
        'sender':"Mining",
        'recipient': owner,
        'amount' : MINING_REWARD
    }

    open_transactions.append(reward_transaction)
    print('Hash of last block: ' + hashed_block)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions':open_transactions
    }
    blockchain.append(block)
    return True

#creating a nested list

def get_transaction_value():
    tx_recipient = input('Enter the transaction recipient:')
    # input function returns a string
    tx_amount = float(input('Transaction amount please:'))
    return (tx_recipient, tx_amount) #creates a tuple out of the two variables


def get_user_choice():
    user_input = input('Your Choice: ')
    return user_input

def print_blockchain_element():
    #outputting the blockchain
    blocknumber = 1
    for element in blockchain:
        print(f"Outputting block {blocknumber}: ")
        print(element)
        blocknumber += 1
    else:   #the else executes when ever I exit the for loop
        print("_"*20)
    print('Done!')

def verify_blockchain():
    """ Verify the the current blockchain """
    for (index, block) in enumerate(blockchain): #enumerate gives index and value
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True


# allows you to check anytime if open transactions are valid

def verify_transactions():
    is_valid = True
    for tx in open_transactions:
        if verify_transaction(tx):
            is_valid = True
        else:
            is_valid = False
    return is_valid
        





waiting_for_input = True
#print(blockchain)
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a block')
    print('3: Output the blockchain blocks')
    print('4: Output Participants')
    print('5: Check transaction validity')
    print('h: manipulate the blockchain')
    print('select q to Quit!')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data #unpacking a tuple
        if add_transaction(recipient, amount=amount):
            print('Added Transaction!')
        else:
            print('Transaction Failed!')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block(): #we've set the function to return true at the end
            open_transactions = [] #when the block is appended we need to reset the transactions to an empy block
    elif user_choice == '3':
        print_blockchain_element()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': {
                    'sender': 'ZK',
                    'recipient': "MK",
                    'amount': 13.2
                }
            }
    elif user_choice == 'q':
        waiting_for_input = False  
    else:
        print("Input was invalid please pick a value from the list!")
    if not verify_blockchain():  #verify_blockchain function is a function that returns True / False after checking blockchain
        print('Invalid Blockchain')
        break
    print('Balance: ' + str(get_balance('ZK')))
    print('Blockchain: ' + str(blockchain))

print('Choice Registered!')
print('Balance of sender:')

