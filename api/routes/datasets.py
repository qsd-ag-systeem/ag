from core.search import retrieve_datasets
from api.helpers.response import success_response, error_response


def get():
    try:
        datasets = retrieve_datasets()
        data = [{'name': ds[0], 'count': ds[1]} for ds in datasets]
        return success_response(data)
    except:
        return error_response('An error occurred while fetching the datasets')


# delete datasets here as well
def delete():
    return error_response('Not yet implemented')
