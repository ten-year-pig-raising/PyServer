import time

from seleniumwire import webdriver  # Import from seleniumwire

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()


def wait_login():
    WEB_TITLE = "工作台"

    driver.get("https://gitee.com/login")

    wait_flag = 1
    while (wait_flag):
        handles = driver.window_handles  # 获取当前窗口句柄集合（列表类型）
        # 逐个窗口打印标题
        for b in handles:
            # driver.switch_to_window(b)

            # h_id = handles.index(b)
            # wb.switch_to_window(handles[h_id])

            if WEB_TITLE in driver.title:
                wait_flag = 0
                break

            # print(str(handels.index(b)) + " : " + wb.title + ": " + wb.current_url)
            print("等待打开登录后的页面...")
            time.sleep(5)


def main():
    # Go to the Google home page
    # driver.get('https://gitee.com/login')
    # Access requests via the `requests` attribute
    wait_login()
    driver.get('https://gitee.com/dashboard/projects')
    for request in driver.requests:
        if 'https://gitee.com/graphql' in request.url:
            if request.response:
                print(
                    request.url,
                    'Cookie=' + request.headers['Cookie'],
                    request.response.status_code,
                    # request.response.headers['Content-Type']
                )


if __name__ == '__main__':
    main()
