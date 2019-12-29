while true
do
process_count=$(ps aux | grep pixelflut | wc -l)
if [[ process_count -lt 10 ]]
then
	for (( c=0; c<=50; c++ ))
	do  
	 python3 /home/stefan/pixelflut/pixelflut.py 151.217.176.193 1234 $1 400 400 &
	done
fi
sleep 10
done

