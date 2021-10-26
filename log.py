from datetime import datetime

class Log:
    #------------------------------------------------------
    def __init__(self, filesInstance):
    #------------------------------------------------------
        self.filesInstance = filesInstance
        self.event_sequence_id = -1
        # Log file
        self.volunteerLogFilePath = "./log_files/"
        self.volunteerLogFileName = "{:04d}_user_log.csv".format(int(self.filesInstance.userID))
        self.volunteerLogFile = open(self.volunteerLogFilePath+self.volunteerLogFileName, "a")
    
    #------------------------------------------------------
    def print_head(self):
    #------------------------------------------------------
        file_head = 'volunteer_id,event_seq,timestamp,phase_name,event_type,image_name,image_type,in_study_phase,answer\n'
        self.volunteerLogFile.write(file_head)

    #------------------------------------------------------
    def closeLogFile(self):
    #------------------------------------------------------
        self.volunteerLogFile.close()

    #------------------------------------------------------
    def log(self, phaseName, eventType, imgName, imgType, inStudyPhase, answer):
    #------------------------------------------------------        
        self.event_sequence_id = self.event_sequence_id  + 1
        #--
        timestamp = str(datetime.now())
        line = "{},{},{},{},{},{},{},{},{}\n".format(self.filesInstance.userID, 
                                                self.event_sequence_id, 
                                                timestamp, 
                                                phaseName,
                                                eventType,
                                                imgName,
                                                imgType,
                                                inStudyPhase,
                                                answer)
        self.volunteerLogFile.write(line)


