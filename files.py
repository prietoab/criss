from os import listdir
from os.path import isfile, join
from random import choice, seed
from aux_funcs import getYAML

class Files:

    IMAGE_TYPES = [
        "positive",
        "neutral",
        "buffer_stimuli",
        "negative_snakes",
        "negative_spiders",
        "negative_human_concerns",
        "negative_animal_concerns",
        "negative_all", 
        "catch_stimuli"
    ]
    #-------------------------------------------------------------------------
    def __init__(
        self, 
        userConfigYAMLfile='user_config.yaml', 
        softwareConfigYAMLfile='software_config.yaml',
        is_creating_user_config_file = False
    ):
    #-------------------------------------------------------------------------

        # -----------------------------------
        # Software configuration file
        # -----------------------------------
        self.softwareConfigYAMLfile = softwareConfigYAMLfile
        self.dictSoftwareConfig = getYAML(softwareConfigYAMLfile)
        self.image_delay_correction_factor = self.dictSoftwareConfig['image_delay_correction_factor']

        # Image paths
        self.positiveImagesPath = self.dictSoftwareConfig['GAPED_positive_images_path']
        self.negativeImagesPath_snakes = self.dictSoftwareConfig['GAPED_snakes_images_path']
        self.negativeImagesPath_spiders = self.dictSoftwareConfig['GAPED_spiders_images_path']
        self.negativeImagesPath_humanConcerns = self.dictSoftwareConfig['GAPED_human_concerns_images_path']
        self.negativeImagesPath_animalConcerns = self.dictSoftwareConfig['GAPED_animal_concerns_images_path']
        self.neutralImagesPath = self.dictSoftwareConfig['GAPED_neutral_images_path']
        self.bufferStimuliImagesPath = self.dictSoftwareConfig['buffer_stimuli_images_path']
        self.crossImagePath = self.dictSoftwareConfig['cross_image_path']
        self.crossImageFileName = self.dictSoftwareConfig['cross_image_name']
        self.catchStimuliImagesPath = self.dictSoftwareConfig['catch_stimuli_images_path']
        
        # Get images file name list
        self.positiveImagesFileList = self.getFileNames(self.positiveImagesPath)
        self.neutralImagesFileList = self.getFileNames(self.neutralImagesPath)
        self.bufferStimuliImagesList = self.getFileNames(self.bufferStimuliImagesPath)
        self.negativeImagesFileList_snakes = self.getFileNames(self.negativeImagesPath_snakes)
        self.negativeImagesFileList_spiders = self.getFileNames(self.negativeImagesPath_spiders)
        self.negativeImagesFileList_humanConcerns = self.getFileNames(self.negativeImagesPath_humanConcerns)
        self.negativeImagesFileList_animalConcerns = self.getFileNames(self.negativeImagesPath_animalConcerns)
        self.negativeImagesFileList_all =   self.negativeImagesFileList_snakes + \
                                            self.negativeImagesFileList_spiders + \
                                            self.negativeImagesFileList_humanConcerns + \
                                            self.negativeImagesFileList_animalConcerns
        self.catchStimuliImagesFileList = self.getFileNames(self.catchStimuliImagesPath)

        self.dictImageTypesFileList = {
            self.IMAGE_TYPES[0]: {'fileList': self.positiveImagesFileList},
            self.IMAGE_TYPES[1]: {'fileList': self.neutralImagesFileList},
            self.IMAGE_TYPES[2]: {'fileList': self.bufferStimuliImagesList},
            self.IMAGE_TYPES[3]: {'fileList': self.negativeImagesFileList_snakes},
            self.IMAGE_TYPES[4]: {'fileList': self.negativeImagesFileList_spiders},
            self.IMAGE_TYPES[5]: {'fileList': self.negativeImagesFileList_humanConcerns},
            self.IMAGE_TYPES[6]: {'fileList': self.negativeImagesFileList_animalConcerns},
            self.IMAGE_TYPES[7]: {'fileList': self.negativeImagesFileList_all}, 
            self.IMAGE_TYPES[8]: {'fileList': self.catchStimuliImagesFileList}
        }

        # -----------------------------------
        # User configuration file
        # -----------------------------------
        self.configYAMLfile = userConfigYAMLfile
        if is_creating_user_config_file == False:
            self.dictConfig = getYAML(userConfigYAMLfile)
        
            # Seed random generator        
            self.random_seed = self.dictConfig['user_random_seed']
            seed(self.random_seed)
        
            # User information
            self.userID = self.dictConfig['user_id']

            # Selected images for the Study Phase
            self.dictSelectedImages = {
                self.IMAGE_TYPES[0]: self.dictConfig['selected_positive_images'],
                self.IMAGE_TYPES[1]: self.dictConfig['selected_neutral_images'],
                self.IMAGE_TYPES[2]: self.dictConfig['selected_buffer_stimuli_images'],
                self.IMAGE_TYPES[3]: self.dictConfig['selected_snake_images'],
                self.IMAGE_TYPES[4]: self.dictConfig['selected_spider_images'],
                self.IMAGE_TYPES[5]: self.dictConfig['selected_human_concerns_images'],
                self.IMAGE_TYPES[6]: self.dictConfig['selected_animal_concerns_images'],
                self.IMAGE_TYPES[7]: {'fileList': self.dictConfig['selected_snake_images'] + \
                                            self.dictConfig['selected_spider_images'] + \
                                            self.dictConfig['selected_human_concerns_images'] + \
                                            self.dictConfig['selected_animal_concerns_images']}
            }

            # Additional selected images for the Test Phase
            self.dictAdditionalImages = {
                self.IMAGE_TYPES[0]: self.dictConfig['additional_positive_images'],
                self.IMAGE_TYPES[1]: self.dictConfig['additional_neutral_images'],
                self.IMAGE_TYPES[3]: self.dictConfig['additional_snake_images'],
                self.IMAGE_TYPES[4]: self.dictConfig['additional_spider_images'],
                self.IMAGE_TYPES[5]: self.dictConfig['additional_human_concerns_images'],
                self.IMAGE_TYPES[6]: self.dictConfig['additional_animal_concerns_images'],
                self.IMAGE_TYPES[7]: {'fileList': self.dictConfig['additional_snake_images'] + \
                                            self.dictConfig['additional_spider_images'] + \
                                            self.dictConfig['additional_human_concerns_images'] + \
                                            self.dictConfig['additional_animal_concerns_images']}
            }
            # Catch images for the Test Phase
            self.dictCatchImages = {
                self.IMAGE_TYPES[8]: self.dictConfig['catch_stimuli_images_list']
            }

    #-------------------------------------------------------------------------
    def getFileNames(self, strPath, sort_names=True):
    #-------------------------------------------------------------------------
        # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
        fileNamesList = [f for f in listdir(strPath) if isfile(join(strPath, f))]
        if sort_names:
            fileNamesList.sort()
        return fileNamesList

    #-------------------------------------------------------------------------
    def getRandomImageNames(self, imageType, n=10):
    #-------------------------------------------------------------------------
        if imageType in self.IMAGE_TYPES:
            selected_image_count = 0
            number_of_images_to_be_selected = n
            randomImageNames = []
            while selected_image_count < number_of_images_to_be_selected:
                strRandomImageName = choice(self.dictImageTypesFileList[imageType]['fileList'])
                if strRandomImageName not in randomImageNames:
                    randomImageNames.append(strRandomImageName)
                    selected_image_count += 1
        else:
            print('Invalid imageType: ' + str(imageType))
            print('Expected: ' + str(self.dictImageTypesFileList.keys()))
            randomImageNames = None

        return randomImageNames
