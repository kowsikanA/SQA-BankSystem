#!/bin/bash

#initial files
CURRENT_ACCOUNT="initial_current_acc.txt"
MASTER_ACCOUNT="master_acc_day0.txt"

cp "$CURRENT_ACCOUNT" current_acc.txt
cp "$MASTER_ACCOUNT" old_master_acc.txt

echo
echo "----------------------------"
echo "       Weekly Script        "
echo "----------------------------"

for i in {1..7}; do

  echo
  echo "--------------------------------"
  echo "     Running Day $i             "
  echo "--------------------------------"

  ./daily_script.sh
  if [ $? -ne 0 ]; then
    echo " "
    exit 1
  fi

  mv new_current_acc.txt current_acc.txt
  mv new_master_acc.txt "master_acc_day${i}.txt"
  cp "master_acc_day${i}.txt" old_master_acc.txt
done

echo
echo " Weekly Script finished"

exit 0