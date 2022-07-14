import time
import python_package
from random import randint


def set_variables(names, surnames, lib):
    # Set variables
    name = names[randint(0, 258000)]["name"]
    surname = surnames[randint(0, 151671)]["name"]
    password = lib.generate_random_password(range_int=7)
    mail = name + "." + surname + str(randint(10000, 1000000))

    return name, surname, password, mail


def get_numbers_list(transform, sms_service):
    active_number = transform.string_to_list_of_dict(sms_service.get_service(action="getCurrentActivationsList",
                                                                             status=1, order="id", orderBy="DESC"))
    new_number = transform.string_to_list_of_dict(sms_service.get_service(action="getCurrentActivationsList",
                                                                          status=0, order="id", orderBy="DESC"))

    aggregated_list = transform.agragate_list_of_dict(active_number, new_number)
    numbers = transform.group_list_of_dict(data=aggregated_list)

    return aggregated_list, numbers


def get_number(numbers, unusable_numbers, sms_service):
    numbers_filtered = []
    for number in numbers:
        phone_number = number["number"]
        number_id = number["id"]
        number_status = number["status"]
        if number_status == 0:
            response = sms_service.get_service(action="setStatus", id=number_id, status=6)
        elif number_status == 1:
            response = sms_service.get_service(action="setStatus", id=number_id, status=3)

        if any(elm in response for elm in ["ACTIVATION", "RETRY_GET"]):
            numbers_filtered.append({})
        else:
            pass
    return numbers_filtered


def select_phone_number(numbers_filtered, sms_service):
    if not numbers_filtered:
        active_number = sms_service.get_service(action="getNumber", service="go", country=15).split(':')
        phone_number = active_number[2]
        number_id = active_number[1]
        sms_service.get_service(action="setStatus", id=number_id, status=6)

    else:
        phone_number = numbers_filtered[0]["number"]
        number_id = numbers_filtered[0]["id"]

    return phone_number, number_id


def g_acc_create():

    sms_service_api_key = "b56234948f91575f343dff92939ec5b5"

    transform = python_package.Transform()
    names = transform.load_csv(file_name='Names.csv')
    surnames = transform.load_csv(file_name='Surnames.csv')

    sms_service = python_package.SmsServiceAPI(API_key=sms_service_api_key, lang="en")

    unusable_numbers = []
    for i in range(1, 10):

        # Set variables
        name, surname, password, mail = set_variables(names, surnames, lib=transform)

        aggregated_list, numbers = get_numbers_list(transform=transform, sms_service=sms_service)

        driver = python_package.webdriver_functions(browser="undetected_chromedriver",
                                                    arguments=["--disable-extensions",
                                                               "--disable-popup-blocking",
                                                               "--profile-directory=Default",
                                                               "--ignore-certificate-errors",
                                                               "--disable-plugins-discovery",
                                                               "--incognito",
                                                               "user_agent=DN",
                                                               "--disable-extensions",
                                                               "--start-maximized"], sub_process=True)
        driver.open_website(link="https://www.google.com/intl/pl/account/about/")

        # Sign in click
        driver.click_on_xpath(xpath="(//*[contains(@href, 'Sign')])[1]")

        # Basic info fill
        driver.send_keys_to_text_box(xpath="//*[@name='firstName']", text=name, interval=1)
        driver.send_keys_to_text_box(xpath="//*[@name='lastName']", text=surname)
        driver.send_keys_to_text_box(xpath="//*[@type='email']", text=mail)
        driver.click_on_xpath(xpath="//*[@aria-labelledby='selectioni1']")
        driver.send_keys_to_text_box(xpath="(//*[@name='Passwd'])[1]", text=password)
        driver.send_keys_to_text_box(xpath="//*[@name='ConfirmPasswd']", text=password)

        # Confirm
        driver.click_on_xpath(xpath="(//*[@type='button'])[2]")

        # Give Phone number
        numbers_filtered = get_number(numbers=numbers, unusable_numbers=unusable_numbers, sms_service=sms_service)
        phone_number, number_id = select_phone_number(numbers_filtered=numbers_filtered, sms_service=sms_service)
        driver.send_keys_to_text_box(xpath="//*[@type='tel']", text="+" + phone_number)
        driver.click_on_xpath(xpath="(//*[@type='button'])[1]")

        if driver.check_if_xpath_exists(xpath="//*[@fill='currentColor' and @width='16px' and @height='16px']"):
            unusable_numbers.append(phone_number)
            driver.quit_driver()
        else:

            # Return received code
            for i in range(1, 60):
                verification_code = sms_service.get_service(action="getStatus", id=number_id)
                time.sleep(1)
                if "WAIT" in verification_code or "ERROR" in verification_code:
                    pass
                else:
                    break

            verification_code = verification_code.split(":")[1]

            # Type verification code
            driver.send_keys_to_text_box(xpath="(//*[@type='tel'])", text=verification_code, interval=1)
            driver.click_on_xpath(xpath="(//*[@type='button'])[2]")

            # Select date
            driver.send_keys_to_text_box(xpath="(//*[@type='tel'])[2]", text=randint(1, 28), interval=1)
            driver.click_on_xpath(xpath="(//*[@aria-labelledby='month-label'])")
            driver.click_on_xpath(f"//*[@value='{randint(5, 12)}']")
            driver.send_keys_to_text_box(xpath="(//*[@type='tel'])[3]", text=randint(1950, 2002))

            # Select gender
            driver.click_on_xpath(xpath="(//*[@aria-labelledby='gender-label'])")
            driver.click_on_xpath(xpath="(//*[@value=1])[2]")

            # Confirm
            driver.click_on_xpath(xpath="(//*[@type='button'])[1]")

            # Skip phone number usage
            driver.click_on_xpath(xpath="(//*[@type='button'])[5]")

            # Fast personalization
            driver.click_on_xpath(xpath="(//*[@role='radio'])[1]")
            driver.click_on_xpath(xpath="(//*[@type='button'])")

            driver.click_on_xpath(xpath="(//*[@type='button'])[5]")
            driver.click_on_xpath(xpath="(//*[@type='button'])[2]")

            transform.append_list_as_row(file_name="mails.csv", list_of_elem=[mail, name, surname, password, phone_number])

            driver.quit_driver()


if __name__ == '__main__':
    g_acc_create()
