
cd /srv/www/web/ClashRoyale
echo `pwd`

date
echo "Check on Lock File"
./testLock.py

echo "Runing" >> ClanData.lck
echo "Data for Clan Tag #QQG200V"
./ClanData.py --clantag QQG200V --history
chmod 666 QQG200V/record/*.txt
retVal=$?
#printf 'QQG200V Exit Code = %d\n' $retVal

if [ $retVal -ne 0 ]; then
    echo "Got Here1"
    exit 1
fi

echo "Data for Highland, #8YGUPVPR"
./Highland.py --tag "#8YGUPVPR" --clantag "QQG200V"
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Got Here for Highland code failure"
    exit 1
fi
pwd
./record_cleanup.py

echo "Data for Clan Tag #2UPJYJPU"
./ClanData.py --clantag "2UPJYJPU" --history
#printf '2UPJYJPUj Exit Code = %d\n' $?
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Got Here1"
    exit 1
fi

./Highland.py --tag "#LQU8GLYY" --clantag "2UPJYJPU"
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Got Here1"
    exit 1
fi

date
touch /home/dmmacs/tmp.txt

rm ClanData.lck
