from drivers import owrt
def get_router(router_data):
    if router_data['type'] == 'owrt':
        return owrt.OwrtRouter()