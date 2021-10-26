from os import name
from pandas import read_csv, DataFrame
from datetime import datetime

class VolunteerResultsReport():
    
    IMAGE_LABEL_MAP = {
        "catch_stimuli": '"Pegadinha"',
        "negative": "Negativa",
        "neutral": "Neutra",
        "positive": "Positiva"
    }

    #-------------------------------------------------------------------------
    def __init__(self, volunteer_id, log_path):
    #-------------------------------------------------------------------------
        self.volunteer_id = volunteer_id
        self.log_path = log_path
        self.df_log = self.read_log_file(log_path, volunteer_id)
        self.duration_dict = self.get_duration()
        self.df_test_answers = self.label_right_answers()
        self.overall_result_dict = self.get_overall_result()
        self.result_per_class_df, self.result_per_class_records = (
            self.get_result_per_class()
        )
        self.report = self.build_report()
        
    #-------------------------------------------------------------------------
    def read_log_file(self, log_path, volunteer_id):
    #-------------------------------------------------------------------------
        log_name = '{:04d}_user_log.csv'.format(volunteer_id)
        df_log = read_csv(log_path+log_name)
        return df_log
    
    #-------------------------------------------------------------------------
    def get_hours_minutes_seconds(self, delta_t):
    #-------------------------------------------------------------------------
        # https://stackoverflow.com/questions/2119472/convert-a-timedelta-to-days-hours-and-minutes
        days = delta_t.days
        hours, remainder = divmod(delta_t.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return days, hours, minutes, seconds
    
    #-------------------------------------------------------------------------
    def get_duration(self):
    #-------------------------------------------------------------------------
        
        timestamp_format = '%Y-%m-%d %H:%M:%S.%f'
        
        t_i = (
            self.df_log[(self.df_log['phase_name'] == 'study_phase') 
            & (self.df_log['event_type'] == 'instructions')]['timestamp']
        )
    
        t_i = datetime.strptime(t_i.values[0], timestamp_format)

        
        t_f = (
            self.df_log[(self.df_log['phase_name'] == 'test_phase') 
            & (self.df_log['event_type'] == 'end')]['timestamp']
        )
        
        t_f = datetime.strptime(t_f.values[0], timestamp_format)
        
        delta_t = t_f - t_i
        
        days, hours, minutes, seconds = self.get_hours_minutes_seconds(delta_t)
        
        duration_dict = {
            "timestamp_begin": t_i,
            "timestamp_end": t_f,
            "timestamp_duration": delta_t,
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }
        
        return duration_dict

    #-------------------------------------------------------------------------
    def get_image_class(self, image_type):
    #-------------------------------------------------------------------------
        
        image_class = image_type
        
        if image_type == 'negative_animal_concerns':
            image_class = 'negative'
        if image_type == 'negative_human_concerns':
            image_class = 'negative'
        if image_type == 'negative_spiders':
            image_class = 'negative'
        if image_type == 'negative_snakes':
            image_class = 'negative'
        
        return image_class
    
    #-------------------------------------------------------------------------
    def label_right_answers(self):
    #-------------------------------------------------------------------------
    
        self.df_log['image_class'] = self.df_log['image_type'].apply(self.get_image_class)

        is_test_phase = self.df_log['phase_name'] == 'test_phase'
        df_test = self.df_log.loc[is_test_phase]

        is_answer = df_test['event_type'] == 'answer'
        df_test_answers = df_test.loc[is_answer]
        
        mask_right_true  = (
            (df_test_answers['image_class'] != 'catch_stimuli') 
            & (df_test_answers['in_study_phase'] == 'True') 
            & (df_test_answers['answer'] == 'yes')
        )

        mask_right_false = (
            (df_test_answers['image_class'] != 'catch_stimuli') 
            & (df_test_answers['in_study_phase'] == 'False') 
            & (df_test_answers['answer'] == 'no' )
        )

        mask_right_catch = (
            (df_test_answers['image_class'] == 'catch_stimuli') 
            & (df_test_answers['answer'] == 'catch_image' )
        )
        
        mask_right = mask_right_true | mask_right_false | mask_right_catch
        
        df_test_answers['is_right_answer'] = mask_right.to_numpy()
        
        return df_test_answers
    
    #-------------------------------------------------------------------------
    def get_overall_result(self):
    #-------------------------------------------------------------------------
        images_count = self.df_test_answers.shape[0]
        right_answers_count = self.df_test_answers['is_right_answer'].sum()
        wrong_answers_count = images_count - right_answers_count
        overall_result_ratio = (right_answers_count / images_count)
        overall_result_percentage = overall_result_ratio*100.0
        overall_result_dict = {
            "images_count": images_count,
            "right_answers_count": right_answers_count,
            "wrong_answers_count": wrong_answers_count,
            "overall_result_ratio": overall_result_ratio,
            "overall_result_percentage": overall_result_percentage,
        }
        
        return overall_result_dict
  

    #-------------------------------------------------------------------------
    def get_result_per_class(self):
    #-------------------------------------------------------------------------
        df_groupby_image_class = self.df_test_answers.groupby(['image_class'])
        df_result_per_class = DataFrame(df_groupby_image_class['is_right_answer'].sum())
        df_result_per_class['count'] = df_groupby_image_class['is_right_answer'].count()
        df_result_per_class['right_perc'] = (df_result_per_class['is_right_answer'] / df_result_per_class['count'])*100.0
        result_per_class_records = self.get_result_per_class_records(df_result_per_class)
        return df_result_per_class, result_per_class_records
    
    #-------------------------------------------------------------------------
    def get_result_per_class_records(self, df_result_per_class):
    #-------------------------------------------------------------------------
        records_list = []
        result_per_class_records = df_result_per_class.reset_index().to_records()
        for index, image_class, is_right_answer, count, right_perc in result_per_class_records:
            record = {
            "image_class" : image_class,
            "is_right_answer" : is_right_answer,
            "count" : count,
            "right_perc" : right_perc
            }
            records_list.append(record)
        return records_list
    
    #-------------------------------------------------------------------------
    def build_report(self):
    #-------------------------------------------------------------------------
        
        days = self.duration_dict["days"]
        hours = self.duration_dict["hours"]
        minutes = self.duration_dict["minutes"]
        seconds = self.duration_dict["seconds"]
 
        images_count = self.overall_result_dict['images_count']
        right_answers_count = self.overall_result_dict['right_answers_count']
        overall_result_percentage = round(self.overall_result_dict['overall_result_percentage'],1)
        
        lines = []

        lines.append("+===================================================================================================+")
        lines.append("| PARABÉNS, PARTICIPANTE {:d}!".format(self.volunteer_id))
        lines.append("+===================================================================================================+")
        lines.append("")
        lines.append("    Você concluiu o desafio de memória. Veja abaixo como você se saiu.")
        lines.append("")
        lines.append("+---------------------------------------------------------------------------------------------------+")
        lines.append("|  QUANTO TEMPO VOCÊ GASTOU FAZENDO O TESTE?                                                        |")
        lines.append("+---------------------------------------------------------------------------------------------------+")
        lines.append("")
        lines.append(f"    Você gastou {minutes} minutos e {seconds} segundos para finalizar o desafio.")
        lines.append("")
        lines.append("+---------------------------------------------------------------------------------------------------+")
        lines.append("|  COMO VOCÊ FOI NO GERAL?                                                                          |")
        lines.append("+---------------------------------------------------------------------------------------------------+")
        lines.append("")
        lines.append(f"    - Você teve contato com {images_count} imagens! ")
        lines.append(f"    - Acertou {right_answers_count}!")
        lines.append(f"    - O que representa {overall_result_percentage}% do total!")
        lines.append("")
        lines.append("+---------------------------------------------------------------------------------------------------+")
        lines.append("|  QUAL TIPO DE IMAGEM VOCÊ LEMBROU MAIS?                                                           |")
        lines.append("+---------------------------------------------------------------------------------------------------+")
        lines.append("")
        lines.append("    +-----------------------+-----------------------+-----------------------+-----------------------+")
        lines.append("    |  Tipo de imagem       |     Qtde. acertos     |     Qtde. Imagens     | Porcentagem de acerto |")
        lines.append("    +-----------------------+-----------------------+-----------------------+-----------------------+")
        
        for record in self.result_per_class_records:
            image_class = self.IMAGE_LABEL_MAP[record["image_class"]]
            is_right_answer = record["is_right_answer"]
            count = record["count"]
            right_perc = record["right_perc"]
            lines.append("    | {:21s} | {:21d} | {:21d} | {:20.1f}% | ".format(image_class, is_right_answer, count, right_perc))

        lines.append("    +-----------------------+-----------------------+-----------------------+-----------------------+")

        report = "\n"
        for line in lines:
            report = report + line + "\n"
        
        return report

    #-------------------------------------------------------------------------
    def print_report(self):
    #-------------------------------------------------------------------------
        print(self.report)

    #-------------------------------------------------------------------------
    def save_report(self):
    #-------------------------------------------------------------------------

        file_full_name = (
            self.log_path 
            + "{:04d}_report.txt".format(self.volunteer_id)
        )

        f = open(file_full_name, "a")
        
        for line in self.report:
            f.write(line)

        f.close()