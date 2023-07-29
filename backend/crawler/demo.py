# from WXBizDataCrypt import WXBizDataCrypt
import datetime
from dvadmin.crawler.util import waimai_util


def main():
    # appId = 'wx0fb2061401ae94e6'
    # sessionKey = 'tiihtNczf5v6AKRyjwEUhQ=='
    # encryptedData = "59vo9jYCBVfVglxYdHZwTO5UoT4QAJSvHzMueWVfOzEfBR3Hxuns/NrISfeYSpH8TVCdbkcJxzlOEYIZNttpKcwbtNpgcACmgqlrpNjiw1/HKK4XO0uJfJlFQdeS61xlVoR9L/fO0Qe7L+fV1f2EK2tJI6n8xNpsuXqE8qOjsQqonkNVa/elkOqgzbhvQ2oTGny+oMGxGWdOjKInIR9xppYas+7Jq/mBzTRVLNe6MPUuOqrsg2HVsMJdAF6laBKHHyvOh4CSGePb5zlyHz5CK8XITiZuEtLyIU+vsRqy/qiOR4oOThQjUC+Dq8yuzEXe"
    # iv = "wjjSsaS9w7ltB5LPT3d6jA=="
    #
    # pc = WXBizDataCrypt(appId, sessionKey)
    #
    # print(pc.decrypt(encryptedData, iv))
    print(datetime.datetime.now() + datetime.timedelta(seconds=7200))
    device_uuid = '!cc4108b8-83aa-4355-8c63-1517eaf55ef2'
    print(device_uuid[1:])


if __name__ == '__main__':
    main()
