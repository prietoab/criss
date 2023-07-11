from flask import (
    Flask, 
    render_template, 
    redirect, 
    url_for,
    request 
)
from time import sleep
from files import Files
from study_phase import StudyPhase
from test_phase import TestPhase
from log import Log
from volunteer_report import VolunteerResultsReport
app = Flask(__name__)

# ----------------------------------------------------------------------
@app.route('/')
def home():
# ----------------------------------------------------------------------
    global logFile

    logFile.print_head()

    logFile.log(phaseName = 'study_phase', 
            eventType = 'instructions',
            imgName = None, 
            imgType = None, 
            inStudyPhase = None, 
            answer = None)

    return render_template('study_phase_beginning.html')

# ----------------------------------------------------------------------
@app.route('/study_phase_next_image')
def study_phase_next_image():
# ----------------------------------------------------------------------

    global studyPhaseImageSequence
    global logFile
    global image_delay_correction_factor

    global studyPhaseImageIndex
    studyPhaseImageIndex += 1
    
    if studyPhaseImageIndex < len(studyPhaseImageSequence):
        imgName, _, imageType, imgDelayMiliSeconds = studyPhaseImageSequence[studyPhaseImageIndex]
        imgDelaySeconds = int(imgDelayMiliSeconds / 1000.0) * image_delay_correction_factor

        
        logFile.log(phaseName = 'study_phase', 
                    eventType = 'image',
                    imgName = imgName, 
                    imgType = imageType, 
                    inStudyPhase = None, 
                    answer = None)

        return render_template('study_phase_next_image.html', image_full_name = imgName, image_delay_seconds = imgDelaySeconds)
    else:
        return render_template('test_phase_instructions.html')
    # https://stackoverflow.com/questions/46785507/python-flask-display-image-on-a-html-page
    #

# ----------------------------------------------------------------------
@app.route('/test_phase_next_image')
def test_phase_next_image():
# ----------------------------------------------------------------------
    global testPhase
    global logFile

    returnCode, imageName, _, _, _, _ = testPhase.nextImage(logFile)

    if returnCode == 0:
        return render_template('test_phase_next_image.html', image_full_name = imageName)
    if returnCode == -1:
        return render_template('test_phase_end.html')

# ----------------------------------------------------------------------
@app.route('/test_phase_yes')
def test_phase_yes():
# ----------------------------------------------------------------------
    global testPhase
    global logFile
    
    processAnswerReturnCode = testPhase.processAnswer(testPhase.ANSWER_YES_, logFile) 

    if processAnswerReturnCode != 0:
        logFile.log(phaseName = TestPhase.PHASE_NAME_, 
                    eventType = TestPhase.EVENT_TYPE_END_,
                    imgName = None, 
                    imgType = None, 
                    inStudyPhase = None, 
                    answer = None)        
        return render_template('test_phase_end.html')

    nextImageReturnCode, imageName, _, _, _, _ = testPhase.nextImage(logFile)

    if nextImageReturnCode != 0:
        logFile.log(phaseName = TestPhase.PHASE_NAME_, 
                    eventType = TestPhase.EVENT_TYPE_END_,
                    imgName = None, 
                    imgType = None, 
                    inStudyPhase = None, 
                    answer = None)
        return render_template('test_phase_end.html')       
    else:
        return render_template('test_phase_next_image.html', image_full_name = imageName)

# ----------------------------------------------------------------------
@app.route('/test_phase_no')
def test_phase_no():
# ----------------------------------------------------------------------
    global testPhase
    global logFile

    processAnswerReturnCode = testPhase.processAnswer(testPhase.ANSWER_NO_, logFile)

    if processAnswerReturnCode != 0:
        logFile.log(phaseName = TestPhase.PHASE_NAME_, 
                    eventType = TestPhase.EVENT_TYPE_END_,
                    imgName = None, 
                    imgType = None, 
                    inStudyPhase = None, 
                    answer = None)
        return render_template('test_phase_end.html')

    nextImageReturnCode, imageName, _, _, _, _ = testPhase.nextImage(logFile)

    if nextImageReturnCode != 0:
        logFile.log(phaseName = TestPhase.PHASE_NAME_, 
                    eventType = TestPhase.EVENT_TYPE_END_,
                    imgName = None, 
                    imgType = None, 
                    inStudyPhase = None, 
                    answer = None)
        return render_template('test_phase_end.html')       
    else:
        return render_template('test_phase_next_image.html', image_full_name = imageName)



# ----------------------------------------------------------------------
@app.route('/test_phase_check_point')
def test_phase_check_point():
# ----------------------------------------------------------------------
    global testPhase
    global logFile

    processAnswerReturnCode = testPhase.processAnswer(testPhase.ANSWER_CATCH_IMAGE, logFile)

    if processAnswerReturnCode != 0:
        logFile.log(phaseName = TestPhase.PHASE_NAME_, 
                    eventType = TestPhase.EVENT_TYPE_END_,
                    imgName = None, 
                    imgType = None, 
                    inStudyPhase = None, 
                    answer = None)
        return render_template('test_phase_end.html')

    nextImageReturnCode, imageName, _, _, _, _ = testPhase.nextImage(logFile)

    if nextImageReturnCode != 0:
        logFile.log(phaseName = TestPhase.PHASE_NAME_, 
                    eventType = TestPhase.EVENT_TYPE_END_,
                    imgName = None, 
                    imgType = None, 
                    inStudyPhase = None, 
                    answer = None)
        return render_template('test_phase_end.html')       
    else:
        return render_template('test_phase_next_image.html', image_full_name = imageName)

# ----------------------------------------------------------------------
@app.route('/shutdown_server')
def shutdown_server():
# ----------------------------------------------------------------------
    # func = request.environ.get('werkzeug.server.shutdown')
    # if func is None:
    #     raise RuntimeError('Not running with the Werkzeug Server')
    # func()
    return render_template('server_stopped.html')


# ----------------------------------------------------------------------
@app.route('/volunteer_report')
def volunteer_report():
# ----------------------------------------------------------------------
    global logFile
    global arqs
    
    logFile.closeLogFile()
    report = VolunteerResultsReport(arqs.userID,logFile.volunteerLogFilePath)
    report.save_report()

    volunteer_id = arqs.userID
    minutes = report.duration_dict["minutes"]
    seconds = report.duration_dict["seconds"]

    images_count = report.overall_result_dict["images_count"]
    right_answers_count = report.overall_result_dict["right_answers_count"]
    overall_result_percentage = (
        round(report.overall_result_dict["overall_result_percentage"],1)
    )

    result_per_class_records = report.result_per_class_records
    mapa_tipo_imagens = report.IMAGE_LABEL_MAP

    tipo_imagem_01_classe = mapa_tipo_imagens[result_per_class_records[0]["image_class"]]
    tipo_imagem_01_qtde_acertos = result_per_class_records[0]["is_right_answer"]
    tipo_imagem_01_qtde_imagens = result_per_class_records[0]["count"]
    tipo_imagem_01_qtde_porcentagem_acertos = result_per_class_records[0]["right_perc"]

    tipo_imagem_02_classe = mapa_tipo_imagens[result_per_class_records[1]["image_class"]]
    tipo_imagem_02_qtde_acertos = result_per_class_records[1]["is_right_answer"]
    tipo_imagem_02_qtde_imagens = result_per_class_records[1]["count"]
    tipo_imagem_02_qtde_porcentagem_acertos = result_per_class_records[1]["right_perc"]

    tipo_imagem_03_classe = mapa_tipo_imagens[result_per_class_records[2]["image_class"]]
    tipo_imagem_03_qtde_acertos = result_per_class_records[2]["is_right_answer"]
    tipo_imagem_03_qtde_imagens = result_per_class_records[2]["count"]
    tipo_imagem_03_qtde_porcentagem_acertos = result_per_class_records[2]["right_perc"]

    tipo_imagem_04_classe = mapa_tipo_imagens[result_per_class_records[3]["image_class"]]
    tipo_imagem_04_qtde_acertos = result_per_class_records[3]["is_right_answer"]
    tipo_imagem_04_qtde_imagens = result_per_class_records[3]["count"]
    tipo_imagem_04_qtde_porcentagem_acertos = result_per_class_records[3]["right_perc"]

    return render_template(
        'volunteer_report.html',
        volunteer_id = volunteer_id,
        minutes = minutes,
        seconds = seconds,
        images_count = images_count,
        right_answers_count = right_answers_count,
        overall_result_percentage = overall_result_percentage,
        tipo_imagem_01_classe = tipo_imagem_01_classe,
        tipo_imagem_01_qtde_acertos = tipo_imagem_01_qtde_acertos,
        tipo_imagem_01_qtde_imagens = tipo_imagem_01_qtde_imagens,
        tipo_imagem_01_qtde_porcentagem_acertos = tipo_imagem_01_qtde_porcentagem_acertos,
        tipo_imagem_02_classe = tipo_imagem_02_classe,
        tipo_imagem_02_qtde_acertos = tipo_imagem_02_qtde_acertos,
        tipo_imagem_02_qtde_imagens = tipo_imagem_02_qtde_imagens,
        tipo_imagem_02_qtde_porcentagem_acertos = tipo_imagem_02_qtde_porcentagem_acertos,
        tipo_imagem_03_classe = tipo_imagem_03_classe,
        tipo_imagem_03_qtde_acertos = tipo_imagem_03_qtde_acertos,
        tipo_imagem_03_qtde_imagens = tipo_imagem_03_qtde_imagens,
        tipo_imagem_03_qtde_porcentagem_acertos = tipo_imagem_03_qtde_porcentagem_acertos,
        tipo_imagem_04_classe = tipo_imagem_04_classe,
        tipo_imagem_04_qtde_acertos = tipo_imagem_04_qtde_acertos,
        tipo_imagem_04_qtde_imagens = tipo_imagem_04_qtde_imagens,
        tipo_imagem_04_qtde_porcentagem_acertos = tipo_imagem_04_qtde_porcentagem_acertos
    )


# ----------------------------------------------------------------------    
if __name__ == "__main__":
# ----------------------------------------------------------------------
        
    arqs = Files(is_creating_user_config_file=False)

    studyPhase = StudyPhase(
        filesInstance=arqs, 
        random_seed=arqs.random_seed
    )

    global logFile
    logFile = Log(arqs)

    global studyPhaseImageSequence
    studyPhaseImageSequence = (
        studyPhase.getLinearImageSequence(
            shuffleImages=True
        )
    )

    global studyPhaseImageIndex
    studyPhaseImageIndex = -1

    global testPhase
    testPhase = TestPhase(
        filesInstance=arqs,
        random_seed=arqs.random_seed
    )

    global image_delay_correction_factor
    image_delay_correction_factor = arqs.image_delay_correction_factor

    app.run(debug=True)