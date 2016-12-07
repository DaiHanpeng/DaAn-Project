from GetLatestFile.GetLatestFile import GetLatestFile
import uuid
import datetime
from DatabaseInterface.MySqlTimestampInterface import MYSQL_DB_SCHEMA,TableTimestampInterface


class CalibrationResult():
    '''
    definition of Calibration Result.
    '''
    def __init__(self,fv,mean,r,n):
        self.fv= fv
        self.mean = mean
        self.r = r
        self.n = n

    def __repr__(self):
        return ' fv: '+str(self.fv)+' mean: '+str(self.mean)+' r: '+str(self.r)+' n: '+str(self.n)


class CalibrationCurveInfo():
    '''
    definition of Calibration Curve.
    '''
    def __init__(self,lot,points,fit_rate=1,status='pass',result_date='',reagent_lot='',test_code='',curve='',cal_results=[]):
        self.lot = lot
        self.points = points
        self.fit_rate = fit_rate
        self.status = status
        self.result_date = result_date
        self.reagent_lot = reagent_lot
        self.test_code = test_code
        self.curve = curve
        self.cal_results = cal_results #list of CalibrationResult
        self.uuid = str(uuid.uuid1()) # generate an unique id.

    def __repr__(self):
        return 'Calibration Curve Info:\n'+'lot:'+str(self.lot)+'\n'+\
            'points:'+str(self.points)+'\n'+\
            'fit_rate:'+str(self.fit_rate)+'\n'+\
            'status:'+str(self.status)+'\n'+\
            'result_date:'+str(self.result_date)+'\n'+\
            'reagent_lot:'+str(self.reagent_lot)+'\n'+\
            'test_code:'+str(self.test_code)+'\n'+\
            'curve:'+str(self.curve)+'\n'+\
            'uuid:'+str(self.uuid)+'\n'+\
            'calibration results:\n'+\
            '\n'.join(str(result) for result in self.cal_results)+\
            '\n'


class CalibrationCurveParser():
    '''
    parser of Calibration Curve Info from printed file.
    '''
    '''
    [HEAD1]Test name : TBA-M
    [HEAD2]Calc.mthd : 1-point      Blank : Zero                  Axis conv. : No conv.    Formula : Linear         Points : 2
    [HEAD3]Date/Time : 8/10/2016 18:12:42   Cal Kit Lot Number :    R1 Lot Number :    R2 Lot Number :
    [HEAD4]Status : Pass
    [HEAD5]A  = 0.000000   B  = 0.001167   C  = 0.000000   D  = 0.000000   E  = 0.000000   u1 = 0.000000   u2 = 0.000000
    [HEAD6]                      <FV>               <MEAN>               <R>            <N>    <User>
    [HEAD7]
    [RESULT]BLK :                 0.0000              0.0046            0.000037           2    adv
    [RESULT]STD :                50.0000              0.0584            0.000560           2
    [RESULT]F :                                   856.730047
    '''
    PARSING_MODE = {'OFF':0,'HEAD1':1,'HEAD2':2,'HEAD3':3,'HEAD4':4,'HEAD5':5,'HEAD6':6,'HEAD7':7,'RESULT':8}
    MODULE_NAME = r'CalibrationCurve'
    def __init__(self):
        self.cal_curve_info_list = []
        try:
            db_interface = TableTimestampInterface()
            db_interface.db_connect_initialize(MYSQL_DB_SCHEMA)
            self.last_updated_timestamp = db_interface.get_table_last_updated_timestamp(self.MODULE_NAME)
            print self.MODULE_NAME,' last updated timestamp: ', self.last_updated_timestamp
        except Exception as e:
            print 'db timestamp initialize failed!', e
        finally:
            db_interface.db_disconnect()

    def extract_cal_info(self,cal_path):
        self.cal_curve_info_list = []

        lates_cal_file = GetLatestFile.get_latest_file(cal_path,'Calibration Curve','.TXT')

        last_updated_timestamp = self.last_updated_timestamp

        print lates_cal_file

        file_content_list = []
        if lates_cal_file:
            # read file content into list.
            try:
                cal_file_handler = open(lates_cal_file)
                file_content_list = cal_file_handler.readlines()
            except Exception as e:
                print 'file read failed!'
            finally:
                cal_file_handler.close()

        if file_content_list:

            file_content_list.append(r'')
            parsing_mode = CalibrationCurveParser.PARSING_MODE['HEAD1']

            for line in file_content_list:
                if isinstance(line,str):
                    # matching for [HEAD1]
                    if CalibrationCurveParser.PARSING_MODE['HEAD1'] == parsing_mode:
                        test = ''
                        curve = ''
                        points = ''
                        date_time = ''
                        cal_lot = ''
                        reagent_lot = ''
                        status = ''
                        cal_results = []
                        rate = r'1.0'
                        f_date_time = datetime.datetime.now()
                        if line.find(r'Test name :') <> -1:
                            test = line.split(r':')[1].strip()
                            parsing_mode = CalibrationCurveParser.PARSING_MODE['HEAD2']
                    # matching for [HEAD2]
                    elif CalibrationCurveParser.PARSING_MODE['HEAD2'] == parsing_mode:
                        if line.find(r'Formula :') <> -1 and line.find(r'Points :') <> -1:
                            curve = line.split(r'Formula :')[1].split()[0].strip()
                            points = line.split(r'Points :')[1].strip()
                            parsing_mode = CalibrationCurveParser.PARSING_MODE['HEAD3']
                    #matching for [HEAD3]
                    elif CalibrationCurveParser.PARSING_MODE['HEAD3'] == parsing_mode:
                        if line.find(r'Date/Time :') <> -1 and line.find(r'Cal Kit Lot Number :') <> -1:
                            date_time = line.split(r'Date/Time :')[1].split(r'Cal Kit Lot Number :')[0].strip()
                            f_date_time = datetime.datetime.strptime(date_time,'%m/%d/%Y %H:%M:%S')#1/20/2016 16:00:08
                            cal_lot = line.split(r'Cal Kit Lot Number :')[1].split(r'R1 Lot Number :')[0].strip()
                            reagent_lot = line.split(r'R1 Lot Number :')[1].split(r'R2 Lot Number :')[0].strip()
                            parsing_mode = CalibrationCurveParser.PARSING_MODE['HEAD4']
                    # matching for [HEAD4]
                    elif CalibrationCurveParser.PARSING_MODE['HEAD4'] == parsing_mode:
                        if line.find(r'Status :') <> -1:
                            status = line.split(r'Status :')[1].strip()
                            parsing_mode = CalibrationCurveParser.PARSING_MODE['HEAD5']
                    # matching for [HEAD5]
                    elif CalibrationCurveParser.PARSING_MODE['HEAD5'] == parsing_mode:
                        parsing_mode = CalibrationCurveParser.PARSING_MODE['HEAD6']
                    # matching for [HEAD6]
                    elif CalibrationCurveParser.PARSING_MODE['HEAD6'] == parsing_mode:
                        parsing_mode = CalibrationCurveParser.PARSING_MODE['HEAD7']
                    elif CalibrationCurveParser.PARSING_MODE['HEAD7'] == parsing_mode:
                        parsing_mode = CalibrationCurveParser.PARSING_MODE['RESULT']
                    # matching for [RESULT]
                    elif CalibrationCurveParser.PARSING_MODE['RESULT'] == parsing_mode:
                        if line.strip() == '':
                            parsing_mode = CalibrationCurveParser.PARSING_MODE['HEAD1']
                            if f_date_time > last_updated_timestamp:
                                if f_date_time > self.last_updated_timestamp:
                                    self.last_updated_timestamp = f_date_time
                                self.cal_curve_info_list.append(\
                                    CalibrationCurveInfo(cal_lot,points,rate,status,f_date_time,reagent_lot,test,curve,cal_results))
                        else:
                            if line.find(r'SD :') <> -1:
                                rate = line.split(r'     r :')[1].strip()
                            else:
                                fv = line[12:30].strip()
                                mean = line[35:50].strip()
                                r = line[58:72].strip()
                                n= line[78:82].strip()
                                user = line[82:].strip()
                                if fv and mean and r and n and user:
                                    cal_results.append(CalibrationResult(fv,mean,r,n))

        if self.last_updated_timestamp > last_updated_timestamp:
            try:
                db_interface = TableTimestampInterface()
                db_interface.db_connect_initialize(MYSQL_DB_SCHEMA)
                db_interface.update_table_timestamp(self.MODULE_NAME,self.last_updated_timestamp)
            except Exception as e:
                print 'db update timestamp failed!', e
            finally:
                db_interface.db_disconnect()

    def __repr__(self):
        return 'Calibration Curve Parse Result:\n' +\
            '\n'.join(str(item) for item in self.cal_curve_info_list)


def test():
    parser = CalibrationCurveParser()
    parser.extract_cal_info('.')
    print parser


if __name__ == '__main__':
    test()
