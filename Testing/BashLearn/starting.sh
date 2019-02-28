#!/bin/bash


#ECHOING(cast)
echo "=============CASTS=========="
VAR1=56
VAR2=NOT
VAR3="it is."
echo "My favorite numbes is $VAR1 . ${VAR3} or maybe $VAR2"

FILELIST=`ls`
echo "$FILELIST"

#./startng.sh A B C
#echo $3 
#>> C
#echo $0 
#>> startng.sh
# echo $#
#>> 4            numero de aegumentos recibidos

#ARRAYS
echo "=============ARRAYS=========="
my_array=(apple banana Fruit Basket orange)
my_array[2]="apricot"
echo ${my_array[2]}
echo "El tamaño del array es ${#my_array[@]}"

#OPERATORS
echo "=============OPERATORS=========="

a=3
echo "305 = $((10**2* $a +5)) "
echo "305 = $((10/2% $a +303)) "

STR="sometimes things get complicated, but my cat is named avocato"
SUBSTR="i"
echo "length of ' $STR ' is ${#STR}"

expr index "$STR" "$SUBSTR"

POS=21
LEN=11
echo ${STR:$POS:$LEN}
echo ${STR:38}

STRING="to be or not to be"
echo ${STRING[@]/be/eat} 

STRING="to be or not to be"
echo ${STRING[@]//be/eat}  

##CHOICES
echo "=============CHOICES=========="
NAME="George"
if [ "$NAME" = "John" ]; then
  echo "John Lennon"
elif [ "$NAME" = "George" ]; then
  echo "George Harrison"
else
  echo "This leaves us with Paul and Ringo"
fi

#comparison    Evaluated to true when
#$a -lt $b    $a < $b
#$a -gt $b    $a > $b
#$a -le $b    $a <= $b
#$a -ge $b    $a >= $b
#$a -eq $b    $a is equal to $b
#"$a" = "$b"     $a is the same as $b
#"$a" == "$b"    $a is the same as $b
#"$a" != "$b"    $a is different from $b
#-z "$a"         $a is empty

#note1: whitespace around = is required
#note2: use "" around string variables to avoid shell expansion of special characters as *


#CASOS==========
echo "=============CASOS=========="

mycase=1
case $mycase in
    1) echo "You selected bash";;
    2) echo "You selected perl";;
    3) echo "You selected phyton";;
    4) echo "You selected c++";;
    5) exit
esac


##LOOOPS====
echo "=============LOOPS=========="
# loop on array member
NAMES=(Joe Jenny Sara Tony)
for N in ${NAMES[@]} ; do
  echo "My name is $N"
done



COUNT=4
while [ $COUNT -gt 0 ]; do
  echo "Value of count is: $COUNT"
  COUNT=$(($COUNT - 1))
done


COUNT=1
until [ $COUNT -gt 5 ]; do
  echo "Value of count is: $COUNT"
  COUNT=$(($COUNT + 1))
done


# Prints out 0,1,2,3,4

COUNT=0
while [ $COUNT -ge 0 ]; do
  echo "Value of COUNT is: $COUNT"
  COUNT=$((COUNT+1))
  if [ $COUNT -ge 5 ] ; then
    break
  fi
done

# Prints out only odd numbers - 1,3,5,7,9
COUNT=0
while [ $COUNT -lt 10 ]; do
  COUNT=$((COUNT+1))
  # Check if COUNT is even
  if [ $(($COUNT % 2)) = 0 ] ; then
    continue
  fi
  echo $COUNT
done




##FUNCTIONS====
echo "=============FUNCTIONS=========="

function function_B {
  echo "Function B."
}
function function_A {
  echo "$1"
}
function adder {
  echo " $1 * $2 = $(($1 * $2))"
}

# FUNCTION CALLS
# Pass parameter to function A
function_A "Function A."     # Function A.
function_B                   # Function B.
# Pass two parameters to function adder
adder 111111 111111                  # 68



# $0 - The filename of the current script.|
# $n - The Nth argument passed to script was invoked or function was called.|
# $# - The number of argument passed to script or function.|
# $@ - All arguments passed to script or function.|
# $* - All arguments passed to script or function.|
# $? - The exit status of the last command executed.|
# $$ - The process ID of the current shell. For shell scripts, this is the process ID under which they are executing.|
# $! - The process number of the last background command.|

function func {
    echo "--- \"\$*\""
    for ARG in "$*"
    do
        echo $ARG
    done

    echo "--- \"\$@\""
    for ARG in "$@"
    do
        echo $ARG
    done
}
func We are argument





filename="Arrests.csv"
echo "testing if '$filename' exists"
if [ -e "$filename" ]; then
    echo "$filename exists as a file"
fi


dirnames="TestFolder"
mkdir $dirnames



echo "testing if '$dirnames' exists"
if [ -d "$dirnames" ]; then
    echo "$dirnames exists as a file"
fi




if [ ! -f "$filename" ]; then
    touch "$filename"
fi
if [ -r "$filename" ]; then
    echo "you are allowed to read $filename"
else
    echo "you are not allowed to read $filename"
fi


