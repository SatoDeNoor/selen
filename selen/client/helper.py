import datetime
import operator
import time


class Tools:
    @staticmethod
    def time_stamp(text: str):
        return f'{text}{datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S-%f")}'

    @staticmethod
    def text_validation(actual_text: str, expected_text: str, condition, waiting=1, attempts=3):
        for attempt in range(attempts):
            fails_log = ''
            msg = f'#MESSAGE# Actual data: "{actual_text}", expected: "{expected_text}", condition: "{condition}". '
            try:
                ops = {'in': operator.contains,
                       '==': operator.eq,
                       '!=': operator.ne}[condition]
                if not ops(actual_text, expected_text):
                    fails_log = msg + ' Check FAILED'
                break
            except:
                pass
            time.sleep(waiting)
            if attempt + 1 == attempts:
                fails_log = msg + ' Check FAILED'
        return fails_log if fails_log else None