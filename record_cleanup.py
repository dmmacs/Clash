

from zipfile import ZipFile
from glob2 import glob
import ClanCommon
from datetime import datetime, date
import os


def clean_up_files(clan_tag, clan_name, file_root):

    fPath = clan_tag + '/record'
    # Look for existing zip file
    file_filter = fPath + '/' + clan_name + file_root + '.zip'

    # zip_files = glob(file_filter)

    zip_name = fPath + '/' + clan_name + '-clan_member_data.zip'
    # if len(zip_files) > 0:
    #     zip_name = zip_files[0] 
    # else:
    #     zip_name = clan_name + '-clan_member_data.zip'
#    print("Zip Name = ", zip_name)

    print("Opening Zipfile = " + zip_name)    
    zipObj = ZipFile(zip_name, 'a')

    file_filter = fPath +  '/' + clan_name + file_root + '*.txt'

    #beavercleavers-clan_member_data-20190915.txt
#    print(file_filter)

    files = glob(file_filter)

#    print(len(files))

    SEC_IN_30_DAYS = 60 * 60 * 24 * 30

    now = datetime.now()
    cnt = 0
    for file in files:
        # Need to zip up all files more than 30 days ago
        file_timestamp = os.path.getmtime(file)
#        print(file, os.path.getmtime(file), now.timestamp() - file_timestamp, now.timestamp() - file_timestamp > SEC_IN_30_DAYS)
        if now.timestamp() - file_timestamp > SEC_IN_30_DAYS:
            zipObj.write(file)
            os.remove(file)
            cnt += 1

        #break

    zipObj.close()
    print("Files Archived, ", cnt)

if __name__ == "__main__":

    clan_tag = 'QQG200V'
    file_root = '-clan_member_data'
    clean_up_files(clan_tag, 'beavercleavers', '-clan_member_data')
    clean_up_files(clan_tag, 'beavercleavers', '-clan_data-')
    clean_up_files(clan_tag, 'beavercleavers', '-currentwar-')
    clean_up_files(clan_tag, 'beavercleavers', '-tourn_global_data-')
    clean_up_files(clan_tag, 'beavercleavers', '-warlog-')
    
