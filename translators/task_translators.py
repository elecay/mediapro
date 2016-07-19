
class TaskTranslator:

    def __init__(self):
        pass

    @staticmethod
    def translate(source, destination):
        if 'start' in source:
            destination['start'] = source['start']
        if 'title' in source:
            destination['title'] = str(source['title'])
        if 'worker' in source:
            destination['worker'] = str(source['worker'])
        if 'status' in source:
            destination['status'] = str(source['status'])
        if 'payload' in source:
            destination['payload'] = source['payload']
