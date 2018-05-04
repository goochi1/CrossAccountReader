import os 
import argparse
import subprocess


def par():
    parser = argparse.ArgumentParser(description='Base for cross account reader.')
    parser.add_argument('-env', required=True, help='Enviroment Prod or Dev')
   
    args = parser.parse_args()

    #use as varibles
    global env
    env = args.env

def addaccount():
    print '\nAccount Name:',
    AccountName = raw_input()

    try:
        AccountNo = int(raw_input("\nAccount Number: "))
    except ValueError:
        print "\nPlease enter number:" 


    accounts="%sAccountNo.txt" %env
    #file_path = "file.txt"
    par ()
    if os.path.exists(file_path): 
        with open(file_path, 'a') as file:
            file.write("\n%s%s,%s" %(AccountName,env, AccountNo))  #adds account name, env and number to list

addaccount ()