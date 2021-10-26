from aux_funcs import isEven, getYAML
from random import shuffle, seed

class TestPhase:    

    ANSWER_YES_ = 'yes'
    ANSWER_NO_ = 'no'
    ANSWER_CATCH_IMAGE = 'catch_image'
    ANSWER_TYPES_ = [ANSWER_YES_,ANSWER_NO_,ANSWER_CATCH_IMAGE]

    EVENT_TYPE_INSTRUCTIONS_ = 'instructions'
    EVENT_TYPE_IMAGE_ = 'image'
    EVENT_TYPE_ANSWER_ = 'answer'
    EVENT_TYPE_END_ = 'end'
    EVENT_TYPES_ = [EVENT_TYPE_INSTRUCTIONS_, EVENT_TYPE_IMAGE_, EVENT_TYPE_ANSWER_, EVENT_TYPE_END_]

    PHASE_NAME_ = 'test_phase'

    #------------------------------------------------------------------------------------------
    def __init__(
        self, 
        filesInstance, 
        softwareConfigYAMLfile='software_config.yaml', 
        random_seed=0
        ):
    #------------------------------------------------------------------------------------------        
        self.filesInstance = filesInstance
        self.dictSoftwareConfig = getYAML(softwareConfigYAMLfile)
        
        #self.random_seed = self.dictSoftwareConfig['random_seed']
        self.random_seed = random_seed
        seed(self.random_seed)

        self.delayCross = int(self.dictSoftwareConfig['study_phase_central_fixation_cross_delay'])
        self.delayImage = int(self.dictSoftwareConfig['study_phase_to_be_studied_image_delay'])
        self.delayCatchImage = int(self.dictSoftwareConfig['test_phase_catch_stimuli_image_delay'])
        
        self.testImageSequenceNumber = -1
        self.testPhaseImageSequence = self.getLinearImageSequence(shuffleImages=True)
        self.testImageCount = len(self.testPhaseImageSequence)

    #------------------------------------------------------------------------------------------
    def currentImage(self):
    #------------------------------------------------------------------------------------------
        returnCode = -1
        imageName = None
        imagePath = None
        imageType = None
        imageDelay = None
        imageWasInStudyPhase = None

        if self.testImageSequenceNumber < self.testImageCount:
            returnCode = 0
            imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase = self.testPhaseImageSequence[self.testImageSequenceNumber]

        return returnCode, imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase

    #------------------------------------------------------------------------------------------
    def processAnswer(self, answer, logInstance):
    #------------------------------------------------------------------------------------------
        currentImageReturnCode, imageName, _, imageType, _, imageWasInStudyPhase = self.currentImage()
        if currentImageReturnCode == 0:
            logInstance.log(phaseName = TestPhase.PHASE_NAME_, 
                            eventType = TestPhase.EVENT_TYPE_ANSWER_,
                            imgName = imageName, 
                            imgType = imageType, 
                            inStudyPhase = imageWasInStudyPhase, 
                            answer = answer
            )
        return currentImageReturnCode

    #------------------------------------------------------------------------------------------
    def nextImage(self, logInstance):
    #------------------------------------------------------------------------------------------
        returnCode = -1
        imageName = None
        imagePath = None
        imageType = None
        imageDelay = None
        imageWasInStudyPhase = None
        
        self.testImageSequenceNumber += 1
        
        if self.testImageSequenceNumber < self.testImageCount:
            returnCode = 0
            imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase = self.testPhaseImageSequence[self.testImageSequenceNumber]
            print("A")
            logInstance.log(phaseName = 'test_phase', 
                            eventType = TestPhase.EVENT_TYPE_IMAGE_,
                            imgName = imageName, 
                            imgType = imageType, 
                            inStudyPhase = imageWasInStudyPhase, 
                            answer = None)
            print("B")
        return returnCode, imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase

    #------------------------------------------------------------------------------------------
    def getLinearImageSequence(self, shuffleImages=False, crossesBetweenImages=False):
    #------------------------------------------------------------------------------------------

        positiveImages              = self.getPositiveImages()
        additionalPositiveImages    = self.getAdditionalPositiveImages()

        neutralImages               = self.getNeutralImages()
        additionalNeutralImages     = self.getAdditionalNeutralImages()

        negativeImages              = self.getNegativeImages()
        additionalNegativeImages    = self.getAdditionalNegativeImages()

        catchStimuliImages          = self.getCatchStimuliImages()

        imagesToBeTested            =   positiveImages + additionalPositiveImages + \
                                        neutralImages + additionalNeutralImages + \
                                        negativeImages + additionalNegativeImages + \
                                        catchStimuliImages

        if shuffleImages:
            shuffle(imagesToBeTested)

        sequenceWithoutCrosses = imagesToBeTested

        imageReturnList = sequenceWithoutCrosses
        if crossesBetweenImages:
            imageReturnList = self.insertCrossesBetweenImages(sequenceWithoutCrosses)

        return imageReturnList

    #------------------------------------------------------------------------------------------
    def getPositiveImages(self):
    #------------------------------------------------------------------------------------------
        imagePath = self.filesInstance.positiveImagesPath
        imageDelay = self.delayImage
        imageType = 'positive'
        imageWasInStudyPhase = True
        positiveImageNamesList = self.filesInstance.dictSelectedImages[imageType]

        positiveImagesTupleList = []
        for imageName in positiveImageNamesList:
            positiveImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) )

        return positiveImagesTupleList

    #------------------------------------------------------------------------------------------
    def getAdditionalPositiveImages(self):
    #------------------------------------------------------------------------------------------
        imagePath = self.filesInstance.positiveImagesPath
        imageDelay = self.delayImage
        imageType = 'positive'
        imageWasInStudyPhase = False
        additionalPositiveImageNamesList = self.filesInstance.dictAdditionalImages[imageType]

        additionalPositiveImagesTupleList = []
        for imageName in additionalPositiveImageNamesList:
            additionalPositiveImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) )

        return additionalPositiveImagesTupleList

    #------------------------------------------------------------------------------------------
    def getNeutralImages(self):
    #------------------------------------------------------------------------------------------        
        imagePath = self.filesInstance.neutralImagesPath
        imageDelay = self.delayImage
        imageType = 'neutral'
        imageWasInStudyPhase = True
        neutralImageNamesList = self.filesInstance.dictSelectedImages[imageType]

        neutralImagesTupleList = []
        for imageName in neutralImageNamesList:
            neutralImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) )

        return neutralImagesTupleList

    #------------------------------------------------------------------------------------------
    def getAdditionalNeutralImages(self):
    #------------------------------------------------------------------------------------------
        imagePath = self.filesInstance.neutralImagesPath
        imageDelay = self.delayImage
        imageType = 'neutral'
        imageWasInStudyPhase = False
        neutralImageNamesList = self.filesInstance.dictAdditionalImages[imageType]

        neutralImagesTupleList = []
        for imageName in neutralImageNamesList:
            neutralImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) )

        return neutralImagesTupleList

    #------------------------------------------------------------------------------------------
    def getNegativeImages(self, shuffle=False):
    #------------------------------------------------------------------------------------------

        imageWasInStudyPhase = True

        # Snakes ---------------------------------------------
        imagePath = self.filesInstance.negativeImagesPath_snakes
        imageDelay = self.delayImage
        imageType = 'negative_snakes'
        snakeImageNamesList = self.filesInstance.dictSelectedImages[imageType]

        snakeImagesTupleList = []
        for imageName in snakeImageNamesList:
            snakeImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) )

        # Spiders ---------------------------------------------
        imagePath = self.filesInstance.negativeImagesPath_spiders
        imageDelay = self.delayImage
        imageType = 'negative_spiders'
        spiderImageNamesList = self.filesInstance.dictSelectedImages[imageType]

        spiderImagesTupleList = []
        for imageName in spiderImageNamesList:
            spiderImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) )        

        # Human concerns ---------------------------------------
        imagePath = self.filesInstance.negativeImagesPath_humanConcerns
        imageDelay = self.delayImage
        imageType = 'negative_human_concerns'
        humanImageNamesList = self.filesInstance.dictSelectedImages[imageType]

        humanImagesTupleList = []
        for imageName in humanImageNamesList:
            humanImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) )        

        # Animal concerns ---------------------------------------
        imagePath = self.filesInstance.negativeImagesPath_animalConcerns
        imageDelay = self.delayImage
        imageType = 'negative_animal_concerns'
        animalImageNamesList = self.filesInstance.dictSelectedImages[imageType]

        animalImagesTupleList = []
        for imageName in animalImageNamesList:
            animalImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) ) 

        # Final list ---------------------------------------
        negativeImagesTupleList =   snakeImagesTupleList + \
                                    spiderImagesTupleList + \
                                    humanImagesTupleList + \
                                    animalImagesTupleList     

        if shuffle:
            negativeImagesTupleList = shuffle(negativeImagesTupleList)

        return negativeImagesTupleList

    #------------------------------------------------------------------------------------------
    def getAdditionalNegativeImages(self, shuffle=False):
    #------------------------------------------------------------------------------------------
        imageWasInStudyPhase = False

        # Snakes ---------------------------------------------
        imagePath = self.filesInstance.negativeImagesPath_snakes
        imageDelay = self.delayImage
        imageType = 'negative_snakes'
        snakeImageNamesList = self.filesInstance.dictAdditionalImages[imageType]

        snakeImagesTupleList = []
        for imageName in snakeImageNamesList:
            snakeImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) )

        # Spiders ---------------------------------------------
        imagePath = self.filesInstance.negativeImagesPath_spiders
        imageDelay = self.delayImage
        imageType = 'negative_spiders'
        spiderImageNamesList = self.filesInstance.dictAdditionalImages[imageType]

        spiderImagesTupleList = []
        for imageName in spiderImageNamesList:
            spiderImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) )        

        # Human concerns ---------------------------------------
        imagePath = self.filesInstance.negativeImagesPath_humanConcerns
        imageDelay = self.delayImage
        imageType = 'negative_human_concerns'
        humanImageNamesList = self.filesInstance.dictAdditionalImages[imageType]

        humanImagesTupleList = []
        for imageName in humanImageNamesList:
            humanImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) )        

        # Animal concerns ---------------------------------------
        imagePath = self.filesInstance.negativeImagesPath_animalConcerns
        imageDelay = self.delayImage
        imageType = 'negative_animal_concerns'
        animalImageNamesList = self.filesInstance.dictAdditionalImages[imageType]

        animalImagesTupleList = []
        for imageName in animalImageNamesList:
            animalImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) ) 

        # Final list ---------------------------------------
        negativeImagesTupleList =   snakeImagesTupleList + \
                                    spiderImagesTupleList + \
                                    humanImagesTupleList + \
                                    animalImagesTupleList     

        if shuffle:
            negativeImagesTupleList = shuffle(negativeImagesTupleList)

        return negativeImagesTupleList

    # -----------------------------------------------------------------
    def getCatchStimuliImages(self):
    # -----------------------------------------------------------------

        imagePath = self.filesInstance.catchStimuliImagesPath
        imageDelay = self.delayCatchImage
        imageType = 'catch_stimuli'
        imageWasInStudyPhase = False
        catchStimuliImageNamesList = self.filesInstance.catchStimuliImagesFileList

        catchStimuliImagesTupleList = []
        for imageName in catchStimuliImageNamesList:
            catchStimuliImagesTupleList.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) )

        return catchStimuliImagesTupleList

    # -----------------------------------------------------------------
    def insertCrossesBetweenImages(self, imageTupleSequenceList):
    # -----------------------------------------------------------------
    
        imageTupleSequenceList_withCrosses = []
        for idxImage in range(len(imageTupleSequenceList)):
            #  The cross figure must be before
            #  every image.
            imageName = self.filesInstance.crossImageFileName
            imagePath = self.filesInstance.crossImagePath
            imageType = 'cross'
            imageDelay = self.delayCross
            imageWasInStudyPhase = True
            imageTupleSequenceList_withCrosses.append( (imageName, imagePath, imageType, imageDelay, imageWasInStudyPhase) )

            imageName, imagePath, imageType, imageDelay = imageTupleSequenceList[idxImage]
            imageTupleSequenceList_withCrosses.append( (imageName, imagePath, imageType, imageDelay) )
        return imageTupleSequenceList_withCrosses