from datetime import datetime


def date_validate_YMD(date):
    try:
        _ = datetime.strptime(date.strip(), "%Y-%m-%d")
        return 1
    except ValueError:
        # try:
        #     _ = datetime.strptime(date, "%Y/%m/%d")
        #     return 2
        # except ValueError:
        return -1


if __name__ == '__main__':
    print(date_validate_YMD('2020-10-12 '.strip()))
