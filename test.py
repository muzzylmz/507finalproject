import unittest
import sqlite3


class Test_Data(unittest.TestCase):
    def test_job_table(self):
        DBNAME = 'ux-job.db'
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql= 'SELECT Title, JobType,CompanyName,PostDate From Jobs ORDER BY CompanyId '
        results = cur.execute(sql)
        result_list = results.fetchall()
        title_list= []
        jobtype_list=[]
        for i in result_list:
            a= i[0]
            b= i[1]
            title_list.append(a)
            jobtype_list.append(b)

        self.assertIn('Head of Design',title_list)
        self.assertIn('UX Designer',title_list)
        self.assertIn('Full-time',jobtype_list)
        self.assertIn('Contract',jobtype_list)
        self.assertEqual(title_list[0],'User Experience (UX) Research Lead')
        conn.close()

    def test_company_table(self):
        DBNAME = 'ux-job.db'
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql= 'SELECT Name,City,Country,Lat,Lon From Companies ORDER BY Id '
        results = cur.execute(sql)
        result_list = results.fetchall()

        company_name=[]
        city= []
        for i in result_list:
            a= i[0]
            b=i[1]
            company_name.append(a)
            city.append(b)

        self.assertIn('Bark.com',company_name)
        self.assertIn('Meraki',company_name)
        self.assertEqual(company_name[0],'Achievement Network (ANet)')
        self.assertEqual(city[0],'Boston')
        self.assertIn('Zurich',city)
        conn.close()

    def test_company_obj(self):
        DBNAME = 'ux-job.db'
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql= 'SELECT Name,City,Lat,Lon,CompanySite From Companies ORDER BY Id '
        results = cur.execute(sql)
        result_list = results.fetchall()
        lat_list= []
        lon_list=[]
        companysite=[]
        for i in result_list:
            a= i[2]
            b= i[3]
            c=i[4]
            lat_list.append(a)
            lon_list.append(b)
            companysite.append(c)
        self.assertIn((lat_list)[0],'42.3600825')
        self.assertIn((lon_list)[0],'-71.05888010000001')
        self.assertIn('51.5073509',lat_list)
        self.assertIn('-2.3590166999999838',lon_list)
        self.assertIn('https://www.bark.com/',companysite)
        conn.close()
unittest.main()
