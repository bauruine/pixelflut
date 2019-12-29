while true
do
process_count=$(ps aux | grep pixelflut | wc -l)
if [[ process_count -lt 10 ]]
then
	for (( c=0; c<=9; c++ ))
	do  
	 python3 /home/stefan/pixelflut/pixelflut.py --imagename $1 --host $2 --port 1234 --xoffset $3 --yoffset $4 &
	done
fi
sleep 10
done

