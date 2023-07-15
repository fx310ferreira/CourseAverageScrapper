from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import os

def get_students(students):
    i1 = students.find("(")
    i2 = students.find("A")-1
    if i1 == -1:
        return 0
    else:
        return int(students[i1+1:i2])

def add_grade(url, grades, course):

    student_number = driver.find_element(by= By.XPATH, value=url+'/td[2]').get_attribute("textContent")
    if(student_number) not in grades.keys():
        grades[student_number] = { "name": driver.find_element(by= By.XPATH, value=url+'/td[1]').get_attribute("textContent")}
    grade = driver.find_element(by= By.XPATH, value=url+'/td[4]/span').get_attribute("textContent")
    if grade.isnumeric():
        grade = int(grade)
    else:
        grade = 0
    
    if course not in grades[student_number].keys() or grades[student_number][course] < grade:
        grades[student_number][course] = grade
    
def get_grades(grades, courses, times, start=1):
    for i in range(courses):
        course = driver.find_element(by= By.XPATH, value=f'//*[@id="div_resultados_minhas_uc"]/table/tbody/tr[{start}]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[{i+1}]/td[1]').text.split("(")[0].strip()
        driver.find_element(by= By.XPATH, value=f'//*[@id="div_resultados_minhas_uc"]/table/tbody/tr[{start}]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[{i+1}]/td[8]/a').click()
        for j in range(len(times)):
            students = driver.find_element(by= By.XPATH, value=f'//*[@id="content"]/table/tbody/tr[{j+3}]/td/table/tbody/tr[1]/td/table/tbody/tr/td/a').text
            students = get_students(students)
            for k in range(students):
                add_grade(f'//*[@id="{times[j]}"]/table/tbody/tr/td/table/tbody/tr[{k+1}]', grades, course)
        print(f"Course {course} done")
        driver.find_element(by=By.XPATH, value = '//*[@id="context"]/a').click()

courses = 10
times = ["div_EF", "div_EN", "div_ER", "div_EE"]
grades = {}
base_url = "https://inforestudante.uc.pt/nonio/pautas/pesquisaPautas.do"

driver = webdriver.Firefox()
driver.get("https://inforestudante.uc.pt/nonio/security/login.do")
driver.find_element(by= By.ID, value="username").send_keys(os.getenv('USERNAME'))
driver.find_element(by= By.ID, value="password1").send_keys(os.getenv('PASSWORD'))
driver.find_element(by= By.XPATH, value='//*[@id="loginFormBean"]/table/tbody/tr[3]/td/div/input').click()
driver.get("https://inforestudante.uc.pt/nonio/pautas/pesquisaPautas.do")

driver.find_element(by= By.XPATH, value='//*[@id="dropdownAnoLectivoMinhasUc"]').click()
driver.find_element(by= By.XPATH, value='//*[@id="dropdownAnoLectivoMinhasUc"]/option[2]').click()
get_grades(grades, courses, times)

with open("grades1.pkl", "wb") as f:
    pickle.dump(grades, f)
driver.close()

