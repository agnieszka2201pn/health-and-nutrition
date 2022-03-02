from django.shortcuts import render
from django.views import View
from django.http import request
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import table
import dataframe_image as dfi

class ShowMenu(View):
    """class based view showing main menu of analysis"""
    def get(self, request):
        """class method,
        result: show main menu"""
        return render(request, 'main_menu.html')

class ShowPurpose(View):
    """class based view showing html wit purpose of the project"""
    def get(self, request):
        """class method,
        result: show html with purpose of the project"""
        return render(request, 'purpose.html')

class ShowBMIAnalysis(View):
    """class based view showing results of BMI analysis"""



    def get(self, request):
        """class method,
        result: show html with result of BMI analysis"""
        bmi = pd.read_csv('results\data_files\hlth_ehis_bm1e_1_Data.csv')
        bmi_head = bmi.head(20) # data input as data frame
        df_styled = bmi_head.style.background_gradient()
        dfi.export(df_styled, 'bmi_table.png')
        bmi.drop('UNIT', axis=1, inplace=True)
        bmi.drop('Flag and Footnotes', axis=1, inplace=True)
        bmi.drop('AGE', axis=1, inplace=True)
        bmi_cropped_head = bmi.head(20)
        df_styled_cropped = bmi_cropped_head.style.background_gradient()
        dfi.export(df_styled_cropped,'bmi_table_cropped.png')


        # cropped_bmi_style = bmi.style.background_gradient()
        # dfi.export(cropped_bmi_style, 'bmi_table_cropped.png')

        unique_geo_data = bmi['GEO'].unique()
        unique_geo_data_df = pd.DataFrame(unique_geo_data)
        df_styled_1 = unique_geo_data_df.style.background_gradient()
        dfi.export(df_styled_1, 'unique_geo_data.png')
        bmi_columns = bmi.columns
        bmi_types = bmi['BMI'].unique()
        bmi_description = bmi.describe(include=['O'])
        df_styled_2 = bmi_description.style.background_gradient()
        dfi.export(df_styled_2,'static\description.png')

        countries = bmi['GEO'].unique().tolist()[2:]
        bmi_single_countries = bmi[bmi['GEO'].isin(countries)].copy()
        bmi_2019 = bmi_single_countries[bmi_single_countries['TIME'] == 2019].copy()

        def change_to_number(x):
            if x == ':':
                return 0
            else:
                return float(x)

        bmi_2019['Value'] = bmi_2019['Value'].apply(lambda x: change_to_number(x))

        education_descriptions = bmi_2019['ISCED11'].unique().tolist()
        education_simplified = ['lower', 'middle', 'upper']
        education_dict = {name: number for name, number in zip(education_descriptions, education_simplified)}
        bmi_2019['education_level'] = bmi_2019['ISCED11'].map(education_dict)

        df_styled_3 = bmi_2019.head(20).style.background_gradient()
        dfi.export(df_styled_3, 'bmi2019.png')

        pivot_bmi = bmi_2019.pivot_table(values='Value', index='education_level', columns='BMI').round(2)
        df_styled_4 = pivot_bmi.style.background_gradient()
        dfi.export(df_styled_4, 'pivot_bmi.png')

        # plot = plt.subplot(111, frame_on=False)
        # plot.xaxis.set_visible(False)
        # plot.yaxis.set_visible(False)
        # table(plot, bmi_description, loc='upper right')
        # pict = plt.savefig('desc_plot.png')
        first_conclusions = "First conclusions: data frame contains 1224 records. There are 3 BMI values: Underweight, " \
                            "Normal and Overweigth. Data covers 34 countries (including collected information for the EU), " \
                            "3 education levels, provides differentiation between man and women, but not the age. " \
                            "Therefore the column: AGE can also be removed."
        heat_plot = sns.heatmap(bmi.isnull())
        heat_plot_pict = heat_plot.get_figure()
        heat_plot_pict.savefig("output.png")

        # bmi.drop('UNIT', axis=1, inplace=True)
        # bmi.drop('Flag and Footnotes', axis=1, inplace=True)
        # bmi.drop('AGE', axis=1, inplace=True)




        return render(request, 'bmi_analysis.html', {'bmi': bmi,
                                                         'geo': unique_geo_data,
                                                         'columns': bmi_columns,
                                                         'bmi_types': bmi_types,
                                                         'bmi_description': bmi_description,
                                                        'first_conclusions':first_conclusions,
                                                        })
