import datetime


class Tool:
    @staticmethod
    def time_stamp(text: str):
        return f'{text}{datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S-%f")}'
