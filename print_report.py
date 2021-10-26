import sys
from os import system
from pandas import read_csv, DataFrame
from volunteer_report import VolunteerResultsReport

log_path = './log_files/'
volunteer_id = int(sys.argv[1])
fulano_rel = VolunteerResultsReport(volunteer_id,log_path)
fulano_rel.save_report()
fulano_rel.print_report()