from os import mkdir
from glob import glob
from pandas import DataFrame
from datetime import datetime
from volunteer_report import VolunteerResultsReport

class DataAnalysis():
    
    #-------------------------------------------------------------------------
    def __init__(
        self, 
        log_path, 
        save_dir="datasets/",
        find_string="_user", 
        log_file_extension="*.csv"
        ):
    #-------------------------------------------------------------------------
        self.log_path = log_path
        self.save_dir = save_dir
        self.save_path = self.log_path + self.save_dir
        self.find_string = find_string
        self.log_file_extension = log_file_extension
        self.volunteers_log_file_list = self.get_volunteers_log_file_list()
        self.volunteer_id_list = self.get_volunteers_id_list()
        self.volunteers_data = self.get_volunteers_data()
        self.last_volunteers_file_name_csv = None
        self.last_volunteers_file_name_excel = None
        self.save_path_already_existed = self.create_save_dir()
    
    #-------------------------------------------------------------------------
    def create_save_dir(self):
    #-------------------------------------------------------------------------
        save_path_already_existed = False
        try:
            mkdir(path=self.save_path)
        except FileExistsError as path_already_existed_error:
            save_path_already_existed = True
            print(path_already_existed_error)
            print("The save_path directory already exists. No need to creat it.")
        except OSError as error: 
            print(error)
        
        return save_path_already_existed
    
    #-------------------------------------------------------------------------
    def get_volunteers_log_file_list(self):
    #-------------------------------------------------------------------------
        search_pattern = self.log_path + self.log_file_extension
        volunteers_log_file_list = glob(search_pattern)
        volunteers_log_file_list.sort()
        return volunteers_log_file_list
    
    #-------------------------------------------------------------------------
    def get_volunteers_id_list(self):
    #-------------------------------------------------------------------------
        volunteer_id_list = []
        for file_name in self.volunteers_log_file_list:
            position = file_name.find(self.find_string)
            volunteer_id = int(file_name[position-4:position])
            volunteer_id_list.append(volunteer_id)
        return volunteer_id_list
    
    #-------------------------------------------------------------------------
    def get_volunteer_time_record(self, volunteer_id):
    #-------------------------------------------------------------------------
        volunteer_report = VolunteerResultsReport(volunteer_id, self.log_path)
        time_record = {"volunteer_id": volunteer_id}
        time_record = {**time_record, **volunteer_report.duration_dict}
        return time_record
    
    #-------------------------------------------------------------------------
    def get_volunteer_overall_result_record(self, volunteer_id):
    #-------------------------------------------------------------------------
        volunteer_report = VolunteerResultsReport(volunteer_id, self.log_path)
        record = {"volunteer_id": volunteer_id}
        record = {**record, **volunteer_report.overall_result_dict}
        return record
    
    #-------------------------------------------------------------------------
    def get_volunteer_result_per_class_record(self, volunteer_id):
    #-------------------------------------------------------------------------
        volunteer_report = VolunteerResultsReport(volunteer_id, self.log_path)
        result_per_class_records = volunteer_report.result_per_class_records
        dict_list = []
        for record in result_per_class_records:
            image_class_column_name = record["image_class"]
            right_answer_column_name = image_class_column_name+"_"+"questions_right_answer_count"
            total_count_column_name = image_class_column_name+"_"+"questions_total_count"
            right_perc_column_name = image_class_column_name+"_"+"questions_right_percentage"
            volunteer_result_per_class_record = {
                right_answer_column_name: record["is_right_answer"],
                total_count_column_name: record["count"],
                right_perc_column_name: record["right_perc"]
            }
            dict_list.append(volunteer_result_per_class_record)
        
        volunteer_result_per_class_record = {"volunteer_id": volunteer_id}
        for record in dict_list:
            volunteer_result_per_class_record = {**volunteer_result_per_class_record, **record}
        
        return volunteer_result_per_class_record
    
    #-------------------------------------------------------------------------
    def get_volunteer_record(self, volunteer_id):
    #-------------------------------------------------------------------------
        
        record_list = []
        
        record_list.append(self.get_volunteer_overall_result_record(volunteer_id))
        record_list.append(self.get_volunteer_time_record(volunteer_id))
        record_list.append(self.get_volunteer_result_per_class_record(volunteer_id))
        
        volunteer_record = {"volunteer_id": volunteer_id}
        for record in record_list:
            volunteer_record.update(record)
        
        return volunteer_record
    
    #-------------------------------------------------------------------------
    def get_volunteers_data(self):
    #-------------------------------------------------------------------------
        
        record_list = []
        for volunteer_id in self.volunteer_id_list:
            record_list.append(self.get_volunteer_record(volunteer_id))
        
        volunteers_data = DataFrame.from_dict(data=record_list)
        
        return volunteers_data
    
    #-------------------------------------------------------------------------
    def get_volunteers_data_file_name(
            self, 
            file_format="excel",
            file_path=None,
            file_name = "volunteers_data",
            suffix_time_format = "%Y_%m_%d_%H_%M_%S"
        ):
    #-------------------------------------------------------------------------
        
        file_format_extension_map = {
            "excel":".xlsx",
            "csv":".csv"
        }
        
        if file_format == None:
            file_format = "excel"
        
        if file_path == None:
            file_path = self.save_path
           
        if file_name == None:
            file_name = "volunteers_data"
        
        if suffix_time_format == None:
            suffix_time_format = "%Y_%m_%d_%H_%M_%S"
        
        now = datetime.now()
        suffix = now.strftime(suffix_time_format)
        extension = file_format_extension_map[file_format]
        
        full_file_name = (
            file_path
            +file_name
            +"_"
            +suffix
            +extension
        )
        
        return full_file_name
    
    #-------------------------------------------------------------------------
    def save_volunteers_csv(
            self, 
            file_path = None, 
            file_name = None,
            suffix_time_format = None    
        ):
    #-------------------------------------------------------------------------
         
        csv_file_name = self.get_volunteers_data_file_name(
            file_format="csv",
            file_path=file_path, 
            file_name=file_name,
            suffix_time_format=suffix_time_format
        )
        
        self.volunteers_data.to_csv(csv_file_name, index_label="dataset_index")
        
        self.last_volunteers_file_name_csv = csv_file_name
        
        return csv_file_name
    
    #-------------------------------------------------------------------------
    def save_volunteers_excel(
        self, 
        file_path = None, 
        file_name = None,
        suffix_time_format = None    
        ):
    #-------------------------------------------------------------------------
        excel_file_name = self.get_volunteers_data_file_name(
            file_format="excel",
            file_path=file_path, 
            file_name=file_name,
            suffix_time_format=suffix_time_format
        )
        
        self.volunteers_data.to_excel(excel_file_name, index_label="dataset_index")
        print("[save_volunteers_excel] " + excel_file_name + " has been created.")
        self.last_volunteers_file_name_excel = excel_file_name
        
        return excel_file_name 