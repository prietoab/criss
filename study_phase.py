from aux_funcs import isEven, getYAML
from random import shuffle, seed

class StudyPhase:
    
    #-------------------------------------------------------------------------
    def __init__(
        self, 
        filesInstance, 
        softwareConfigYAMLfile='software_config.yaml', 
        random_seed=0
        ):
    #-------------------------------------------------------------------------
        self.filesInstance = filesInstance
        self.dictSoftwareConfig = getYAML(softwareConfigYAMLfile)
        self.delayCross = int(self.dictSoftwareConfig['study_phase_central_fixation_cross_delay'])
        self.delayImage = int(self.dictSoftwareConfig['study_phase_to_be_studied_image_delay'])
        self.idxNextImage = 0
        self.random_seed = random_seed
        seed(random_seed)

    #-------------------------------------------------------------------------
    def getLinearImageSequence(
        self, 
        shuffleImages=False, 
        crossesBetweenImages=True
        ):
    #-------------------------------------------------------------------------

        firstHalfBufferImages   = self.getBufferImages('first_half')
        secondtHalfBufferImages = self.getBufferImages('second_half')

        positiveImages          = self.getPositiveImages()
        neutralImages           = self.getNeutralImages()
        negativeImages          = self.getNegativeImages()

        imagesToBeStudied       = positiveImages + neutralImages + negativeImages

        if shuffleImages:
            shuffle(imagesToBeStudied)

        print("firstHalfBufferImages: " + str(type(firstHalfBufferImages)))
        print("imagesToBeStudied: " + str(type(imagesToBeStudied)))
        print("secondtHalfBufferImages: " + str(type(secondtHalfBufferImages)))
        sequenceWithoutCrosses = firstHalfBufferImages + imagesToBeStudied + secondtHalfBufferImages

        imageReturnList = sequenceWithoutCrosses
        if crossesBetweenImages:
            imageReturnList = self.insertCrossesBetweenImages(sequenceWithoutCrosses)

        return imageReturnList

    #-------------------------------------------------------------------------
    def getPositiveImages(self):
    #-------------------------------------------------------------------------

        imagePath = self.filesInstance.positiveImagesPath
        imageDelay = self.delayImage
        imageType = 'positive'
        positiveImageNamesList = self.filesInstance.dictSelectedImages[imageType]

        positiveImagesTupleList = []
        for imageName in positiveImageNamesList:
            positiveImagesTupleList.append( (imageName, imagePath, imageType, imageDelay) )

        return positiveImagesTupleList

    #-------------------------------------------------------------------------
    def getNeutralImages(self):
    #-------------------------------------------------------------------------
        imagePath = self.filesInstance.neutralImagesPath
        imageDelay = self.delayImage
        imageType = 'neutral'
        neutralImageNamesList = self.filesInstance.dictSelectedImages[imageType]

        neutralImagesTupleList = []
        for imageName in neutralImageNamesList:
            neutralImagesTupleList.append( (imageName, imagePath, imageType, imageDelay) )

        return neutralImagesTupleList

    #-------------------------------------------------------------------------
    def getNegativeImages(self, shuffle=False):
    #-------------------------------------------------------------------------
        # Snakes ---------------------------------------------
        imagePath = self.filesInstance.negativeImagesPath_snakes
        imageDelay = self.delayImage
        imageType = 'negative_snakes'
        snakeImageNamesList = self.filesInstance.dictSelectedImages[imageType]

        snakeImagesTupleList = []
        for imageName in snakeImageNamesList:
            snakeImagesTupleList.append( (imageName, imagePath, imageType, imageDelay) )

        # Spiders ---------------------------------------------
        imagePath = self.filesInstance.negativeImagesPath_spiders
        imageDelay = self.delayImage
        imageType = 'negative_spiders'
        spiderImageNamesList = self.filesInstance.dictSelectedImages[imageType]

        spiderImagesTupleList = []
        for imageName in spiderImageNamesList:
            spiderImagesTupleList.append( (imageName, imagePath, imageType, imageDelay) )        

        # Human concerns ---------------------------------------
        imagePath = self.filesInstance.negativeImagesPath_humanConcerns
        imageDelay = self.delayImage
        imageType = 'negative_human_concerns'
        humanImageNamesList = self.filesInstance.dictSelectedImages[imageType]

        humanImagesTupleList = []
        for imageName in humanImageNamesList:
            humanImagesTupleList.append( (imageName, imagePath, imageType, imageDelay) )        

        # Animal concerns ---------------------------------------
        imagePath = self.filesInstance.negativeImagesPath_animalConcerns
        imageDelay = self.delayImage
        imageType = 'negative_animal_concerns'
        animalImageNamesList = self.filesInstance.dictSelectedImages[imageType]

        animalImagesTupleList = []
        for imageName in animalImageNamesList:
            animalImagesTupleList.append( (imageName, imagePath, imageType, imageDelay) ) 

        # Final list ---------------------------------------
        negativeImagesTupleList =   snakeImagesTupleList + \
                                    spiderImagesTupleList + \
                                    humanImagesTupleList + \
                                    animalImagesTupleList     

        if shuffle:
            negativeImagesTupleList = shuffle(negativeImagesTupleList)

        return negativeImagesTupleList

    #-------------------------------------------------------------------------
    def insertCrossesBetweenImages(self, imageTupleSequenceList):
    #-------------------------------------------------------------------------
        imageTupleSequenceList_withCrosses = []
        for idxImage in range(len(imageTupleSequenceList)):
            #  The cross figure must be before
            #  every image.
            imageName = self.filesInstance.crossImageFileName
            imagePath = self.filesInstance.crossImagePath
            imageType = 'cross'
            imageDelay = self.delayCross
            imageTupleSequenceList_withCrosses.append( (imageName, imagePath, imageType, imageDelay) )

            imageName, imagePath, imageType, imageDelay = imageTupleSequenceList[idxImage]
            imageTupleSequenceList_withCrosses.append( (imageName, imagePath, imageType, imageDelay) )
        return imageTupleSequenceList_withCrosses

    #-------------------------------------------------------------------------
    def getBufferImages(self, group):
    #-------------------------------------------------------------------------

        numberOfBufferImages = len(self.filesInstance.dictSelectedImages['buffer_stimuli'])
        
        if isEven(numberOfBufferImages) == False:
            print('numberOfBufferImages is not an even number.')
            return None

        imageTupleSequenceList = []
        
        if group == 'first_half':
            i_begin = 0
            i_end   = int(numberOfBufferImages/2)
        elif group == 'second_half':
            i_begin = int(numberOfBufferImages/2)
            i_end   = numberOfBufferImages
        else:
            print("Invalid group {}. Expected 'first_half' or 'second_half' ".format(group))
            return None

        for i_BufferImage in range(i_begin, i_end):
            imageName = self.filesInstance.dictSelectedImages['buffer_stimuli'][i_BufferImage]
            imagePath = self.filesInstance.dictConfig['buffer_stimuli_images_path']
            imageType = 'buffer_stimuli'
            imageDelay = self.delayImage
            imageTupleSequenceList.append( (imageName, imagePath, imageType, imageDelay) )

        return imageTupleSequenceList