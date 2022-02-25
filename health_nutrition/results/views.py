from django.shortcuts import render
from django.views import View
from django.http import request
import pandas as pd
import seaborn as sn
import numpy as np
import matplotlib as plt


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
        return render(request, 'bmi_analysis.html')
