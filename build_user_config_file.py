import sys
from files import Files
from aux_funcs import (
    getYAML,
    getMaxEven,
    get_file_names
)
from random import seed
import yaml

## ----------------------------------------------------------------------------
## Input parameters
## ----------------------------------------------------------------------------
user_id = int(sys.argv[1])
user_random_seed = int(user_id)

print("user_random_seed = {:d}".format(user_random_seed))

## ----------------------------------------------------------------------------
## Other parameters
## ----------------------------------------------------------------------------
#-
seed(user_random_seed)
USER_CONFIG_FILE_NAME = 'user_config.yaml'
SOFTWARE_CONFIG_FILENAME = "software_config.yaml"
cross_image_name = "cross.jpg"

# --------------------------------------
# Study Phase
# --------------------------------------

software_config_dict = getYAML(SOFTWARE_CONFIG_FILENAME)

STUDY_PHASE_POSITIVE_IMAGES_QUANTITY = software_config_dict['study_phase_positive_images_quantity']
STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY = software_config_dict["study_phase_neutral_images_quantity"]

STUDY_PHASE_NEGATIVE_HUMAN_IMAGES_QUANTITY = software_config_dict["study_phase_negative_human_images_quantity"]
STUDY_PHASE_NEGATIVE_ANIMAL_IMAGES_QUANTITY = software_config_dict["study_phase_negative_animal_images_quantity"]
STUDY_PHASE_NEGATIVE_SPIDER_IMAGES_QUANTITY = software_config_dict["study_phase_negative_spider_images_quantity"]
STUDY_PHASE_NEGATIVE_SNAKE_IMAGES_QUANTITY = software_config_dict["study_phase_negative_snake_images_quantity"]
STUDY_PHASE_NEGATIVE_IMAGES_QUANTITY = software_config_dict["study_phase_negative_all_images_quantity"]
STUDY_PHASE_ALL_NEGATIVE_IMAGES_QUANTITY = (
    STUDY_PHASE_NEGATIVE_HUMAN_IMAGES_QUANTITY
    + STUDY_PHASE_NEGATIVE_ANIMAL_IMAGES_QUANTITY
    + STUDY_PHASE_NEGATIVE_SPIDER_IMAGES_QUANTITY
    + STUDY_PHASE_NEGATIVE_SNAKE_IMAGES_QUANTITY
)
if STUDY_PHASE_ALL_NEGATIVE_IMAGES_QUANTITY != STUDY_PHASE_NEGATIVE_IMAGES_QUANTITY:
    print(
        """
            Error: the sum of all negative image quantities is different
            from what was declared in study_phase_negative_all_images_quantity.
            ({})
        """.format(SOFTWARE_CONFIG_FILENAME)
    )

STUDY_PHASE_BUFFER_IMAGES_QUANTITY = software_config_dict["study_phase_buffer_images_quantity"]

STUDY_PHASE_IMAGES_QUANTITY = (
    STUDY_PHASE_POSITIVE_IMAGES_QUANTITY
    + STUDY_PHASE_ALL_NEGATIVE_IMAGES_QUANTITY
    + STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY
    + STUDY_PHASE_BUFFER_IMAGES_QUANTITY
)



# --------------------------------------
# Test Phase
# --------------------------------------

# catch
TEST_PHASE_CATCH_IMAGES_QUANTITY = software_config_dict["test_phase_catch_images_quantity"]

# positive
TEST_PHASE_ADDITIONAL_POSITIVE_IMAGES_QUANTITY = STUDY_PHASE_POSITIVE_IMAGES_QUANTITY
TEST_PHASE_All_POSITIVE_IMAGES_QUANTITY = (
    STUDY_PHASE_POSITIVE_IMAGES_QUANTITY
    + TEST_PHASE_ADDITIONAL_POSITIVE_IMAGES_QUANTITY
)
# neutral
TEST_PHASE_ADDITIONAL_NEUTRAL_IMAGES_QUANTITY = STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY
TEST_PHASE_ALL_NEUTRAL_IMAGES_QUANTITY = (
    STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY
    + TEST_PHASE_ADDITIONAL_NEUTRAL_IMAGES_QUANTITY
)
# buffer
TEST_PHASE_ADDITIONAL_BUFFER_IMAGES_QUANTITY = 0
TEST_PHASE_ALL_BUFFER_IMAGES_QUANTITY = 0

# negative
TEST_PHASE_ADDITIONAL_NEGATIVE_HUMAN_IMAGES_QUANTITY = STUDY_PHASE_NEGATIVE_HUMAN_IMAGES_QUANTITY
TEST_PHASE_ADDITIONAL_NEGATIVE_ANIMAL_IMAGES_QUANTITY = STUDY_PHASE_NEGATIVE_ANIMAL_IMAGES_QUANTITY
TEST_PHASE_ADDITIONAL_NEGATIVE_SPIDER_IMAGES_QUANTITY = STUDY_PHASE_NEGATIVE_SPIDER_IMAGES_QUANTITY
TEST_PHASE_ADDITIONAL_NEGATIVE_SNAKE_IMAGES_QUANTITY = STUDY_PHASE_NEGATIVE_SNAKE_IMAGES_QUANTITY
TEST_PHASE_ADDITIONAL_NEGATIVE_IMAGES_QUANTITY = (
    TEST_PHASE_ADDITIONAL_NEGATIVE_HUMAN_IMAGES_QUANTITY
    + TEST_PHASE_ADDITIONAL_NEGATIVE_ANIMAL_IMAGES_QUANTITY
    + TEST_PHASE_ADDITIONAL_NEGATIVE_SPIDER_IMAGES_QUANTITY
    + TEST_PHASE_ADDITIONAL_NEGATIVE_SNAKE_IMAGES_QUANTITY
)
TEST_PHASE_ALL_NEGATIVE_IMAGES_QUANTITY = (
    STUDY_PHASE_ALL_NEGATIVE_IMAGES_QUANTITY
    + TEST_PHASE_ADDITIONAL_NEGATIVE_IMAGES_QUANTITY
)

TEST_PHASE_ALL_IMAGES_QUANTITY = (
    TEST_PHASE_CATCH_IMAGES_QUANTITY
    + TEST_PHASE_All_POSITIVE_IMAGES_QUANTITY
    + TEST_PHASE_ALL_NEUTRAL_IMAGES_QUANTITY
    + TEST_PHASE_ALL_BUFFER_IMAGES_QUANTITY
    + TEST_PHASE_ALL_NEGATIVE_IMAGES_QUANTITY 
)

TOTAL_NUMBER_OF_IMAGES = (
    STUDY_PHASE_POSITIVE_IMAGES_QUANTITY
    + STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY
    + STUDY_PHASE_ALL_NEGATIVE_IMAGES_QUANTITY
    + STUDY_PHASE_BUFFER_IMAGES_QUANTITY
    + TEST_PHASE_ADDITIONAL_POSITIVE_IMAGES_QUANTITY
    + TEST_PHASE_ADDITIONAL_NEUTRAL_IMAGES_QUANTITY
    + TEST_PHASE_ADDITIONAL_NEGATIVE_IMAGES_QUANTITY
    + TEST_PHASE_CATCH_IMAGES_QUANTITY
)

## ----------------------------------------------------------------------------
## Files list and Number of files per image category
## ----------------------------------------------------------------------------

cross_image_path = software_config_dict["cross_image_path"]
catch_images_path = software_config_dict["catch_stimuli_images_path"]

buffer_stimuli_images_path = software_config_dict["buffer_stimuli_images_path"]
GAPED_positive_images_path = software_config_dict["GAPED_positive_images_path"]

GAPED_neutral_images_path = software_config_dict["GAPED_neutral_images_path"]
GAPED_snakes_images_path = software_config_dict["GAPED_snakes_images_path"]
GAPED_spiders_images_path = software_config_dict["GAPED_spiders_images_path"]
GAPED_human_concerns_images_path = software_config_dict["GAPED_human_concerns_images_path"]
GAPED_animal_concerns_images_path = software_config_dict["GAPED_animal_concerns_images_path"]

if buffer_stimuli_images_path == GAPED_neutral_images_path:
    print("Warning: buffer path = GAPED_neutral_images_path")

images_dict = {
    "cross": {"path": cross_image_path},
    "catch": {"path": catch_images_path},
    "buffer": {"path": buffer_stimuli_images_path},
    "positive": {"path": GAPED_positive_images_path},
    "neutral": {"path": GAPED_neutral_images_path},
    "negative_snakes": {"path": GAPED_snakes_images_path},
    "negative_spiders": {"path": GAPED_spiders_images_path},
    "negative_human_concerns": {"path": GAPED_human_concerns_images_path},
    "negative_animal_concerns": {"path": GAPED_animal_concerns_images_path}
}

for image_class in images_dict.keys():
    image_list, image_count = get_file_names(images_dict[image_class]["path"])
    images_dict[image_class]["image_count"] = image_count
    images_dict[image_class]["image_list"] = image_list
    
images_dict["negative_all"] = {
    "path": None,
    "image_count":(
        images_dict["negative_snakes"]["image_count"]
        + images_dict["negative_spiders"]["image_count"]
        + images_dict["negative_human_concerns"]["image_count"]
        + images_dict["negative_animal_concerns"]["image_count"]
    ),
    "image_list": (
        images_dict["negative_snakes"]["image_list"]
        + images_dict["negative_spiders"]["image_list"]
        + images_dict["negative_human_concerns"]["image_list"]
        + images_dict["negative_animal_concerns"]["image_list"]
    )
}

## ----------------------------------------------------------------------------
## Check image count limits
## ----------------------------------------------------------------------------

positive_total = images_dict["positive"]["image_count"]
neutral_total = images_dict["neutral"]["image_count"]

animal_concern_total = images_dict["negative_animal_concerns"]["image_count"]
human_concern_total = images_dict["negative_human_concerns"]["image_count"]
snake_total = images_dict["negative_snakes"]["image_count"]
spider_total = images_dict["negative_spiders"]["image_count"]

negative_total = (
    animal_concern_total
    + human_concern_total
    + snake_total
    + spider_total
)

positive_images_count_needed = (
    STUDY_PHASE_POSITIVE_IMAGES_QUANTITY 
    + TEST_PHASE_ADDITIONAL_POSITIVE_IMAGES_QUANTITY
)

if positive_images_count_needed > positive_total:
    print("Error: no enough positive images.")

negative_images_count_needed = (
    STUDY_PHASE_NEGATIVE_IMAGES_QUANTITY 
    + TEST_PHASE_ADDITIONAL_NEGATIVE_IMAGES_QUANTITY
)

if negative_images_count_needed > negative_total:
    print("Error: no enough negative images.")


### Neutral images available for Neutral and Buffer

neutral_images_count_needed = (
    STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY
    + STUDY_PHASE_BUFFER_IMAGES_QUANTITY
    + TEST_PHASE_ADDITIONAL_NEUTRAL_IMAGES_QUANTITY
    + TEST_PHASE_ADDITIONAL_BUFFER_IMAGES_QUANTITY
)

if images_dict["neutral"]["path"] == images_dict["buffer"]["path"]:
    neutral_images_count_available = images_dict["neutral"]["image_count"]
else:
    neutral_images_count_available = (
        images_dict["neutral"]["image_count"]
        + images_dict["buffer"]["image_count"]
    )
    
if neutral_images_count_needed > neutral_images_count_available:
    print("""
    =====================================================
        Error!! There is no enough neutral images 
        for neutral and buffer.
    =====================================================
    """
    )


print("""
    ===========================================================
    Number of neutral images needed
    ===========================================================
    STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY ...............: {}
    STUDY_PHASE_BUFFER_IMAGES_QUANTITY ................: {}
    TEST_PHASE_ADDITIONAL_NEUTRAL_IMAGES_QUANTITY .....: {}
    TEST_PHASE_ADDITIONAL_BUFFER_IMAGES_QUANTITY ......: {}
    -----------------------------------------------------------
    neutral_images_count_needed .......................: {}
    
    
    ===========================================================
    Number of neutral images available
    ===========================================================
    neutral_images_count_available ....................: {}
    
    ===========================================================
    Difference
    ===========================================================
    Difference ........................................: {}
    """.format(
        STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY,
        STUDY_PHASE_BUFFER_IMAGES_QUANTITY,
        TEST_PHASE_ADDITIONAL_NEUTRAL_IMAGES_QUANTITY,
        TEST_PHASE_ADDITIONAL_BUFFER_IMAGES_QUANTITY,
        neutral_images_count_needed,
        neutral_images_count_available,
        (
            neutral_images_count_available
            - neutral_images_count_needed
        )
    
    )
)

print(f"""
    +=========================================================================+
    | USER CONFIG IMAGE PARAMETERS                                            |
    +=========================================================================+

    +-------------------------------------------------------------------------+
    | Total number of images: {TOTAL_NUMBER_OF_IMAGES}                                             |
    +-------------------------------------------------------------------------+

    +-------------------------------------------------------------------------+
    | Number of images for each class                                         |
    +-------------------------------------------------------------------------+

      -----------------------------------------------------------------------
      Positive images: {STUDY_PHASE_POSITIVE_IMAGES_QUANTITY+TEST_PHASE_ADDITIONAL_POSITIVE_IMAGES_QUANTITY}
      -----------------------------------------------------------------------
           Study phase .....................: {STUDY_PHASE_POSITIVE_IMAGES_QUANTITY:02d}
           Test phase - additional images ..: {TEST_PHASE_ADDITIONAL_POSITIVE_IMAGES_QUANTITY:02d}
           Test phase - all images .........: {TEST_PHASE_All_POSITIVE_IMAGES_QUANTITY:02d}

      -----------------------------------------------------------------------
      Neutral images: {STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY+TEST_PHASE_ADDITIONAL_NEUTRAL_IMAGES_QUANTITY}
      -----------------------------------------------------------------------
           Study phase .....................: {STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY:02d}
           Test phase - additional images ..: {TEST_PHASE_ADDITIONAL_NEUTRAL_IMAGES_QUANTITY:02d}
           Test phase - all images .........: {TEST_PHASE_ALL_NEUTRAL_IMAGES_QUANTITY:02d}

      -----------------------------------------------------------------------
      Buffer images: {STUDY_PHASE_BUFFER_IMAGES_QUANTITY+TEST_PHASE_ADDITIONAL_BUFFER_IMAGES_QUANTITY}
      -----------------------------------------------------------------------
           Study phase .....................: {STUDY_PHASE_BUFFER_IMAGES_QUANTITY:02d}
           Test phase - additional images ..: {TEST_PHASE_ADDITIONAL_BUFFER_IMAGES_QUANTITY:02d}
           Test phase - all images .........: {TEST_PHASE_ALL_BUFFER_IMAGES_QUANTITY:02d}

      -----------------------------------------------------------------------
      Catch images: {TEST_PHASE_CATCH_IMAGES_QUANTITY}
      -----------------------------------------------------------------------
           Study phase .....................: {0:02d}
           Test phase - additional images ..: {TEST_PHASE_CATCH_IMAGES_QUANTITY:02d}
           Test phase - all images .........: {TEST_PHASE_CATCH_IMAGES_QUANTITY:02d}

      -----------------------------------------------------------------------
      Negative images: {STUDY_PHASE_ALL_NEGATIVE_IMAGES_QUANTITY+TEST_PHASE_ADDITIONAL_NEGATIVE_IMAGES_QUANTITY}
      -----------------------------------------------------------------------

           Study phase .....................: {STUDY_PHASE_ALL_NEGATIVE_IMAGES_QUANTITY:02d}
                                           --------
               Animal concerns              : {STUDY_PHASE_NEGATIVE_ANIMAL_IMAGES_QUANTITY:02d}
               Human concerns               : {STUDY_PHASE_NEGATIVE_HUMAN_IMAGES_QUANTITY:02d}
               Snakes                       : {STUDY_PHASE_NEGATIVE_SNAKE_IMAGES_QUANTITY:02d}
               Spiders                      : {STUDY_PHASE_NEGATIVE_SPIDER_IMAGES_QUANTITY:02d}
               
           Test phase - additional images ..: {TEST_PHASE_ADDITIONAL_NEGATIVE_IMAGES_QUANTITY}
                                           -------- 
               Animal concerns              : {TEST_PHASE_ADDITIONAL_NEGATIVE_ANIMAL_IMAGES_QUANTITY}
               Human concerns               : {TEST_PHASE_ADDITIONAL_NEGATIVE_HUMAN_IMAGES_QUANTITY}
               Snakes                       : {TEST_PHASE_ADDITIONAL_NEGATIVE_SNAKE_IMAGES_QUANTITY}
               Spiders                      : {TEST_PHASE_ADDITIONAL_NEGATIVE_SPIDER_IMAGES_QUANTITY}

           Test phase - all images .........: {TEST_PHASE_ALL_NEGATIVE_IMAGES_QUANTITY} 

"""
)


if neutral_images_count_needed > neutral_images_count_available:
    neutral_count = getMaxEven(neutral_images_count_available)
    print("Maximum even number for available neutral images: ", neutral_count)

    print("+==========+===================+===============+==============+================+")
    print("| n_buffer | neutral_available | neutral_study | neutral_test | divisible by 4 |")
    print("+==========+===================+===============+==============+================+")
    for n_buffer in range(2, neutral_count+2, 2):
        neutral_available = neutral_count - n_buffer
        neutral_study = int(neutral_available / 2)
        neutral_test = neutral_study
        if neutral_study % 4 == 0:
            divisible4_str = "*"
        else:
            divisible4_str = " "
        row = "|  {:4d}    |       {:4d}        |     {:4d}      |    {:4d}      |       {}        |"
        print(
            row.format(
                n_buffer,
                neutral_available,
                neutral_study,
                neutral_test,
                divisible4_str
            )
        )
    print("+==========+===================+===============+==============+================+")
    
## ----------------------------------------------------------------------------
## Execution
## ----------------------------------------------------------------------------

files_ = Files(is_creating_user_config_file=True)

positive_list_all = files_.getRandomImageNames(
    imageType='positive', 
    n=STUDY_PHASE_POSITIVE_IMAGES_QUANTITY*2
)

positive_list = positive_list_all[:STUDY_PHASE_POSITIVE_IMAGES_QUANTITY]
positive_list_additional = positive_list_all[STUDY_PHASE_POSITIVE_IMAGES_QUANTITY:]

neutral_images_needed_count = (
    STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY
    + STUDY_PHASE_BUFFER_IMAGES_QUANTITY
    + TEST_PHASE_ADDITIONAL_NEUTRAL_IMAGES_QUANTITY
)

neutral_list_all = files_.getRandomImageNames(
    imageType='neutral', 
    n=neutral_images_needed_count
)

#----------------------------------------

buffer_list = neutral_list_all[
    :STUDY_PHASE_BUFFER_IMAGES_QUANTITY
]

neutral_list = neutral_list_all[
    STUDY_PHASE_BUFFER_IMAGES_QUANTITY
    :STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY+STUDY_PHASE_BUFFER_IMAGES_QUANTITY
]

neutral_list_additional = neutral_list_all[
    STUDY_PHASE_NEUTRAL_IMAGES_QUANTITY+STUDY_PHASE_BUFFER_IMAGES_QUANTITY
    :
]


negative_human_all = files_.getRandomImageNames('negative_human_concerns', n = STUDY_PHASE_NEGATIVE_HUMAN_IMAGES_QUANTITY * 2)
negative_human = negative_human_all[:STUDY_PHASE_NEGATIVE_HUMAN_IMAGES_QUANTITY]
negative_human_additional = negative_human_all[STUDY_PHASE_NEGATIVE_HUMAN_IMAGES_QUANTITY:]

negative_animal_all = files_.getRandomImageNames('negative_animal_concerns', n = STUDY_PHASE_NEGATIVE_ANIMAL_IMAGES_QUANTITY * 2)
negative_animal = negative_animal_all[:STUDY_PHASE_NEGATIVE_ANIMAL_IMAGES_QUANTITY]
negative_animal_additional = negative_animal_all[STUDY_PHASE_NEGATIVE_ANIMAL_IMAGES_QUANTITY:]

negative_spider_all = files_.getRandomImageNames('negative_spiders', n = STUDY_PHASE_NEGATIVE_SPIDER_IMAGES_QUANTITY * 2)
negative_spider = negative_spider_all[:STUDY_PHASE_NEGATIVE_SPIDER_IMAGES_QUANTITY]
negative_spider_additional = negative_spider_all[STUDY_PHASE_NEGATIVE_SPIDER_IMAGES_QUANTITY:]

negative_snake_all = files_.getRandomImageNames('negative_snakes', n = STUDY_PHASE_NEGATIVE_SNAKE_IMAGES_QUANTITY * 2)
negative_snake = negative_snake_all[:STUDY_PHASE_NEGATIVE_SNAKE_IMAGES_QUANTITY]
negative_snake_additional = negative_snake_all[STUDY_PHASE_NEGATIVE_SNAKE_IMAGES_QUANTITY:]

catch_images_quantity = TEST_PHASE_CATCH_IMAGES_QUANTITY
catch_stimuli_images_list = files_.getRandomImageNames("catch_stimuli", n = catch_images_quantity)

yaml_dict = {
    "user_id": user_id,
    "user_random_seed": user_random_seed,
    "cross_image_path": cross_image_path,
    "cross_image_name": cross_image_name,
    "catch_images_path": catch_images_path,
    "buffer_stimuli_images_path": buffer_stimuli_images_path,
    "GAPED_positive_images_path": GAPED_positive_images_path,
    "GAPED_neutral_images_path": GAPED_neutral_images_path,
    "GAPED_snakes_images_path": GAPED_snakes_images_path,
    "GAPED_spiders_images_path": GAPED_spiders_images_path,
    "GAPED_human_concerns_images_path": GAPED_human_concerns_images_path,
    "GAPED_animal_concerns_images_path": GAPED_animal_concerns_images_path,
    "selected_positive_images": positive_list,
    "additional_positive_images": positive_list_additional,
    "selected_neutral_images": neutral_list,
    "additional_neutral_images": neutral_list_additional,
    "selected_buffer_stimuli_images": buffer_list,
    "selected_snake_images": negative_snake,
    "additional_snake_images": negative_snake_additional,
    "selected_spider_images": negative_spider,
    "additional_spider_images": negative_spider_additional,
    "selected_human_concerns_images": negative_human,
    "additional_human_concerns_images": negative_human_additional,
    "selected_animal_concerns_images": negative_animal,
    "additional_animal_concerns_images": negative_animal_additional,
    "catch_stimuli_images_path": catch_images_path,
    "catch_stimuli_images_list": catch_stimuli_images_list
    
}

f = open(USER_CONFIG_FILE_NAME, 'w+')
yaml.dump(yaml_dict, f, allow_unicode=False)
f.close()