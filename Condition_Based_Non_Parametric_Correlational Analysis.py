# This can be used to correlate two variables setting different conditions


import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import Categorization_Methods as g_methods

root_data_path = r'C:\Users\HP\Desktop\5th & 6th Semester\Bap Re Bap\CSV File\Data_Total.csv'
root_path_categories = r'C:\Users\HP\Desktop\5th & 6th Semester\Bap Re Bap\CSV File\Coded_Demographic_For_Aanlysis.csv'
corr_coef_writer = open("C:\\Users\\HP\\Desktop\\5th & 6th Semester\\Bap Re Bap\\Results"
                        "\\cc_below_SSC.txt", "a")

DEGREE = 1  # Fit a polynomial

x_axis_label = "X Axis"
y_axis_label = "Y Axis"
data_set = []
already_calculated = []
group_1_data_indices = []


# To detect outliers we are using IQR(Inter Quartile Range) method instead of using Z Score.
# The reason is, after data analysis, I have found IQR works better than Z score
# Parameter "sorted_data" must have to be sorted since IQR method needs to find median
def detect_outlier_z_score(data):
    outliers_indices = []
    threshold = 3
    mean = np.mean(data)
    std = np.std(data)

    index = 0
    for value in data:
        z_score = (value - mean) / std
        if np.abs(z_score) > threshold:
            outliers_indices.append(index)
        index += 1

    return outliers_indices


def detect_outlier_iqr(sorted_data):
    outliers_indices = []
    index = 0
    data = np.array(sorted_data)

    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    for value in data:
        if value < lower_bound or value > upper_bound:
            outliers_indices.append(index)
        index += 1
    return outliers_indices


def get_2_decimal(value):
    return str(float("{0:.4f}".format(value)))


def not_calculated_correlation(var1_name, var2_name):
    for name in already_calculated:
        if var1_name in name and var2_name in name:
            return False

    already_calculated.append(var1_name+"_"+var2_name)
    return True


def find_the_correlation(variable_1_data):

    variable_1_name = variable_1_data[len(variable_1_data)-1]
    print("Name", variable_1_name)
    variable_1_data = variable_1_data[:len(variable_1_data)-1]
    variable_1_data = np.array(variable_1_data, dtype=np.float32)
    variable_1_data_not_sorted = variable_1_data

    for variable_2_data in data_set:

        variable_1_data = variable_1_data_not_sorted

        variable_2_name = variable_2_data[len(variable_2_data)-1]
        variable_2_data = variable_2_data[:len(variable_2_data)-1]
        variable_2_data = np.array(variable_2_data, dtype=np.float32)

        if not_calculated_correlation(variable_1_name, variable_2_name):
            variable_1_data, variable_2_data = zip(*sorted(zip(variable_1_data, variable_2_data)))
            n_outlier = 0
            title = "Correlation between " + variable_1_name + " and " + variable_2_name

            if len(variable_1_data) > 0 and len(variable_2_data) > 0:

                #  Outlier detection for variable_1_data
                print("Prior to removing outliers, var 1 :N = ", len(variable_1_data))
                outliers_indices = detect_outlier_z_score(variable_1_data)

                for index in sorted(outliers_indices, reverse=True):
                    print("Outlier variable_1_data: ", variable_1_data[index])
                    # del variable_1_data[index]
                    # del variable_2_data[index]
                    n_outlier += 1

                # Outlier Detection for variable_2_data
                print("Prior to removing outliers, var 2 :N = ", len(variable_2_data))
                outliers_indices = detect_outlier_z_score(variable_2_data)

                for index in sorted(outliers_indices, reverse=True):
                    print("Outlier variable_2_data: ", variable_2_data[index])
                    # del variable_1_data[index]
                    # del variable_2_data[index]
                    n_outlier += 1

                # Spearman Correlation Coefficient and P value
                print(stats.spearmanr(variable_1_data, variable_2_data))
                pcc, pcc_p_value = stats.spearmanr(variable_1_data, variable_2_data)
                print("Spearman")
                r_text = "rs = "

                # Data visualization
                plt.xlabel(x_axis_label, fontweight='bold')
                plt.ylabel(y_axis_label, fontweight='bold')
                plt.title(title)

                # Drawing the trending line
                z = np.polyfit(variable_1_data, variable_2_data, DEGREE)
                p = np.poly1d(z)
                plt.plot(variable_1_data, variable_2_data, linestyle='-.', marker='o', color='b')
                # plt.plot(duration_list, p(duration_list), "k", label='Trending line')
                plt.plot(variable_1_data, p(variable_1_data), "k")
                # plt.legend(loc='best')

                # Printing the findings
                n_student_PCC = "N=" + str(len(variable_2_data))
                str_PCC = r_text + get_2_decimal(pcc) + ", p=" + get_2_decimal(pcc_p_value)

                if pcc_p_value > 0.0001:
                    cc_data = variable_1_name + " , " + variable_2_name + " ," + str(len(variable_1_data)) + " , " + r_text\
                              + get_2_decimal(pcc) + " , " + get_2_decimal(pcc_p_value) + "\n"
                else:
                    cc_data = variable_1_name + " , " + variable_2_name + " ," + str(len(variable_1_data)) + " , " + r_text\
                              + get_2_decimal(pcc) + " , " + str(pcc_p_value) + "\n"

                corr_coef_writer.write(cc_data)

                print(title)
                print(variable_1_data)
                print(variable_2_data)
                print(n_student_PCC)
                print(str_PCC)
                print("\n\n")

                # plt.show()


# Getting the data by which we will categorize. e.g. Years of experience
def get_categories_data():

    categories_data = []

    with open(root_path_categories, encoding="utf8") as opened_file:
        print(os.path.basename(root_path_categories))
        data = opened_file.readlines()

        # Reading the data(line by line)
        # Each row contains data of one categories. e.g. All participants age data
        for line in data:
            line = line.split(',')
            categories_data.append(line)
        return categories_data


# To analyze the data
# We have to send the data path where the files will contain data
def analyze_data():

    categories_data = get_categories_data()

    options = {12: g_methods.education_level_categorization}
    # 2: g_methods.age_categories
    # 3: g_methods.vehicle_categorization,
    # 4: g_methods.experience_categorization
    # 5: g_methods.driving_hour_categorization,
    # 6: g_methods.rest_interval_categorization,
    # 7: g_methods.duty_hours_categorization,
    # 8: g_methods.rest_hours_categorization,
    # 9: g_methods.marital_status_categorization,
    # 10: g_methods.lives_with_family_categorization,
    # 11: g_methods.no_of_housemates_categorization,
    # }

    data_retrieve_index = 0
    Group_1 = True

    if data_retrieve_index == 0:
        group_1_name_temp = ""  # As we do not have these data in this case
        group_2_name_temp = ""  # As we do not have these data in this case
        for function_index in range(12, 13):
            grouping_methods = options.get(function_index)
            # By which we are categorizing. e.g. Years of Experience
            working_category = categories_data[function_index - 1]
            # Getting the indices of the people whose data we need. e.g. People having experince <= 10 Years
            group_1_name, group_2_name, group_1_data_indices, group_2_data_indices = grouping_methods(working_category[1:])

    # Finding who is young and have education level at least SSC
    elif data_retrieve_index == 11110:  # 1 means age, 11 means education, 10 means SSC
        category_temp = categories_data[1]
        # Finding who is young
        group_1_name_temp, group_2_name_temp, group_1_data_indices_temp, group_2_data_indices_temp = \
            g_methods.age_categories(category_temp[1:])
        print("Age ", group_2_data_indices_temp)
        working_category = categories_data[11]
        # Finding who has at least SSC
        if Group_1: # Finding young and at least SSC
            group_1_name, group_1_data_indices = \
            g_methods.compound_education_categorize_atlesat_ssc(group_1_data_indices_temp, working_category)
            group_2_data_indices = []  # For generalisation, otherwise problem will occur in appending 0 index
        else: # Finding older and at least SSC
            group_2_name, group_2_data_indices = \
                g_methods.compound_education_categorize_atlesat_ssc(group_2_data_indices_temp, working_category)
            group_1_data_indices = [] # For generalisation
            print("index", group_2_data_indices)

    # Finding who is young and have education level below SSC
    elif data_retrieve_index == 1118:  # 1 means age, 11 means education, 8 means below SSC
        category_temp = categories_data[1]
        # Finding who are young
        group_1_name_temp, group_2_name_temp, group_1_data_indices_temp, group_2_data_indices_temp = \
            g_methods.age_categories(category_temp[1:])
        working_category = categories_data[11]
        # Finding who has below SSC education
        if Group_1:  # Finding young and below SSC
            group_1_name, group_1_data_indices = \
                g_methods.compound_education_categorize_below_ssc(group_1_data_indices_temp, working_category)
            group_2_data_indices = []  # For generalisation, otherwise problem will occur in appending 0 index
        else:  # Finding older and below SSC
            group_2_name, group_2_data_indices = \
                g_methods.compound_education_categorize_below_ssc(group_2_data_indices_temp, working_category)
            group_1_data_indices = []  # For generalisation

    # Finding who is young and have education level at least SSC and lives with family
    elif data_retrieve_index == 1119:  # 1 means age, 11 means education, 9 means family
        category_temp = categories_data[1]

        ########### Need to Checcccccck ####

        group_1_name_temp, group_2_name_temp, group_1_data_indices_temp, group_2_data_indices_temp =\
            g_methods.age_categories(category_temp[1:])
        # temp_category = categories_data[11]
        # group_1_name_temp, group_2_name_temp, group_1_data_indices_temp, group_2_data_indices_temp =\
        #     g_methods.compound_education_categorize(group_1_data_indices_temp, temp_category)

        # working_category = categories_data[9]
        # group_1_name, group_2_name, group_1_data_indices, group_2_data_indices = \
        #     g_methods.compound_family_categorization(group_1_data_indices_temp, working_category)

    group_1_data_indices.append(0)
    group_2_data_indices.append(0)

    if Group_1:
        str_write = group_1_name_temp + "," + group_1_name + "\n"
        print("Indices", group_1_data_indices)
        working_category = np.array(working_category)
        print(working_category[group_1_data_indices])
    else:
        str_write = group_2_name_temp + "," + group_2_name + "\n"
        print("Indices", group_2_data_indices)
        working_category = np.array(working_category)
        print(working_category[group_2_data_indices])
    corr_coef_writer.write(str_write)

    with open(root_data_path, encoding="utf8") as opened_file:
        print(os.path.basename(root_data_path))
        data = opened_file.readlines()

        # Reading the data(line by line)
        # Each row contains data of one type. e.g. All participants data of personality
        for line in data:
            line = line.split(',')
            line = np.array(line)

            if Group_1:
                data_set.append(line[group_1_data_indices])
                print(str_write," ", line[0])
                print(str_write, line[group_1_data_indices])
            else:
                data_set.append(line[group_2_data_indices])
                print(str_write, line[0])
                print(str_write, line[group_2_data_indices])

        # Find the correlation one by one
        for per_data_in_dataset in data_set:
            print("Length_Per_Data ", len(per_data_in_dataset))
            find_the_correlation(per_data_in_dataset)


analyze_data()
