#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import smtplib
import time
import os

from datetime import datetime


class CustomError(Exception):
    pass


def send_email(error, location=''):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('bot.python.script@gmail.com', 'PythonScript25')

    if error:
        subject = 'Erreur Script SAAQ\n'
    else:
        subject = 'Disponibilite SAAQ : {}\n'.format(location)

    lien = 'https://saaq.gouv.qc.ca/services-en-ligne/citoyens/examen-conduite/prendre-rendez-vous/automobile-classe-5/#c37835'
    numero_permis = 'Numero du permis de conduire : C6007-300801-07'
    msg = "Subject: {}\n{}\n{}".format(subject, lien, numero_permis)

    if error:
        recipient = 'dandanny13.levy@gmail.com'
    else:
        recipient = 'rosaliecayer01@gmail.com'

    server.sendmail(
        'bot.python.script@gmail.com',
        recipient,
        msg
    )
    if error:
        print("\n========= ERREUR envoyé =========\n")
    else:
        print("\n========= Email envoyé =========\n")

    server.quit()


def check_availability():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")

    url = "https://saaq.gouv.qc.ca/services-en-ligne/citoyens/examen-conduite/prendre-rendez-vous/automobile-classe-5/"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    page = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    page.get(url)
    # page.minimize_window()

    button_get_appointment = WebDriverWait(page, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="colonne-plugin-service-en-ligne"]/div[3]/a')))
    button_get_appointment.click()
    time.sleep(2)
    current_url = page.current_url

    if (current_url != 'https://services.saaq.gouv.qc.ca/FonctionsWeb/RendezVous.Web/fr-CA/RendezVous/Renseignement'):
        message_closed = WebDriverWait(page, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="colonne-plugin-service-en-ligne"]/div[3]/p')))
        if (message_closed.get_attribute('class') == 'msg closed'):
            raise CustomError

    input_examen_pratique = WebDriverWait(page, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="TypeExamenPratique"]')))

    while not(input_examen_pratique.is_selected()):
        input_examen_pratique.click()

        input_examen_theorique = WebDriverWait(page, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="TypeExamenTheorique"]')))
        input_examen_theorique.click()
        input_examen_pratique.click()

    try:
        question_cours_de_conduite = WebDriverWait(page, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="CoursPratiqueOui"]')))
    except:
        input_examen_theorique.click()
        input_examen_pratique.click()

    question_cours_de_conduite.click()

    numero_permis = WebDriverWait(page, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="Identification_Permis_NoPermis"]')))

    numero_permis.clear()
    numero_permis.send_keys('C6007-300801-07')

    numero_telephone = WebDriverWait(page, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="Identification_Telephone_Numero"]')))

    numero_telephone.send_keys('4184559560', Keys.ENTER)

    time.sleep(5)

    # Clicking Rdv Buttons

    buttons_xpath = [
        '#block0 > div:nth-child(2) > div > div > div.media-body.GrvInfoCSListe > button',
        '#block0 > div:nth-child(4) > div > div > div.media-body.GrvInfoCSListe > button',
        '#block0 > div:nth-child(6) > div > div > div.media-body.GrvInfoCSListe > button'
    ]
    location = [
        "Quebec",
        "Levis",
        "Donnaconna"
    ]

    for i in range(3):
        button_rdv = WebDriverWait(page, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, buttons_xpath[i])))
        button_rdv.click()
        time.sleep(2)

        try:
            No_availability = WebDriverWait(page, 15).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ConteneurMessagesSevere"]/div/h3')))
        except:
            send_email(False, location[i])

        error_message = WebDriverWait(page, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ConteneurMessagesSevere"]/div')))
        if (error_message.get_attribute('class') != 'validation-summary-errors'):
            send_email(False, location[i])

    print("=========================================")
    print("Successfully Searched || {}".format(dt_string))
    print("=========================================")

    page.quit()


if __name__ == "__main__":
    os.system('clear')
    while True:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M")
        dayOfWeek = int(time.strftime("%w"))
        hourOfDay = datetime.today().strftime("%H:%M")

        while ((dayOfWeek in [1, 2, 3, 4, 5, 6] and hourOfDay >= '07:30' and hourOfDay <= '22:50') or (dayOfWeek == 0 and hourOfDay >= '12:00' and hourOfDay <= '22:50')):
            try:
                check_availability()
            except CustomError:
                pass
            except:
                send_email(True)
            print("==== Sleep Time ====")
            time.sleep(60*5)
            dayOfWeek = int(time.strftime("%w"))
            hourOfDay = datetime.today().strftime("%H:%M")
        print("================================================")
        print("The reservation are closed || {}".format(dt_string))
        print("================================================")
        if (dayOfWeek in [1, 2, 3, 4, 5, 6] and hourOfDay >= '22:50' and hourOfDay <= '00:00'):
            print("==== Overnight Sleep Time ====")
            time.sleep(60*60*8.25)
        elif (dayOfWeek == 0 and hourOfDay >= '22:50' and hourOfDay <= '00:00'):
            print("==== Overnight Sleep Time ====")
            time.sleep(60*60*12)
        else:
            print("==== Long Sleep Time ====")
            time.sleep(60*15)
