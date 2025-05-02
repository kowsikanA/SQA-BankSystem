#!/bin/bash

# Input files
CURRENT_ACCOUNT_FILE="../../First three phases/FrontEnd/CurrentBankAccounts.txt"
MASTER_ACCOUNT_FILE="../old_master_acc.txt"
FRONT_END="../../First three phases/FrontEnd/bank-atm.py"
MERGED_TRANSACTION_FILE="../merged_acc_transaction.txt"

# Output files
MERGED_TRANSACTION_FILE="merged_acc_transaction.txt"
NEW_MASTER_ACCOUNT_FILE="new_master_acc.txt"
NEW_CURRENT_ACCOUNT_FILE="new_current_acc.txt"

# Makes sure the input files exist
if [ ! -f "$CURRENT_ACCOUNT_FILE" ]; then
    echo "Error: $CURRENT_ACCOUNT_FILE does not exist"
    exit 1
fi
if [ ! -f "$MASTER_ACCOUNT_FILE" ]; then
    echo "Error: $MASTER_ACCOUNT_FILE does not exist"
    exit 1
fi

rm -f "$MERGED_TRANSACTION_FILE"

for i in {1..7}; do
  INPUT_FILE="../daily script inputs/session${i}.inp.txt"
  OUTPUT_FILE="../atf_files/session${i}.atf.txt"

  echo
  echo "-----------------------------------------"
  echo "          Front End Session $i           "
  echo "-----------------------------------------"

  if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: $INPUT_FILE does not exist"
    exit 1
  fi

  python3 "$FRONT_END" "$CURRENT_ACCOUNT_FILE" "$OUTPUT_FILE" < "$INPUT_FILE"
  if [ $? -ne 0 ]; then
    echo "Error: Front End session $i failed"
    exit 1
  fi
done

# Merged transaction files
for i in {1..7}; do
  cat "../atf_files/session${i}.atf.txt" >> "$MERGED_TRANSACTION_FILE"
done

# Running the backend
echo
echo "-----------------------------------------"
echo "          Back End                       "
echo "-----------------------------------------"

python3 bank_system.py "$MERGED_TRANSACTION_FILE" "$MASTER_ACCOUNT_FILE" "$NEW_MASTER_ACCOUNT_FILE" "$NEW_CURRENT_ACCOUNT_FILE"
if [ $? -ne 0 ]; then
  echo "Error: Back End failed"
  exit 1
fi


echo
echo "Daily script finished"
exit 0