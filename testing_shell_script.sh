
echo "Jack"


col_1=("a" "d" "g")
col_2=("b" "e" "h")
col_3=("c" "f" "i")

arr_main=(col_1 col_2 col_3)

for i in "${arr_main[@]}"; do
    declare -n col="$i"  
    for j in "${col[@]}"; do
        echo "$j"
    done
done

