# coding: utf8
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time, sys

# TODO: print the acknowledgements
ack = u'''浙江大学安全理论考试满分脚本
------------------------------------------
请仔细阅读以下使用方式及注意事项后，按Enter键继续：
1. 本脚本的使用方式：
按Enter键继续后，会打开一个浏览器，在浏览器中填写好自己的学号密码，然后【不要】点击登录!
再次提醒：【不要点击登录】！
填写完毕后，回到该脚本再次按Enter键继续，该脚本会自动完成剩余步骤
2. 使用该脚本的过程中，页面可能会在某一时刻停顿，这是正常现象，但最多不会超过10秒
如果停顿超过10秒，【可能】该脚本已崩溃
3. 使用该脚本的过程中，可能会在某一时刻看到自己是0分，这是正常现象，不会影响最终结果
4. 使用该脚本的过程中，【绝对不要】自己操作浏览器，否则可能会发生不可预料的后果
5. 脚本会在完成填写100道题后，输出提示信息并自动终止，你可以随后填写剩下的问卷调查题并提交
6. 如果该脚本在使用的过程中出现问题，请立即切换至该脚本所在窗口，按Ctrl+C组合键打断脚本的执行
------------------------------------------
请仔细阅读以上使用方式即注意事项后，按Enter键继续
再次提醒：在浏览器中填写好自己的学号密码后，【不要】点击登录'''
print(ack)
input()

# TODO: choose the browser
prompt = u'''请输入相应数字选择浏览器：
1. Chrome
2. IE (not always work)
3. Safari (not tested)

我的选择是：'''
choice = int(input(prompt))
#
# browser = {
#     '1': webdriver.Chrome,
#     '2': webdriver.Ie,
#     '3': webdriver.Safari
# }

# TODO: start the browser
# driver = webdriver.Chrome(executable_path='chromedriver.exe')
# driver = browser[choice]()
driver = None
if choice == 1:
    driver = webdriver.Chrome()
elif choice == 2:
    driver = webdriver.Ie(capabilities={'ignoreZoomSetting': True})
elif choice == 3:
    driver = webdriver.Safari()
else:
    print('请输入正确的数字代号！')
    sys.exit(1)
driver.get('http://www.xsfww.cn')

# TODO: fill in the captcha
captcha = driver.find_element_by_id('login_vcode').text[1:-1]
captchaElmt = driver.find_element_by_id('login_verf')
captchaElmt.send_keys(captcha)
idElmt = driver.find_element_by_id('login_uid')
idElmt.click()

# TODO: wait until the user finishes the submit form
print(u'''如果你已经填写完毕自己的学号和密码，请按Enter键继续
如果该脚本在使用的过程中出现问题，请立即切换至该脚本所在窗口，按Ctrl+C组合键打断脚本的执行''')
input()

# TODO: login
loginBtn = driver.find_element_by_id('login_bt_login')
loginBtn.click()

# TODO: go to the pre-exam page
# time.sleep(5)
# want to use selenium wait but failed
# wait = WebDriverWait(driver, 10)
# startExamBtn = wait.until(EC.element_to_be_clickable((By.ID, 'main_bt_kaoshi')))
t = 0
while t < 10:
    try:
        startExamBtn = driver.find_element_by_id('main_bt_kaoshi')
        startExamBtn.click()
        # break
    except WebDriverException:
        time.sleep(1)
        t += 1
        continue
    break
# startExamBtn = driver.find_element_by_id('main_bt_kaoshi')
# startExamBtn.click()
confirmBtn = driver.find_element_by_id('popup_ok')
confirmBtn.click()

# TODO: open the exam page
driver.get('http://kaoshi.xsfww.cn/exam_basic_exam.php?action=paper&examid=2')

# TODO: open a new tab and fetch the correct answers
driver.get('http://kaoshi.xsfww.cn/exam_basic_exam.php?action=view&examid=2')
answers = [x.text[6:] for x in driver.find_elements_by_class_name('red')]

# for test use:
# singleChoiceAnswers = [x[6:] for x in answers[:40]]
# multiChoiceAnswers = [x[6:] for x in answers[40:60]]
# TorFAnswers = [x[6:] for x in answers[60:]]
# with open('answers.txt', 'wb') as file:
#     file.write(bytes('single choices:\n', encoding='utf8'))
#     file.write(bytes('\n'.join(singleChoiceAnswers), encoding='utf8'))
#     file.write(bytes('\nmultiple choices:\n', encoding='utf8'))
#     file.write(bytes('\n'.join(multiChoiceAnswers), encoding='utf8'))
#     file.write(bytes('\ntrue or false:\n', encoding='utf8'))
#     file.write(bytes('\n'.join(TorFAnswers), encoding='utf8'))

# TODO: fill in the answers
driver.get('http://kaoshi.xsfww.cn/exam_basic_exam.php?action=paper&examid=2')
# must remove the float element first, otherwise the click won't work!
element = driver.find_element_by_id('float')
driver.execute_script("""
var element = arguments[0];
element.parentNode.removeChild(element);
""", element)
qElmts = driver.find_elements_by_class_name('qu_option')
for i in range(100):
    options = qElmts[i].find_elements_by_tag_name('input')
    for option in options:
        if option.get_attribute('value') in answers[i]:
            option.click()

# TODO: print notification and wait for exit
print(u'脚本应该已经完成试卷的填写，请提交试卷后，按Enter键退出')
input()
