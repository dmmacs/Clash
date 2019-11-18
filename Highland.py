
import ClanCommon
import glob
import json


def getTrophyData(tag, clan_tag):
    record_folder = 'record' + ClanCommon.DirSlash()
    record_folder = clan_tag + ClanCommon.DirSlash() + 'record' + ClanCommon.DirSlash()
    print('\nProcess Trophy History for {} in {}'.format(clan_tag, record_folder))

    file_filter = record_folder + '*clan_data*' + '*.txt'
    files = glob.glob(file_filter)

    outstr = ''
    for file in files:
        idx1 = file.rfind('-') + 1
        idx2 = file.rfind('.')
        fTime = ClanCommon.getFileNameDate(file[idx1:idx2])
        #        print(file,fTime)
        fin = open(file, 'r')
        clan_data = json.load(fin)
        for person in clan_data['memberList']:
            if person['tag'] == '#8YGUPVPR':
                # print('{},{},{}'.format(fTime.strftime('%d-%b-%Y'),person['name'], person['trophies']))
                outstr += '{},{},{}\n'.format(person['name'], fTime.strftime('%d-%b-%Y'), person['trophies'])
                break

    # print(outstr)
    fname = record_folder + 'highland' + '.csv'
    #    print(fname)
    out = open(fname, 'w', encoding='UTF-8')
    out.write(outstr)
    out.close()


# Start of main
if __name__ == '__main__':

    ClanCommon.init()

    clan_tag = 'QQG200V'

    getTrophyData('#8YGUPVPR',clan_tag)
